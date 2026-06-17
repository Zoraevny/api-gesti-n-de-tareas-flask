from flask import request, jsonify
from db import cursor, conexion
from proyectos.proyectos import proyectos_bp
from flask_jwt_extended import (
    jwt_required,
    get_jwt_identity
)


@proyectos_bp.route("/proyectos", methods=["POST"])
@jwt_required()
def proyectos_post():
    """
Crear proyectos
---
tags:
    - Proyectos
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
                    example: Ejemplo proyecto
                descripcion:
                    type: string
                    example: Ejemplo de la descripción etc, etc
responses:
    200:
        description: Se ha añadido correctamente el proyecto
    400:
        description: Ha ocurrido un error

"""
    try:
        datos = request.get_json() or {}
        nombre =  datos.get("nombre")
        descripcion = datos.get("descripcion") 
        id_usuario = get_jwt_identity()

        if not all([nombre, descripcion]):
            return jsonify({"Error": "Los campos no pueden estar vacíos"}), 400

        if not(len(nombre) > 3 and len(nombre) < 100):
            return jsonify({"Error": "El nombre del proyecto debe de tener entre 3 y 100 caracteres"}), 400

        if not(len(descripcion) >= 0 and len(descripcion) < 500):
            return jsonify({"Error": "El nombre del proyecto debe de tener entre 3 y 100 caracteres"}), 400
        

        script_proyecto = """
        INSERT INTO Proyectos(nombre, descripcion, id_usuario) VALUES(?, ?, ?)
        """
        cursor.execute(script_proyecto, (nombre, descripcion, id_usuario))
        conexion.commit()

        return jsonify({"Correcto": "Los datos han sido guardados con éxito"}), 200



    except Exception as e:
        return jsonify({"Error": str(e)}), 500