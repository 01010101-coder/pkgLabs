import os
import zipfile
from flask import render_template, request, redirect, url_for
from werkzeug.utils import secure_filename
from app.vlad.laba2.image_data import process_images_in_directory

from . import vlad_laba2_bp as laba2_bp

UPLOAD_FOLDER = 'app/vlad/laba2/images'
ALLOWED_EXTENSIONS = {'zip'}


# Проверка допустимых форматов файлов (только zip)
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


# Функция очистки папки с изображениями
def clear_upload_folder(folder):
    for root, dirs, files in os.walk(folder):
        for file in files:
            file_path = os.path.join(root, file)
            try:
                if os.path.isfile(file_path) or os.path.islink(file_path):
                    os.unlink(file_path)  # Удаление файлов
            except Exception as e:
                print(f'Failed to delete {file_path}. Reason: {e}')
        for dir in dirs:
            dir_path = os.path.join(root, dir)
            try:
                os.rmdir(dir_path)  # Удаление пустых директорий
            except Exception as e:
                print(f'Failed to delete {dir_path}. Reason: {e}')


# Функция очистки папки __MACOSX
def clear_macosx_folder(folder):
    macosx_folder = os.path.join(folder, '__MACOSX')
    if os.path.exists(macosx_folder):
        for root, dirs, files in os.walk(macosx_folder, topdown=False):
            for file in files:
                os.remove(os.path.join(root, file))
            for dir in dirs:
                os.rmdir(os.path.join(root, dir))
        os.rmdir(macosx_folder)


# Функция распаковки архива
def unzip_file(zip_path, extract_to):
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extractall(extract_to)


# Маршрут для отображения и загрузки файлов
@laba2_bp.route('/vlad/laba2', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Очистка папки перед загрузкой новых файлов
        clear_upload_folder(UPLOAD_FOLDER)

        # Проверка наличия файлов
        if 'files[]' not in request.files:
            return redirect(request.url)

        files = request.files.getlist('files[]')
        for file in files:
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file_path = os.path.join(UPLOAD_FOLDER, filename)
                file.save(file_path)

                # Распаковка архива ZIP
                unzip_file(file_path, UPLOAD_FOLDER)

                # Удаление папки __MACOSX, если она существует
                clear_macosx_folder(UPLOAD_FOLDER)

        # После загрузки и распаковки файлов происходит обработка
        return redirect(url_for('laba2.index'))

    # Обработка изображений и отображение результата
    images = process_images_in_directory(UPLOAD_FOLDER)
    return render_template('laba2/index.html', images=images)
