from flask import request, jsonify
from db import cursor
from proyectos.proyectos import proyectos_bp
from flask_jwt_extended import (
    jwt_required,
    get_jwt_identity
)


@proyectos_bp.route("/proyectos", methods=["GET"])
@jwt_required()
def proyectossolo_get():
    """
Obtener proyectos
---
tags:
    - Proyectos
security:
    - Bearer: []
responses:
    200:
        description: Se obtuviero correctamente
    400:
        description: Ha ocurrido un error
        

"""

    try: 
        id_usuario = get_jwt_identity()
        script = """
            SELECT nombre, descripcion FROM Proyectos WHERE id_usuario = ?    
        """
        datos = []
        cursor.execute(script, (id_usuario,))
        registros = cursor.fetchall()
        for registro in registros:
            nuevo = {
                "nombre": registro[0],
                "Descripción": registro[1]
            }
            datos.append(nuevo)
        
        return jsonify(datos), 200


    except Exception as e:
        return jsonify({"Error": str(e)}), 500