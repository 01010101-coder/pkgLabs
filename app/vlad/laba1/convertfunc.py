
def cmyk_to_rgb(c, m, y, k):
    r = 255 * (1 - c) * (1 - k)
    g = 255 * (1 - m) * (1 - k)
    b = 255 * (1 - y) * (1 - k)
    return int(r), int(g), int(b)


def lab_to_xyz(l, a, b):
    y = (l + 16) / 116
    x = a / 500 + y
    z = y - b / 200

    x = 95.047 * (x ** 3 if x ** 3 > 0.008856 else (x - 16 / 116) / 7.787)
    y = 100.0 * (y ** 3 if y ** 3 > 0.008856 else (y - 16 / 116) / 7.787)
    z = 108.883 * (z ** 3 if z ** 3 > 0.008856 else (z - 16 / 116) / 7.787)

    return x, y, z


def xyz_to_rgb(x, y, z):
    # Нормализуем XYZ
    x /= 100.0
    y /= 100.0
    z /= 100.0

    # Применяем матрицу преобразования
    r = x * 3.2406 + y * -1.5372 + z * -0.4986
    g = x * -0.9689 + y * 1.8758 + z * 0.0415
    b = x * 0.0557 + y * -0.2040 + z * 1.0570

    # Применяем gamma-коррекцию
    r = 12.92 * r if r <= 0.0031308 else 1.055 * (r ** (1 / 2.4)) - 0.055
    g = 12.92 * g if g <= 0.0031308 else 1.055 * (g ** (1 / 2.4)) - 0.055
    b = 12.92 * b if b <= 0.0031308 else 1.055 * (b ** (1 / 2.4)) - 0.055

    return max(0, min(255, int(r * 255))), max(0, min(255, int(g * 255))), max(0, min(255, int(b * 255)))


def lab_to_rgb(l, a, b):
    x, y, z = lab_to_xyz(l, a, b)
    return xyz_to_rgb(x, y, z)


def hsv_to_rgb(h, s, v):
    c = v * s
    x = c * (1 - abs((h / 60) % 2 - 1))
    m = v - c

    if 0 <= h < 60:
        r, g, b = c, x, 0
    elif 60 <= h < 120:
        r, g, b = x, c, 0
    elif 120 <= h < 180:
        r, g, b = 0, c, x
    elif 180 <= h < 240:
        r, g, b = 0, x, c
    elif 240 <= h < 300:
        r, g, b = x, 0, c
    else:
        r, g, b = c, 0, x

    r, g, b = [(n + m) * 255 for n in (r, g, b)]
    return int(r), int(g), int(b)


def rgb_to_cmyk(r, g, b):
    if (r == 0) and (g == 0) and (b == 0):
        return 0, 0, 0, 1
    c = 1 - r / 255.0
    m = 1 - g / 255.0
    y = 1 - b / 255.0
    k = min(c, m, y)
    c = (c - k) / (1 - k)
    m = (m - k) / (1 - k)
    y = (y - k) / (1 - k)
    return round(c, 2), round(m, 2), round(y, 2), round(k, 2)


def rgb_to_xyz(r, g, b):
    # Нормализуем RGB
    r, g, b = [x / 255.0 for x in [r, g, b]]

    # Gamma Correction
    r = r / 12.92 if r <= 0.04045 else ((r + 0.055) / 1.055) ** 2.4
    g = g / 12.92 if g <= 0.04045 else ((g + 0.055) / 1.055) ** 2.4
    b = b / 12.92 if b <= 0.04045 else ((b + 0.055) / 1.055) ** 2.4

    # Переводим в XYZ
    x = r * 0.4124564 + g * 0.3575761 + b * 0.1804375
    y = r * 0.2126729 + g * 0.7151522 + b * 0.0721750
    z = r * 0.0193339 + g * 0.1191920 + b * 0.9503041

    return x * 100, y * 100, z * 100


def xyz_to_lab(x, y, z):
    # Стандартная белая точка D65
    x, y, z = x / 95.047, y / 100.0, z / 108.883

    # Применяем формулу для LAB
    x = x ** (1 / 3) if x > 0.008856 else (7.787 * x + 16 / 116)
    y = y ** (1 / 3) if y > 0.008856 else (7.787 * y + 16 / 116)
    z = z ** (1 / 3) if z > 0.008856 else (7.787 * z + 16 / 116)

    l = (116 * y) - 16
    a = 500 * (x - y)
    b = 200 * (y - z)

    return round(l, 2), round(a, 2), round(b, 2)


def rgb_to_lab(r, g, b):
    x, y, z = rgb_to_xyz(r, g, b)
    return xyz_to_lab(x, y, z)


def rgb_to_hsv(r, g, b):
    r, g, b = r / 255.0, g / 255.0, b / 255.0
    max_c = max(r, g, b)
    min_c = min(r, g, b)
    delta = max_c - min_c

    # Hue Calculation
    if delta == 0:
        h = 0
    elif max_c == r:
        h = ((g - b) / delta) % 6
    elif max_c == g:
        h = (b - r) / delta + 2
    else:
        h = (r - g) / delta + 4
    h = round(h * 60)

    # Saturation Calculation
    s = 0 if max_c == 0 else delta / max_c

    # Value Calculation
    v = max_c

    return round(h, 2), round(s, 2), round(v, 2)
