from flask import jsonify
from db import cursor
from usuarios_carp.usuarios_im import usuarios_bd
from flask_jwt_extended import (
    get_current_user,
    get_jwt_identity,
    jwt_required
    
)

@usuarios_bd.route("/usuarios/<int:id_usuario>", methods=["GET"])
@jwt_required()
def usuarios_get(id_usuario):
    """
Obtener usuarios
---
tags: 
    - Usuarios
    - admin
security:
    - Bearer: []
parameters: 
    -   name: id_usuario
        in: path
        type: integer
        required: true
        description: Escriba el id a buscar
responses:
    200:
        description: Se ha encontrado el usuario de forma correcta
    400:
        description: Ha ocurrido algún error

"""
    id_user = get_jwt_identity()

    if int(id_user) != 1:
        return jsonify("Solo el admininstrador puede acceder"), 403

    try:
        script_verificar_id = """
        SELECT * FROM Usuarios WHERE id_usuario = ?
        """

        cursor.execute(script_verificar_id, (id_usuario,))

        usuario = cursor.fetchone()

        if usuario is None:
            return jsonify({"ERROR":"No se encontro el id"}), 404

        datos = {
            "nombre": usuario[1],
            "apellidos": usuario[2],
            "usuario": usuario[3]

        }
        return jsonify(datos), 200
    
    except Exception as e:
        return jsonify({"Error": str(e)}),500
        
