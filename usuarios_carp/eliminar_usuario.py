from flask import jsonify
from db import conexion, cursor
from usuarios_carp.usuarios_im import usuarios_bd
from flask_jwt_extended import (
    jwt_required,
    get_jwt_identity
)

@usuarios_bd.route("/usuarios/<int:id_usuario>", methods=["DELETE"])
@jwt_required()
def usuarios_delete(id_usuario):
    """
Eliminar usuario ADMIN
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
        description: Escriba el id a eliminar
responses: 
    200:
        description: Se ha eliminado correctamente
    400:
        description: Ha ocurrido un error

"""
    try:

        id_user = get_jwt_identity()
        if int(id_user) != 1:
            return jsonify("Solo el administrador puede acceder"), 403

        if id_usuario is None:
            return jsonify({"Error": "Debe de escribir un id_usuario"}),400

        script = """
            DELETE FROM Usuarios WHERE id_usuario = ?
        """
        cursor.execute(script, (id_usuario,))

        if cursor.rowcount == 0:
            return jsonify({
                "Error": "Usuario no encontrado"
            }), 404 
        
        conexion.commit()
        return jsonify({"Verificado": "Se la eliminado con éxito"}),200
    
    
    except Exception as e:
        return jsonify({"Error": f"Error inesperado: {str(e)}"}), 500