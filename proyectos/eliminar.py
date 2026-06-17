from flask import jsonify
from db import cursor, conexion
from proyectos.proyectos import proyectos_bp
from flask_jwt_extended import (
    jwt_required,
    get_jwt_identity
)


@proyectos_bp.route("/proyectos/<int:id_proyecto>", methods=["DELETE"])
@jwt_required()
def proyectos_delete(id_proyecto):
    """
Eliminar proyecto
---
tags:
    - Proyectos
security: 
    - Bearer: []
parameters:
    -   name: id_proyecto
        in: path
        type: integer
        required: true
        description: id del proyecto a eliminar
responses:
    200: 
        description: Se ha eliminado el proyecto exitosamente
    400:   
        description: Ha ocurrido un error

"""
    try:
        id_usuario = get_jwt_identity()
        
        script_verificar = """
        SELECT * FROM Proyectos WHERE id_usuario = ? and id_proyecto = ?
        """
        cursor.execute(script_verificar, (id_usuario, id_proyecto))
        fila = cursor.fetchone()
        if fila is None:
            return jsonify({"Error": "El id_proyecto no es correcto"}), 400


        script = """
        DELETE FROM Proyectos WHERE id_proyecto = ? and id_usuario = ?
        """

        cursor.execute(script, (id_proyecto, id_usuario))
        conexion.commit()

        return jsonify({"Correcto": "Se ha eliminado correctamente"}), 200



    except Exception as e:
        return jsonify({"Error": str(e)}), 500
