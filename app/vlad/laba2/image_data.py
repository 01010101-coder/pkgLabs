import os
from PIL import Image


def get_image_info(image_path):
    try:
        with Image.open(image_path) as img:
            return {
                "filename": os.path.basename(image_path),
                "size": img.size,
                "dpi": img.info.get("dpi", "Not available"),
                "mode": img.mode,
                "compression": img.info.get("compression", "Not available")
            }
    except (IOError, OSError, Image.UnidentifiedImageError):
        # Если файл не является изображением, пропустить его
        return None


def process_images_in_directory(directory):
    image_data = []
    supported_formats = ('.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tif', '.tiff', '.pcx')

    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.lower().endswith(supported_formats):
                filepath = os.path.join(root, file)
                image_info = get_image_info(filepath)

                # Добавляем только валидные изображения
                if image_info:
                    image_data.append(image_info)
    return image_data
