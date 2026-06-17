from flask import jsonify
from db import cursor
from usuarios_carp.usuarios_im import usuarios_bd
from flask_jwt_extended import(
    jwt_required,
    get_jwt_identity
)



@usuarios_bd.route("/perfil", methods=["GET"])
@jwt_required()
def perfil_get():
    """
    Perfil del usuario autenticado
    ---
    tags:
    - Usuarios

    security:
    - Bearer: []

    responses:
        200:
            description: Datos del usuario
            schema:
            properties:
                Id_usuario:
                    type: integer
                Nombre:
                    type: string
                Apellidos:
                    type: string
                Usuario:
                    type: string

        401:
            description: Token inválido o expirado
    """
    try:
        id_usuario = get_jwt_identity()

        script = """
        SELECT nombre, apellidos, usuario FROM Usuarios WHERE id_usuario = ?
        """

        cursor.execute(script, (id_usuario,))
        datos = cursor.fetchone()

        if datos is None:
            return jsonify({"Error": "Usuario no encontrado"}), 404


        return jsonify({
            "Id_usuario": id_usuario,
            "Nombre": datos[0],
            "Apellidos": datos[1],
            "Usuario": datos[2] 
        }), 200


    except Exception as e:
        return jsonify({"Error": str(e)}), 500