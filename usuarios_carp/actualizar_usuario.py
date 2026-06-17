from flask import request, jsonify
from db import conexion, cursor
from usuarios_carp.usuarios_im import usuarios_bd
from flask_jwt_extended import (
    jwt_required,
    get_jwt_identity
)


@usuarios_bd.route("/usuarios", methods=["PUT"])
@jwt_required()
def usuarios_put():
    """
Actualizar datos de usuario
---
tags:
    - Usuarios
security:
    - Bearer: []
parameters:
    -   name: body
        in: body
        required: true
        schema:
            type: object
            properties:
                nombre:
                    type: string
                    example: Rosa
                apellidos:
                    type: string
                    example: García Rui
responses:
    200:
        description: Se ha actualizado correctamente
    400:
        description: Ha ocurrido un error
"""

    try:
        id_user = get_jwt_identity()
        datos = request.get_json() or {}
        
        nombre = datos.get("nombre")
        apellidos = datos.get("apellidos") 

        if not nombre or not apellidos:
            return jsonify({"Error": "Los campos 'nombre' y 'apellidos' son obligatorios para actualizar"}), 400
            
        
        if not(len(nombre) >2 and len(nombre) <= 50):
            return jsonify({"Error": "El nombre debe de tener entre 2 y 50 caracteres"}), 400
        
        if not(len(apellidos) > 2 and len(apellidos) < 100):
            return jsonify({"Error": "los apellidos debne de tener entre 2 y 100 caracteres"}), 4000


        script = """
            UPDATE Usuarios 
            SET nombre = ?, apellidos = ? 
            WHERE id_usuario = ?
        """
        
        cursor.execute(script, (nombre, apellidos, id_user))

        if cursor.rowcount == 0:
            return jsonify({"Error": "No se encontro el ID"}), 404

        conexion.commit()
        
        return jsonify({"Validado": "El cambio ha sido exitoso"}), 200
    
    except Exception as e:
        return jsonify({"Error": f"El error es: {str(e)}"}), 500
