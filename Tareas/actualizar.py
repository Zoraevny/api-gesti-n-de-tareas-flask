from flask import request, jsonify
from db import conexion, cursor
from Tareas.tareas import tareas_bp
from flask_jwt_extended import (
    jwt_required,
    get_jwt_identity
)


@tareas_bp.route("/tareas/<int:id_tarea>", methods = ["PUT"])
@jwt_required()
def tarea_put(id_tarea):
    """
Actualizar tarea
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
    description: ID de la tarea a actualizar

-   name: body
    in: body
    required: true
    schema:
        type: object
        required:
            - titulo
            - descripcion
            - completada
            - id_proyecto
        properties:
            titulo:
                type: string
                example: Tarea nueva
            descripcion: 
                type: string
                example: Descripción de la tarea nueva
            completada:
                type: boolean
                example: False
            id_proyecto:
                type: integer
                example: 1
responses:
    200: 
        description: Se ha actualizado correctamente
    400: 
        description: Ha ocurrido un error


"""
    try:
        datos = request.get_json() or {}
        titulo = datos.get("titulo")
        descripcion = datos.get("descripcion")
        completada = datos.get("completada")
        id_proyecto = datos.get("id_proyecto")

        if not titulo or not descripcion or not id_proyecto:
            return jsonify({
                "Error": "Título y descripción no pueden estar vacíos"
            }), 400

        if completada is None:
            return jsonify({
                "Error": "Debe indicar si está completada"
            }), 400

        script_validacion = """
        SELECT p.id_usuario FROM Tareas as t JOIN Proyectos as p ON p.id_proyecto = t.id_proyecto WHERE t.id_tarea = ? and p.id_proyecto =? 

        """

        cursor.execute(script_validacion, (id_tarea, id_proyecto))
        fila = cursor.fetchone()
        if fila is None:
            return jsonify({"Error": "Id no es valido para actualizar"}), 404


        script = """
        UPDATE Tareas SET
        titulo = ?, descripcion = ?, completada = ?, updated_at = GETDATE() WHERE id_tarea = ? 
        """

        cursor.execute(script, (titulo, descripcion,completada, id_tarea))
        conexion.commit()
        return jsonify({"Correcto": "Se ha almacenado correctamente"}), 200

    except Exception as e:
        return jsonify({"Error": str(e)}), 500
