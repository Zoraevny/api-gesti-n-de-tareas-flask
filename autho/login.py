from flask import request, jsonify
from db import cursor
from autho.authorization import auth_bp
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token
)
from werkzeug.security import check_password_hash

@auth_bp.route("/login", methods = ["POST"])
def login():
    """
Inicio de sesión
---
tags:
  - Autenticación
consumes:
  - application/json
parameters:
  - name: body
    in: body
    required: true
    schema:
      type: object
      required:
        - usuario
        - contrasenia
      properties:
        usuario:
          type: string
          example: Lyn
        contrasenia:
          type: string
          example: Python_Lover
responses:
  200:
    description: Login exitoso
  401:
    description: Usuario o contraseña incorrectos
"""
    try:
        datos = request.get_json() or {}
        usuario = datos.get("usuario")
        contrasenia = datos.get("contrasenia")

        if not all([usuario, contrasenia]):
            return jsonify({"Error": "Los campos no pueden estar vacíos"}), 400
        
        script = """
        SELECT id_usuario, contrasenia FROM Usuarios WHERE usuario= ?  
        """

        cursor.execute(script, (usuario,))
        registro = cursor.fetchone()
        if registro is None:
            return jsonify({"Error":"Usuario o contraseña incorrectas"}), 401
        
        
        if not check_password_hash(registro[1], contrasenia):
            return jsonify({"Error": "Usuario o contraseña incorrectas"}), 401
        
        access_token = create_access_token(identity=str(registro[0]))
        refresh_token = create_refresh_token(identity=str(registro[0]))
        return jsonify({
            "mensaje": "Login correcto",
            "token": access_token,
            "refresh_token": refresh_token
        }), 200
            

    except Exception as e:
        return jsonify({"Error": str(e)}), 500