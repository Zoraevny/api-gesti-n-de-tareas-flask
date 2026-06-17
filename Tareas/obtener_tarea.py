from flask import jsonify, request
from db import cursor
from Tareas.tareas import tareas_bp
import math
from flask_jwt_extended import (
    jwt_required,
    get_jwt_identity
)


def script_completado(completado, id_proyecto, buscar):
    script_conteo = """
        SELECT COUNT(*)
        FROM Tareas t
        JOIN Proyectos p ON t.id_proyecto = p.id_proyecto
        WHERE p.id_usuario = ?
        """
    
    if completado is not None:
        script_conteo += " AND t.completada = ?"
    
    if id_proyecto is not None:
        script_conteo += " AND p.id_proyecto = ?"

    if buscar  is not None:
        script_conteo += " and (t.titulo like ? or t.descripcion like ?)"
 
    return script_conteo


def script_filtro(completado, id_proyecto, buscar, orden = 'id_tarea', direccion = 'ASC'):
    
    script_paginacion = """
    SELECT t.id_tarea, t.titulo, t.descripcion, t.completada, t.created_at, t.updated_at from Tareas as t JOIN Proyectos as p ON p.id_proyecto = t.id_proyecto WHERE p.id_usuario = ?
        """

    if buscar is not None:
        script_paginacion += " and (t.titulo like ? or t.descripcion like ?)"

    if completado is not None:
        script_paginacion += " AND t.completada = ?"
        
    if id_proyecto is not None:
        script_paginacion += " AND p.id_proyecto = ?"


    script_paginacion+=  f" ORDER BY {orden} {direccion} OFFSET ? ROWS FETCH NEXT ? ROWS ONLY "

    return script_paginacion


@tareas_bp.route("/tareas", methods=["GET"])
@jwt_required()
def tarea_get():
    """
obtencion de tareas
---
tags:
    - Tareas
security:
    - Bearer: []
parameters:

    -   name: pagina
        in: query
        type: integer
        required: false
        default: 1

    -   name: limite
        in: query
        type: integer
        required: false
        default: 10

    -   name: completada
        in: query
        type: boolean
        required: false
        default: false

    -   name: buscar
        in: query
        type: string
        required: false
        
responses:
    200:
        description: Se ha insertado el valor exitosamente
    400:
        description: Ha ocurrido un errors

"""
    try:
        id_usuario = get_jwt_identity()
        pagina = int(request.args.get("pagina", 1))
        limite = int(request.args.get("limite", 10))
        completada = request.args.get("completada")
        id_proyecto = request.args.get("id_proyecto") 
        orden = request.args.get("orden", "id_tarea")
        buscar = request.args.get("buscar")
        direccion = "ASC"

        if id_proyecto is not None:
            try:
                id_proyecto = int(id_proyecto)
            except ValueError:
                return jsonify({
                    "Error": "id_proyecto debe ser un número"
                }), 400
        parametros = [id_usuario]

        if orden.startswith("-"):
            direccion = "DESC"
            orden = orden[1:]

        columnas_permitidas = {
            "id_tarea": "t.id_tarea",
            "titulo": "t.titulo",
            "completado": "t.completada"
        }
        if orden not in columnas_permitidas:
            return jsonify({"Error": "Ese orden no es válido"}), 400
        
        

        

        if completada is not None:
            completada = completada.lower()

            if completada == "true":
                completada = True
            elif completada == "false":
                completada = False
            else:
                return jsonify({
                    "Error": "El valor de completada debe ser true o false"
                }), 400


        if pagina < 1 or limite < 1:
            return jsonify({
                "Error": "Página y límite deben ser mayores que 0"
            }), 400
        
        if limite > 100:
            limite = 100

        offset = (pagina - 1)*limite


        valores_funcion = script_completado(completada, id_proyecto, buscar)
        if completada is not None:
            parametros.append(completada)
        if id_proyecto is not None:
            parametros.append(id_proyecto)
        if buscar is not None:
            palabra = f"%{buscar}%"
            parametros.append(palabra)
            parametros.append(palabra)

        cursor.execute(valores_funcion, parametros)
        conteo = cursor.fetchone()[0]
        if not conteo or conteo == 0:
            return jsonify({
                "pagina": pagina,
                "total_tareas": 0,
                "tareas": []
            }), 200


        if offset >= conteo and conteo > 0:
            return jsonify({"Error": "La paginación no puede ser mayor a la cantidad de tareas"}), 400
        
        parametros = [id_usuario]
        if buscar is not None:
            palabra = f"%{buscar}%"
            parametros.append(palabra)
            parametros.append(palabra)
        if completada is not None: parametros.append(completada)
        if id_proyecto is not None: parametros.append(id_proyecto)

        parametros.append(offset)
        parametros.append(limite)

        valores_funcion_filtro = script_filtro(completada, id_proyecto, buscar, orden, direccion)
        cursor.execute(valores_funcion_filtro, parametros)


        registros = cursor.fetchall()
        if not registros:
            return jsonify({"No hay tareas disponibles"}), 200
        datos = [{"pagina": pagina,
                "límite": limite,
                "total_tareas": conteo,
                "paginas": math.ceil(conteo/limite),}]
        for registro in registros:
            fila = {
                "tareas": {
                    "id": registro[0],
                    "titulo": registro[1],
                    "descripción": registro[2],
                    "completada": registro[3],
                    "fecha_creacion": registro[4],
                    "fecha_actualización": registro[5],

                }
            }

            datos.append(fila)

        

        return jsonify(datos), 200

    
    except Exception as e:
        return jsonify({"Error": str(e)}), 500
