from flask import jsonify
from db import cursor, conexion
from Tareas.tareas import tareas_bp
from flask_jwt_extended import (
    jwt_required, 
    get_jwt_identity
)


@tareas_bp.route("/tareas/<int:id_tarea>", methods=["DELETE"])
@jwt_required()
def tarea_delete(id_tarea):
    """
Eliminar tarea
---
tags: 
    - Tareas
security:
    - Bearer: []
parameters:
    -   name: id_tarea
        in: path
        type: integer
        required: true
        description: id de la tarea a eliminar

responses:
    200:
        description: Se ha eliminado correctamente
    400:
        description: Ha habido algún error al eliminar
"""


    try:
        id_usuario = get_jwt_identity()
        script_validacion = """
        SELECT id_tarea FROM Tareas as t JOIN Proyectos as p ON t.id_proyecto = p.id_proyecto WHERE id_tarea = ? and id_usuario = ?
        """
        cursor.execute(script_validacion, (id_tarea, id_usuario))
        fila = cursor.fetchone()
        if  fila is None:
            return jsonify({"Error": "Id no válido para eliminar tarea"}), 404

        script = """
        DELETE FROM Tareas WHERE id_tarea = ?
        """
        cursor.execute(script, (id_tarea,))
        conexion.commit()

        return jsonify({"Correcto": "Se ha eliminado correctamente la tarea"}), 200
        

    except Exception as e:
        return jsonify({"Error": str(e)}), 500
    