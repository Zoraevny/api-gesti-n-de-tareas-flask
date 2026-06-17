from flask import request, jsonify
from Tareas.tareas import tareas_bp
from db import  conexion, cursor
from flask_jwt_extended import(
    jwt_required,
    get_jwt_identity
)





@tareas_bp.route("/tarea", methods=["POST"])
@jwt_required()
def tarea_post():
    """
Creación de tarea
---
tags:
    - Tareas

security:
    - Bearer: []

parameters:
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
        description: Se ha añadido correctamente
    400:
        description: Ha ocurrido un error al insertar

"""
    
    
    try:
        datos = request.get_json() or {}
        titulo = datos.get("titulo")
        descripcion = datos.get("descripcion")
        completada = datos.get("completada")
        id_proyecto = datos.get("id_proyecto")

        if not titulo or not descripcion or not id_proyecto:
            return jsonify({
                "Error": "id_proyecto, Título y descripción no pueden estar vacíos"
            }), 400

        if completada is None:
            return jsonify({
                "Error": "Debe indicar si se ha completado la tarea o no"
            }), 
    
        if not(len(titulo) >3 and len(titulo) < 100 ):
            return jsonify({"Error": "El título debe de tener entre 3 y 100 caracteres"}), 400
    
        if not(len(descripcion) >= 0 and len(descripcion) < 1000 ):
            return jsonify({"Error": "El título debe de tener entre 3 y 100 caracteres"}), 400

        
        script= """
            INSERT INTO Tareas(titulo, descripcion, completada, id_proyecto) VALUES(?,?,?,?)
        """

        cursor.execute(script, (titulo, descripcion, completada, id_proyecto))
        conexion.commit()

        return jsonify({"Guardado": "Se ha almacenado correctamente"}), 201

        


    except Exception as e:
        return jsonify({"Error": str(e)}), 500