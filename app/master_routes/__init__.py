from flask import Blueprint

bp = Blueprint('master', __name__, )

from app.master_routes import routes

