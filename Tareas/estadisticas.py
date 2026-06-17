from flask import jsonify
from db import cursor
from Tareas.tareas import tareas_bp
from flask_jwt_extended import (
    jwt_required,
    get_jwt_identity
)


@tareas_bp.route("/estadisticas", methods=["GET"])
@jwt_required()
def estadisticas_get():
    """
    Estadísticas del usuario
    ---
    tags:
        - Estadísticas
    security:
        - Bearer: []

    responses: 
        200:
            description: Estadísticas generales
            schema:
                properties:
                    Tareas_totales:
                        type: integer
                    Tareas_completadas:
                        type: integer
                    Tareas_incompletas:
                        type: integer
                    Porcentaje: 
                        type: number
                    Cantidad_proyectos:
                        type: integer
        400:
            description: Algo ha salido mal
    
    
    """

    try:
        id_usuario = get_jwt_identity()

        script_proyectos_totales = """
        SELECT COUNT(*) FROM Proyectos WHERE id_usuario = ?
        """

        cursor.execute(script_proyectos_totales, (id_usuario, ))
        proyecto_dato = cursor.fetchone()[0]
        if proyecto_dato == 0:
            return jsonify({"Sin proyecto": "Todavía no tiene un proyecto"}), 200


        script_tareas_totales = """
        SELECT COUNT(*) FROM Tareas as t JOIN Proyectos as p ON p.id_proyecto = t.id_proyecto WHERE p.id_usuario = ?
        """
        cursor.execute(script_tareas_totales, (id_usuario,))

        tareas_totales = cursor.fetchone()[0]

        if tareas_totales == 0:
            return jsonify({
                "tareas_totales": 0,
                "tareas_completadas": 0,
                "tareas_no_completas": 0
            }), 200

        script_tareas_completadas = """
        SELECT COUNT(*) FROM Tareas as t JOIN Proyectos as p ON p.id_proyecto = t.id_proyecto WHERE p.id_usuario = ? AND t.completada = 1
        """
        cursor.execute(script_tareas_completadas, (id_usuario,))
        tareas_completadas = cursor.fetchone()[0]

        porcentaje = 0
        if tareas_completadas == 0:
            porcentaje = 0
        else:
            porcentaje = (tareas_completadas/tareas_totales)* 100
            

        

        return jsonify({
            "tareas_totales": tareas_totales,
            "tareas_completadas": tareas_completadas,
            "tareas_no_completas": tareas_totales-tareas_completadas,
            "porcentaje": porcentaje,
            "Cantidad_proyectos": proyecto_dato

        }), 200



    except Exception as e:
        return jsonify({"Error": str(e)}), 500