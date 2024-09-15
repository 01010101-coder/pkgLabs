from flask import render_template
from . import vlad_main as main

@main.route('/')
def index():
    return render_template('main/index.html')
