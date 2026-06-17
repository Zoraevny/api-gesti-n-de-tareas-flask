from flask import Blueprint

proyectos_bp = Blueprint("proyectos", __name__, url_prefix="/proyectos")

from proyectos.crear_proyecto import *
from proyectos.crear_tarea_proyecto import *
from proyectos.actualizar import *
from proyectos.obtener_proyectos import *
from proyectos.obtener import *
from proyectos.eliminar import *