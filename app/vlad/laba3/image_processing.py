import cv2
import numpy as np


def load_image(file_path):
    """Загружает изображение с указанного пути"""
    image = cv2.imread(file_path, cv2.IMREAD_COLOR)
    return image


def local_threshold(image):
    """Применение локальной пороговой обработки (адаптивный порог)"""
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    thresholded = cv2.adaptiveThreshold(
        gray, 255, cv2.ADAPTIVE_THRESH_MEAN_C,
        cv2.THRESH_BINARY, 11, 2
    )
    return thresholded


def adaptive_threshold(image):
    """Применение адаптивной пороговой обработки с использованием гауссового среднего"""
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    thresholded = cv2.adaptiveThreshold(
        gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
        cv2.THRESH_BINARY, 11, 2
    )
    return thresholded


def detect_edges(image):
    """Обнаружение перепадов яркости с помощью оператора Canny"""
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    edges = cv2.Canny(gray, 100, 200)
    return edges


def detect_lines(image):
    """Обнаружение линий с помощью преобразования Хафа"""
    edges = detect_edges(image)
    lines = cv2.HoughLinesP(edges, 1, np.pi / 180, 100, minLineLength=100, maxLineGap=10)
    line_image = np.copy(image)

    if lines is not None:
        for line in lines:
            x1, y1, x2, y2 = line[0]
            cv2.line(line_image, (x1, y1), (x2, y2), (0, 255, 0), 2)

    return line_image


def detect_corners(image):
    """Обнаружение углов (точек) с использованием метода Shi-Tomasi"""
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    corners = cv2.goodFeaturesToTrack(gray, 100, 0.01, 10)
    corners = corners.astype(np.int32)

    corner_image = np.copy(image)

    for corner in corners:
        x, y = corner.ravel()
        cv2.circle(corner_image, (x, y), 5, (0, 255, 0), -1)

    return corner_image


def segment_image(image):
    """Комбинация обнаружения краев, линий и точек"""
    edges = detect_edges(image)
    lines_image = detect_lines(image)
    corners_image = detect_corners(image)

    return edges, lines_image, corners_image


def segment_brightness(image):
    """Сегментация изображения по перепадам яркости с использованием градиентов Sobel и Canny"""
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Используем алгоритм Canny для выделения краев
    edges = cv2.Canny(gray, 100, 200)

    # Опционально: Применение морфологических операций для улучшения результата
    kernel = np.ones((3, 3), np.uint8)
    edges_dilated = cv2.dilate(edges, kernel, iterations=1)

    return edges_dilated


