from flask import jsonify
from autho.authorization import auth_bp
from flask_jwt_extended import (
    jwt_required,
    create_access_token,
    get_jwt_identity
)

@auth_bp.route("/refresh", methods=["POST"])
@jwt_required(refresh=True)
def refresh(): 
    """
Refresh token
---
tags:
    - Autenticación
security:
    - Bearer: []
responses:
    200:
        description: Refresh token
        schema:
        properties:
            access_token:
                type: string
    400:
        description: Algo ha salido mal

"""
    try:
        id_usuario = get_jwt_identity()

        nuevo_access_token = create_access_token(identity=id_usuario)

        return jsonify({
            "access_token": nuevo_access_token
        }), 200

    except Exception as e:
        return jsonify({"Error": str(e)}), 500
