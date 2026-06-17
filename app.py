from flask import Flask
import secrets
from flasgger import Swagger

from autho.authorization import auth_bp
from Tareas.tareas import tareas_bp
from proyectos.proyectos import proyectos_bp
from usuarios_carp.usuarios_im import usuarios_bd
from flask_jwt_extended import JWTManager
from datetime import timedelta
from db import cursor

app = Flask(__name__)

swagger_template = {
    "swagger": "2.0",
    "info": {
        "title": "Api de gestion de tareas",
        "version": "1.0"
    },
    "securityDefinitions":{
        "Bearer": {
            "type": "apiKey",
            "name": "Authorization",
            "in": "header",
            "description": "Escribe: Bearer <token>"
        }
    }
}

swagger = Swagger(app, template=swagger_template)


app.config["JWT_SECRET_KEY"] = secrets.token_hex(32)
app.config['JSON_SORT_KEYS'] = False
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(minutes=30)
app.config["JWT_REFRESH_TOKEN_EXPIRES"] = timedelta(hours=1)

jwt = JWTManager(app)
@jwt.token_in_blocklist_loader
def verificar_token_revocado(jwt_header, jwt_payload):
    jti = jwt_payload["jti"]

    cursor.execute(
        'SELECT jti FROM tokensRevocados WHERE jti = ?'
    , (jti,))

    registro = cursor.fetchone()
    return registro is not None

app.register_blueprint(auth_bp)
app.register_blueprint(tareas_bp)
app.register_blueprint(usuarios_bd)
app.register_blueprint(proyectos_bp)


if __name__ == "__main__":
    app.run(debug=True)


