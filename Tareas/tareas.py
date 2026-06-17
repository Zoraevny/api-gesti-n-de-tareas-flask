from flask import Blueprint

tareas_bp = Blueprint("tareas", __name__)

from Tareas.obtener_tarea import *
from Tareas.create_tarea import *
from Tareas.actualizar import *
from Tareas.eliminar_tarea import *
from Tareas.estadisticas import *