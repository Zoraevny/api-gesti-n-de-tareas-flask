from flask import Blueprint

auth_bp = Blueprint("auth", __name__, url_prefix="/auth")

from autho.refresh_token import *
from autho.login import *
from autho.logout import *
