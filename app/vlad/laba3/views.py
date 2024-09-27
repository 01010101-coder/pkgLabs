import os
from flask import request, render_template
from . import vlad_laba3_bp as bp
from werkzeug.utils import secure_filename
from .image_processing import load_image, local_threshold, adaptive_threshold, segment_image, segment_brightness
import cv2

UPLOAD_FOLDER = 'pkgLabs/static/laba3/uploads/'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def clear_upload_folder(folder):
    """Функция для очистки папки с загрузками"""
    for root, dirs, files in os.walk(folder):
        for file in files:
            file_path = os.path.join(root, file)
            try:
                if os.path.isfile(file_path) or os.path.islink(file_path):
                    os.unlink(file_path)
            except Exception as e:
                print(f'Failed to delete {file_path}. Reason: {e}')


@bp.route('/vlad/laba3', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Проверяем, существует ли директория для загрузок, если нет, создаем её
        if not os.path.exists(UPLOAD_FOLDER):
            os.makedirs(UPLOAD_FOLDER)

        # Очищаем папку перед загрузкой нового файла
        clear_upload_folder(UPLOAD_FOLDER)

        # Проверяем, есть ли файл в запросе
        if 'file' not in request.files:
            return 'No file part'

        file = request.files['file']
        if file.filename == '':
            return 'No selected file'

        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            filepath = os.path.join(UPLOAD_FOLDER, filename)
            file.save(filepath)

            # Загрузка изображения
            image = load_image(filepath)

            # Выполняем пороговые обработки и сегментацию
            local_thresh = local_threshold(image)
            adaptive_thresh = adaptive_threshold(image)
            edges, lines_image, corners_image = segment_image(image)
            edges_dilated = segment_brightness(image)

            # Сохраняем обработанные изображения
            cv2.imwrite(os.path.join(UPLOAD_FOLDER, 'local_threshold.jpg'), local_thresh)
            cv2.imwrite(os.path.join(UPLOAD_FOLDER, 'adaptive_threshold.jpg'), adaptive_thresh)
            cv2.imwrite(os.path.join(UPLOAD_FOLDER, 'lines.jpg'), lines_image)
            cv2.imwrite(os.path.join(UPLOAD_FOLDER, 'corners.jpg'), corners_image)
            cv2.imwrite(os.path.join(UPLOAD_FOLDER, 'edges_dilated.jpg'), edges_dilated)

            # Передаем имена файлов для отображения в шаблон
            return render_template('laba3/index.html',
                                   filename=filename,
                                   local_thresh_filename='local_threshold.jpg',
                                   adaptive_thresh_filename='adaptive_threshold.jpg',
                                   lines_filename='lines.jpg',
                                   corners_filename='corners.jpg',
                                   edges_dilated_filename='edges_dilated.jpg')

    return render_template('laba3/index.html')
