from flask import jsonify,request
from db import cursor, conexion
from proyectos.proyectos import proyectos_bp
from flask_jwt_extended import(
    jwt_required,
    get_jwt_identity
)


@proyectos_bp.route("/proyectos/<int:id_proyecto>", methods=["PUT"])
@jwt_required()

def proyectos_put(id_proyecto):
    """
Actualización de proyecto
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
        description: id del proyecto
        
    -   name: body
        in: body
        required: true
        schema: 
            type: object
            properties:
                nombre:
                    type: string
                    example: Nombre cambiado
                descripcion:
                    type: string
                    example: ejemplo de nueva descripción
responses:
    200:
        description: Se ha cambiado el proyecto correctamente
    400:
        description: Ha ocurrido un error
                


"""
    try:
        datos = request.get_json() or {}
        nombre = datos.get("nombre")
        descripcion = datos.get("descripcion")
        id_usuario = get_jwt_identity()

        if not all([id_proyecto, nombre, descripcion]):
            return jsonify({"Error": "Los campos no deben de estar vacíos"}), 400
        
        if not(len(nombre) > 3 and len(nombre) < 100):
            return jsonify({"Error": "El nombre del proyecto debe de tener entre 3 y 100 caracteres"}), 400

        if not(len(descripcion) >= 0 and len(descripcion) < 500):
            return jsonify({"Error": "El nombre del proyecto debe de tener entre 3 y 100 caracteres"}), 400

        script_verificacion = """
        SELECT * FROM Proyectos WHERE id_proyecto = ? and id_usuario = ?
        """
        cursor.execute(script_verificacion, (id_proyecto, id_usuario))
        fila = cursor.fetchone()
        if fila is None:
            return jsonify({"Error": "El id_proyecto del proyecto está mal"}), 400

        script_guardar = """
        UPDATE Proyectos SET nombre = ?, descripcion = ? WHERE id_usuario = ? and id_proyecto = ?
        """

        cursor.execute(script_guardar, (nombre, descripcion, id_usuario, id_proyecto))
        conexion.commit()

        return jsonify({"Correcto": "Se han guardado los datos correctamente"}), 200

    except Exception as e:
        return jsonify({"Error": str(e)}), 500