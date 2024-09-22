import zipfile
from flask import render_template, request, redirect, url_for
from werkzeug.utils import secure_filename
from app.vlad.laba2.image_data import process_images_in_directory
import os
import asyncio
from concurrent.futures import ProcessPoolExecutor
from aiomultiprocess import Pool

from . import vlad_laba2_bp as laba2_bp

UPLOAD_FOLDER = 'app/vlad/laba2/images'
ALLOWED_EXTENSIONS = {'zip'}


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


async def clear_upload_folder(folder):
    for root, dirs, files in os.walk(folder):
        for file in files:
            file_path = os.path.join(root, file)
            try:
                if os.path.isfile(file_path) or os.path.islink(file_path):
                    os.unlink(file_path)
            except Exception as e:
                print(f'Failed to delete {file_path}. Reason: {e}')


async def clear_macosx_folder(folder):
    macosx_folder = os.path.join(folder, '__MACOSX')
    if os.path.exists(macosx_folder):
        for root, dirs, files in os.walk(macosx_folder, topdown=False):
            for file in files:
                try:
                    os.remove(os.path.join(root, file))
                except Exception as e:
                    print(f'Failed to delete file {file} in __MACOSX. Reason: {e}')
            for dir in dirs:
                try:
                    os.rmdir(os.path.join(root, dir))
                except Exception as e:
                    print(f'Failed to delete directory {dir} in __MACOSX. Reason: {e}')
        try:
            os.rmdir(macosx_folder)
        except Exception as e:
            print(f'Failed to delete __MACOSX directory. Reason: {e}')


async def unzip_file(zip_path, extract_to):
    try:
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(extract_to)
    except zipfile.BadZipFile as e:
        print(f'Failed to unzip file {zip_path}. Reason: {e}')
    except Exception as e:
        print(f'Error during unzip process for file {zip_path}. Reason: {e}')


@laba2_bp.route('/vlad/laba2', methods=['GET', 'POST'])
async def index():
    try:
        if request.method == 'POST':
            # Очищаем папку перед загрузкой новых файлов
            await clear_upload_folder(UPLOAD_FOLDER)

            if 'files[]' not in request.files:
                return redirect(request.url)

            files = request.files.getlist('files[]')

            if not os.path.exists(UPLOAD_FOLDER):
                os.makedirs(UPLOAD_FOLDER)

            # Сохраняем файлы в папку перед их обработкой
            saved_file_paths = []
            for file in files:
                if file and allowed_file(file.filename):
                    filename = secure_filename(file.filename)
                    file_path = os.path.join(UPLOAD_FOLDER, filename)
                    await asyncio.to_thread(file.save, file_path)  # Асинхронно сохраняем файл
                    saved_file_paths.append(file_path)

            # Распаковываем файлы с помощью асинхронного пула
            async with Pool() as pool:
                tasks = [pool.apply(unzip_file, args=(file_path, UPLOAD_FOLDER)) for file_path in saved_file_paths]
                await asyncio.gather(*tasks)

            await clear_macosx_folder(UPLOAD_FOLDER)

            # Обрабатываем изображения с помощью ProcessPoolExecutor
            loop = asyncio.get_running_loop()
            with ProcessPoolExecutor() as executor:
                images = await loop.run_in_executor(executor, process_images_in_directory, UPLOAD_FOLDER)

            response = render_template('laba2/index.html', images=images)

            # Очищаем папку после завершения всех операций
            await clear_upload_folder(UPLOAD_FOLDER)
            return response

        images = process_images_in_directory(UPLOAD_FOLDER)
        return render_template('laba2/index.html', images=images)
    except Exception as e:
        print(f'Error in index route: {e}')
        return render_template('laba2/error.html', error=str(e)), 500
