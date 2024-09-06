from flask import Flask, request, jsonify, render_template
from colormath.color_objects import CMYKColor, LabColor, HSVColor, sRGBColor
from colormath.color_conversions import convert_color

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


# Преобразование CMYK в LAB и HSV
@app.route('/convert/cmyk', methods=['POST'])
def convert_cmyk():
    data = request.json
    c, m, y, k = float(data['c']), float(data['m']), float(data['y']), float(data['k'])

    cmyk = CMYKColor(c, m, y, k)
    rgb = convert_color(cmyk, sRGBColor)

    lab = convert_color(rgb, LabColor)
    hsv = convert_color(rgb, HSVColor)

    return jsonify({
        'cmyk': {'c': c, 'm': m, 'y': y, 'k': k},
        'lab': {'l': lab.lab_l, 'a': lab.lab_a, 'b': lab.lab_b},
        'hsv': {'h': hsv.hsv_h, 's': hsv.hsv_s, 'v': hsv.hsv_v}
    })

# Преобразование LAB в CMYK и HSV
@app.route('/convert/lab', methods=['POST'])
def convert_lab():
    data = request.json
    l, a, b = float(data['l']), float(data['a']), float(data['b_lab'])

    lab = LabColor(l, a, b)
    rgb = convert_color(lab, sRGBColor)

    cmyk = convert_color(rgb, CMYKColor)
    hsv = convert_color(rgb, HSVColor)

    return jsonify({
        'cmyk': {'c': cmyk.cmyk_c, 'm': cmyk.cmyk_m, 'y': cmyk.cmyk_y, 'k': cmyk.cmyk_k},
        'lab': {'l': l, 'a': a, 'b': b},
        'hsv': {'h': hsv.hsv_h, 's': hsv.hsv_s, 'v': hsv.hsv_v}
    })

# Преобразование HSV в CMYK и LAB
@app.route('/convert/hsv', methods=['POST'])
def convert_hsv():
    data = request.json
    h, s, v = float(data['h']), float(data['s']), float(data['v'])

    hsv = HSVColor(h, s, v)
    rgb = convert_color(hsv, sRGBColor)

    cmyk = convert_color(rgb, CMYKColor)
    lab = convert_color(rgb, LabColor)

    return jsonify({
        'cmyk': {'c': cmyk.cmyk_c, 'm': cmyk.cmyk_m, 'y': cmyk.cmyk_y, 'k': cmyk.cmyk_k},
        'lab': {'l': lab.lab_l, 'a': lab.lab_a, 'b': lab.lab_b},
        'hsv': {'h': h, 's': s, 'v': v}
    })

if __name__ == '__main__':
    app.run(debug=True)
