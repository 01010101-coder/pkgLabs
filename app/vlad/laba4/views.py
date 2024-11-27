from flask import request, jsonify, render_template

from . import vlad_laba4_bp as laba4_bp


@laba4_bp.route('/vlad/laba4')
def index():
    return render_template('laba4/index.html')