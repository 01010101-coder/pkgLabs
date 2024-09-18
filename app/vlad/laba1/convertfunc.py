def cmyk_to_rgb(c, m, y, k):
    r = 255 * (1 - c) * (1 - k)
    g = 255 * (1 - m) * (1 - k)
    b = 255 * (1 - y) * (1 - k)
    return r, g, b

def rgb_to_cmyk(r, g, b):
    r, g, b = r / 255, g / 255, b / 255
    k = 1 - max(r, g, b)
    if k < 1:
        c = (1 - r - k) / (1 - k)
        m = (1 - g - k) / (1 - k)
        y = (1 - b - k) / (1 - k)
    else:
        c = m = y = 0
    return c, m, y, k

def rgb_to_xyz(r, g, b):
    r = r / 255
    g = g / 255
    b = b / 255

    if r > 0.04045:
        r = ((r + 0.055) / 1.055) ** 2.4
    else:
        r = r / 12.92
    if g > 0.04045:
        g = ((g + 0.055) / 1.055) ** 2.4
    else:
        g = g / 12.92
    if b > 0.04045:
        b = ((b + 0.055) / 1.055) ** 2.4
    else:
        b = b / 12.92

    r *= 100
    g *= 100
    b *= 100

    x = r * 0.4124 + g * 0.3576 + b * 0.1805
    y = r * 0.2126 + g * 0.7152 + b * 0.0722
    z = r * 0.0193 + g * 0.1192 + b * 0.9505
    return x, y, z

def xyz_to_rgb(x, y, z):
    x /= 100
    y /= 100
    z /= 100

    r = x * 3.2406 + y * -1.5372 + z * -0.4986
    g = x * -0.9689 + y * 1.8758 + z * 0.0415
    b = x * 0.0557 + y * -0.2040 + z * 1.0570

    r = max(0, min(255, 255 * (1.055 * (r ** (1 / 2.4)) - 0.055) if r > 0.0031308 else r * 12.92))
    g = max(0, min(255, 255 * (1.055 * (g ** (1 / 2.4)) - 0.055) if g > 0.0031308 else g * 12.92))
    b = max(0, min(255, 255 * (1.055 * (b ** (1 / 2.4)) - 0.055) if b > 0.0031308 else b * 12.92))

    return r, g, b

def xyz_to_lab(x, y, z):
    x /= 95.047
    y /= 100.000
    z /= 108.883

    def f(t):
        if t > 0.008856:
            return t ** (1/3)
        else:
            return (7.787 * t) + (16 / 116)

    l = (116 * f(y)) - 16
    a = 500 * (f(x) - f(y))
    b = 200 * (f(y) - f(z))

    return l, a, b

def lab_to_xyz(l, a, b):
    y = (l + 16) / 116
    x = a / 500 + y
    z = y - b / 200

    def f_inv(t):
        if t ** 3 > 0.008856:
            return t ** 3
        else:
            return (t - 16 / 116) / 7.787

    x = 95.047 * f_inv(x)
    y = 100.000 * f_inv(y)
    z = 108.883 * f_inv(z)

    return x, y, z


def rgb_to_lab(r, g, b):
    x, y, z = rgb_to_xyz(r, g, b)
    return xyz_to_lab(x, y, z)

def lab_to_rgb(l, a, b):
    x, y, z = lab_to_xyz(l, a, b)
    return xyz_to_rgb(x, y, z)


def rgb_to_hsv(r, g, b):
    r, g, b = r / 255.0, g / 255.0, b / 255.0
    max_rgb = max(r, g, b)
    min_rgb = min(r, g, b)
    delta = max_rgb - min_rgb

    # Рассчет H (hue)
    if delta == 0:
        h = 0
    elif max_rgb == r:
        h = (60 * ((g - b) / delta) + 360) % 360
    elif max_rgb == g:
        h = (60 * ((b - r) / delta) + 120) % 360
    elif max_rgb == b:
        h = (60 * ((r - g) / delta) + 240) % 360

    # Рассчет S (saturation)
    if max_rgb == 0:
        s = 0
    else:
        s = (delta / max_rgb) * 100

    # Рассчет V (value)
    v = max_rgb * 100

    # Ограничиваем значения
    h = min(max(h, 0), 360)
    s = min(max(s, 0), 100) / 100
    v = min(max(v, 0), 100) / 100

    return round(h, 2), round(s, 2), round(v, 2)


def hsv_to_rgb(h, s, v):
    h = h % 360  # Убедимся, что h находится в диапазоне [0, 360]
    s = min(max(s / 100.0, 0), 1)  # Ограничиваем значение S между 0 и 1
    v = min(max(v / 100.0, 0), 1)  # Ограничиваем значение V между 0 и 1

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

    r = (r + m) * 255
    g = (g + m) * 255
    b = (b + m) * 255
    return round(r), round(g), round(b)
