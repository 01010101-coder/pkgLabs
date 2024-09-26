from flask import Flask

from app.main_page import main_bp

from app.vlad.main import vlad_main
from app.vlad.laba1 import vlad_laba1_bp
from app.vlad.laba2 import vlad_laba2_bp
from app.vlad.laba3 import vlad_laba3_bp

app = Flask(__name__)

app.register_blueprint(main_bp)

app.register_blueprint(vlad_laba1_bp)
app.register_blueprint(vlad_laba2_bp)
app.register_blueprint(vlad_laba3_bp)
app.register_blueprint(vlad_main)
