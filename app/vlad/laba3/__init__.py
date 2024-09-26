from flask import Blueprint

vlad_laba3_bp = Blueprint('laba3', __name__,
                     template_folder='templates',
                     static_folder='static',
                          )

from . import views
