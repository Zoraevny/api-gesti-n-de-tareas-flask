from flask import Blueprint

usuarios_bd = Blueprint("usuarios", __name__, url_prefix="/user")

from usuarios_carp.perfil_usuario import *
from usuarios_carp.usuario_crear import *
from usuarios_carp.obtener_usuario import *
from usuarios_carp.eliminar_usuario import *
from usuarios_carp.actualizar_usuario import *
