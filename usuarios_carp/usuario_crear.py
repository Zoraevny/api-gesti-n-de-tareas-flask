from flask import request, jsonify
from db import cursor, conexion
from usuarios_carp.usuarios_im import usuarios_bd
from werkzeug.security import generate_password_hash



@usuarios_bd.route("/usuarios", methods=["POST"])
def usuarios_post():
    """
Crear usuario-register
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
                    example: Raúl
                apellidos:
                    type: string    
                    example: Lopéz Esparza
                usuario: 
                    type: string
                    example: color123
                contrasenia: 
                    type: string
                    example: sword_123
responses:
    200:
        description: Se ha creado su cuenta con éxito
    400:
        description: Algo ha salido mal
            
"""

    try: 
        datos =request.get_json() or {}
        nombre =datos.get("nombre")
        apellidos = datos.get("apellidos")
        usuario= datos.get("usuario")
        contrasenia = datos.get("contrasenia")

        if not all([nombre, apellidos, usuario, contrasenia]):
            return jsonify({"Error":"Los campos no pueden estar vacíos"}), 400
        
        if not(len(nombre) >2 and len(nombre) <= 50):
            return jsonify({"Error": "El nombre debe de tener entre 2 y 50 caracteres"}), 400
        
        if not(len(apellidos) > 2 and len(apellidos) < 100):
            return jsonify({"Error": "los apellidos debne de tener entre 2 y 100 caracteres"}), 400

        if not(len(usuario)> 4 and len(usuario) < 30):
            return jsonify({"Error": "El usuario debe de tener entre 4 y 30 caracteres"}), 400
                                    
        if not(len(contrasenia) > 8 and len(contrasenia) < 100):
            return jsonify({"Error": "La contraseña debe de tener entre 8 y 100 caracteres"}), 400



        hash_contrasenia = generate_password_hash(contrasenia)

        script_obtener = """
            SELECT * FROM Usuarios WHERE usuario = ?
        """
        cursor.execute(script_obtener, (usuario,))
        fila  = cursor.fetchone()
        if fila is not None:
            return jsonify("El usuario ya está elegido"), 400


        script = """
        INSERT INTO Usuarios(nombre, apellidos, usuario, contrasenia) 
        VALUES(?, ?, ?, ?)
        """

        cursor.execute(script, (nombre, apellidos, usuario, hash_contrasenia))
        conexion.commit()
        return jsonify({"respuesta": "Usuario añadido con exito"}), 201
    except Exception as e:
        return jsonify({"Error": f"Error del servidor: {str(e)}"})

