from flask import request, jsonify, render_template
from app.vlad.laba1.convertfunc import *

from . import laba1_bp


@laba1_bp.route('/')
def index():
    return render_template('index.html')


# Преобразование CMYK в LAB и HSV
@laba1_bp.route('/convert/cmyk', methods=['POST'])
def convert_cmyk():
    data = request.json
    c, m, y, k = float(data['c']), float(data['m']), float(data['y']), float(data['k'])

    # Конвертация CMYK в RGB
    r, g, b = cmyk_to_rgb(c, m, y, k)

    # Конвертация RGB в LAB
    l, a, b_lab = rgb_to_lab(r, g, b)

    # Конвертация RGB в HSV
    h, s, v = rgb_to_hsv(r, g, b)

    # Возвращаем результат в JSON формате
    return jsonify({
        'cmyk': {'c': c, 'm': m, 'y': y, 'k': k},
        'lab': {'l': l, 'a': a, 'b': b_lab},
        'hsv': {'h': h, 's': s, 'v': v}
    })


# Преобразование LAB в CMYK и HSV
@laba1_bp.route('/convert/lab', methods=['POST'])
def convert_lab():
    data = request.json
    l, a, b_lab = float(data['l']), float(data['a']), float(data['b_lab'])

    # Конвертация LAB в RGB
    r, g, b = lab_to_rgb(l, a, b_lab)

    # Конвертация RGB в CMYK
    c, m, y, k = rgb_to_cmyk(r, g, b)

    # Конвертация RGB в HSV
    h, s, v = rgb_to_hsv(r, g, b)

    # Возвращаем результат в JSON формате
    return jsonify({
        'cmyk': {'c': c, 'm': m, 'y': y, 'k': k},
        'lab': {'l': l, 'a': a, 'b': b_lab},
        'hsv': {'h': h, 's': s, 'v': v}
    })


# Преобразование HSV в CMYK и LAB
@laba1_bp.route('/convert/hsv', methods=['POST'])
def convert_hsv():
    data = request.json
    h, s, v = float(data['h']), float(data['s']), float(data['v'])

    # Конвертация HSV в RGB
    r, g, b = hsv_to_rgb(h, s, v)

    # Конвертация RGB в CMYK
    c, m, y, k = rgb_to_cmyk(r, g, b)

    # Конвертация RGB в LAB
    l, a, b_lab = rgb_to_lab(r, g, b)

    # Возвращаем результат в JSON формате
    return jsonify({
        'cmyk': {'c': c, 'm': m, 'y': y, 'k': k},
        'lab': {'l': l, 'a': a, 'b': b_lab},
        'hsv': {'h': h, 's': s, 'v': v}
    })

