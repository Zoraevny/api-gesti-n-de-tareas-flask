from app import app, request, jsonify

@app.route("/login", methods=["POST"])
def login():
    usuario = request.json.get("usuario")
    password = request.json.get("password")

    if usuario is None or password is None:
        return jsonify({"Error": "Faltan datos"}), 400
    elif usuario == 'admin' and password == '1234':
        return jsonify({"respuesta": "Acceso concedido"}), 200


    
    return jsonify({"respuesta":"Acesso denegado"}), 401



