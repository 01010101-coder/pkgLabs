import zipfile
from flask import render_template, request, redirect, url_for
from werkzeug.utils import secure_filename
from app.vlad.laba2.image_data import process_images_in_directory
import os
from concurrent.futures import ThreadPoolExecutor
import time

from . import vlad_laba2_bp as laba2_bp

UPLOAD_FOLDER = 'app/vlad/laba2/images'
ALLOWED_EXTENSIONS = {'zip'}


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def clear_upload_folder(folder):
    for root, dirs, files in os.walk(folder):
        for file in files:
            file_path = os.path.join(root, file)
            try:
                if os.path.isfile(file_path) or os.path.islink(file_path):
                    os.unlink(file_path)
            except Exception as e:
                print(f'Failed to delete {file_path}. Reason: {e}')


def clear_macosx_folder(folder):
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


def unzip_file(zip_path, extract_to):
    try:
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(extract_to)
    except zipfile.BadZipFile as e:
        print(f'Failed to unzip file {zip_path}. Reason: {e}')
    except Exception as e:
        print(f'Error during unzip process for file {zip_path}. Reason: {e}')


LOG_FILE = 'performance_log.txt'


def log_performance(message):
    """Функция для записи времени в лог-файл."""
    with open(LOG_FILE, 'a') as log_file:
        log_file.write(message + '\n')


@laba2_bp.route('/vlad/laba2', methods=['GET', 'POST'])
def index():
    try:
        start_time = time.time()  # Запоминаем время начала обработки запроса
        if request.method == 'POST':
            clear_upload_folder(UPLOAD_FOLDER)

            if 'files[]' not in request.files:
                return redirect(request.url)

            files = request.files.getlist('files[]')

            if not os.path.exists(UPLOAD_FOLDER):
                os.makedirs(UPLOAD_FOLDER)

            # Измеряем время распаковки файлов
            unzip_start_time = time.time()
            with ThreadPoolExecutor() as executor:
                futures = []
                for file in files:
                    if file and allowed_file(file.filename):
                        filename = secure_filename(file.filename)
                        file_path = os.path.join(UPLOAD_FOLDER, filename)
                        file.save(file_path)

                        # Параллельно распаковываем каждый архив
                        futures.append(executor.submit(unzip_file, file_path, UPLOAD_FOLDER))

                for future in futures:
                    future.result()
            unzip_time = time.time() - unzip_start_time
            log_performance(f'Время на распаковку файлов: {unzip_time:.2f} секунд')

            # Убираем папку __MACOSX после распаковки
            clear_macosx_folder(UPLOAD_FOLDER)

            # Измеряем время обработки изображений
            process_start_time = time.time()
            images = process_images_in_directory(UPLOAD_FOLDER)
            process_time = time.time() - process_start_time
            log_performance(f'Время на обработку изображений: {process_time:.2f} секунд')

            # Измеряем время рендеринга шаблона
            render_start_time = time.time()
            response = render_template('laba2/index.html', images=images)
            render_time = time.time() - render_start_time
            log_performance(f'Время на рендеринг шаблона: {render_time:.2f} секунд')

            # Очищаем папку после обработки
            clear_upload_folder(UPLOAD_FOLDER)

            # Общее время выполнения запроса
            total_time = time.time() - start_time
            log_performance(f'Общее время выполнения запроса: {total_time:.2f} секунд\n')

            return response

        # Для GET-запросов
        process_start_time = time.time()
        images = process_images_in_directory(UPLOAD_FOLDER)
        process_time = time.time() - process_start_time
        log_performance(f'Время на обработку изображений: {process_time:.2f} секунд')

        render_start_time = time.time()
        response = render_template('laba2/index.html', images=images)
        render_time = time.time() - render_start_time
        log_performance(f'Время на рендеринг шаблона: {render_time:.2f} секунд')

        return response

    except Exception as e:
        log_performance(f'Error in index route: {e}')
        return render_template('laba2/error.html', error=str(e)), 500

