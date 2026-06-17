from flask import jsonify
from autho.authorization import auth_bp
from flask_jwt_extended import (
    jwt_required,
    get_jwt
)
from db import cursor,  conexion



@auth_bp.route("/logout", methods=["DELETE"])
@jwt_required()
def logout():
    """
Logout
---
tags:
    - Autenticación
security:
    - Bearer: []
responses:
    200:
        description: Ha cerrado sesión de forma exitosa
    400:
        description: Algo ha salido mal

"""

    try:
        jti = get_jwt()["jti"]
        cursor.execute(
            "INSERT INTO tokensRevocados(jti) VALUES(?)",
            (jti,)
        )
    
        conexion.commit()
        return jsonify({
            "mensaje": "Token revocado"
        }), 200
    except Exception as e:
        return jsonify({"Error": str(e)}), 500