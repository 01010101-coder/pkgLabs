from flask import Blueprint

vlad_main = Blueprint('vlad_main',
                      __name__,
                      template_folder='templates',
                      url_prefix='/vlad')

from . import routes
