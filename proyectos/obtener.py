from flask import jsonify
from db import cursor
from proyectos.proyectos import proyectos_bp
from flask_jwt_extended import(
    jwt_required,
    get_jwt_identity
)

@proyectos_bp.route("/proyectos/tareas", methods = ["GET"])
@jwt_required()
def proyectos_get():
    """
Obtener proyectos y sus tareas
---
tags: 
    - Proyectos
security: 
    - Bearer: []
responses:
    200:
        description: Se obtuvieron los datos correctamente
    400:
        description: Ha ocurrido un error

"""
    try: 
        id_usuario = get_jwt_identity()


        script = """
        SELECT p.nombre, p.descripcion, t.titulo, t.descripcion, t.completada FROM Proyectos as p JOIN Tareas as t ON p.id_proyecto = t.id_proyecto WHERE p.id_usuario = ?
        """

        cursor.execute(script, (id_usuario,))
        registros = cursor.fetchall()

        proyectos_dict = {}

        for registro in registros:
            nombre_proyecto = registro[0]
            desc_proyecto = registro[1]
            
            # Si el proyecto no está en nuestro diccionario, lo añadimos
            if nombre_proyecto not in proyectos_dict:
                proyectos_dict[nombre_proyecto] = {
                    "título": nombre_proyecto,
                    "descripcion": desc_proyecto,
                    "tareas": []
                }
            
            # Creamos el diccionario de la tarea actual
            tarea = {
                "titulo_tarea": registro[2],
                "Descripcion_tarea": registro[3],
                "completada": registro[4] 
            }
            
            # Agregamos la tarea al proyecto correspondiente
            proyectos_dict[nombre_proyecto]["tareas"].append(tarea)

        # Finalmente, convertimos el diccionario en la lista que necesitabas
        lista_final = list(proyectos_dict.values())
                    
        return jsonify(lista_final), 200
                        
    except Exception as e:
        return jsonify({"Error": str(e)}), 500