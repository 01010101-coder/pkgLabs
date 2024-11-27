from flask import Blueprint

vlad_laba4_bp = Blueprint('laba4', __name__,
                     template_folder='templates',
                     static_folder='static',
                          )

from . import views
