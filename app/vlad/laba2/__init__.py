from flask import Blueprint

vlad_laba2_bp = Blueprint('laba2', __name__,
                     template_folder='templates',
                     static_folder='static',
                          )

from . import views
