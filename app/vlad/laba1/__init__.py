from flask import Blueprint

vlad_laba1_bp = Blueprint('laba1', __name__,
                     template_folder='templates',
                     static_folder='static',
                          )

from . import views
