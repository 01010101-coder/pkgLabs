import os
from PIL import Image
from concurrent.futures import ThreadPoolExecutor


def get_image_info(image_path):
    try:
        with Image.open(image_path) as img:
            if img.mode == 'RGB':
                color_depth = 8 * 3
            elif img.mode == 'RGBA':
                color_depth = 8 * 4
            elif img.mode == 'L':
                color_depth = 8
            else:
                color_depth = "Unknown"
            return {
                "format": img.format,
                "filename": os.path.basename(image_path),
                "size": img.size,
                "color_depth": color_depth,
                "mode": img.mode,
                "compression": img.info.get("compression", "Not available")
            }
    except (IOError, OSError, Image.UnidentifiedImageError):
        return None


def process_single_image(file):
    image_info = get_image_info(file)
    return image_info if image_info else None


def process_images_in_directory(directory):
    image_data = []
    supported_formats = ('.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tif', '.tiff', '.pcx')

    # Используем многопоточность для обработки изображений
    with ThreadPoolExecutor() as executor:
        futures = []
        for root, dirs, files in os.walk(directory):
            for file in files:
                if file.lower().endswith(supported_formats):
                    filepath = os.path.join(root, file)
                    futures.append(executor.submit(process_single_image, filepath))

        # Собираем результаты
        for future in futures:
            image_info = future.result()
            if image_info:
                image_data.append(image_info)

    return image_data
