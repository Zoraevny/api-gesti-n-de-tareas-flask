from flask import request, jsonify
from db import conexion, cursor
from proyectos.proyectos import proyectos_bp
from flask_jwt_extended import (
    jwt_required,
    get_jwt_identity
)


@proyectos_bp.route("/proyectos/<int:id_proyecto>/tarea", methods=["POST"])
@jwt_required()
def proyectos_tareas(id_proyecto):
    """
Creación de tarea-proyecto
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
        description: escriba el id del proyecto a añadir la tarea

    -   name: body
        in: body
        required: true
        schema: 
            type: object
            properties:
                titulo:
                    type: string
                    example: nombre titulo
                descripcion:
                    type: string
                    example: ejemplo de la descripción de la tarea
                completada:
                    type: boolean
                    example: false
responses:
    200:
        description: Se ha añadido la tarea correctamente
    400: 
        description: Ha ocurrido un error
                
"""

    try:
        datos = request.get_json() or {}
        titulo = datos.get("titulo")
        descripcion = datos.get("descripcion")
        completada = datos.get("completada")
        id_usuario = get_jwt_identity()

        if not all([titulo, descripcion]):
            return jsonify({"Error": "Los campos titulo o descripción no deben de estar vacíos"}), 400

        if completada is None:
            return jsonify({"Error": "Completada no debe de estar vacía"}), 400

        script_verificar = """
        SELECT * FROM Proyectos WHERE id_proyecto = ? and id_usuario = ?
        """
        cursor.execute(script_verificar, (id_proyecto, id_usuario))
        fila = cursor.fetchone()
        if fila is None:
            return jsonify({"Error": "No existe ese proyecto"}), 400

        script_insertar = """
        INSERT INTO Tareas(titulo, descripcion, completada, id_proyecto, created_at, updated_at) VALUES(?, ?, ?, ?, GETDATE(), GETDATE())
        """

        cursor.execute(script_insertar, (titulo, descripcion, completada, id_proyecto))
        conexion.commit()

        return jsonify({"Correcto": "Se ha insertado la tarea correctamente"}), 200

    except Exception as e:
        return jsonify({"Error": str(e)}), 500