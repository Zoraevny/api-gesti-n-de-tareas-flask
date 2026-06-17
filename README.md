# API GESTIÓN DE TAREAS FLASK

# ARCHIVOS
## Carpeta autho
### authorization
El archivo contiene todas las importaciones para los demas archivos de la misma carpeta

### login
El archivo funciona para que te dé un token para el cual puedas acceder a las demás opciones

### logout
El archivo funciona para cerrar sesión y eliminar el token

### refresh_token
El archivo te da un nuevo token para acceder usando el token_refresh que te da el login

## Carpeta proyectos
### proyectos
Un archivo que contiene todas las importaciones usadas en los archivos de la misma carpeta

### crear_proyecto
Su función es crear un proyecto a partir del id del usuario

### actualizar 
Su función es añadir nuevos datos y  actualizar los datos antes colocados al crear el proyecto

### crear_tarea_proyecto
Su función es crear una tarea directamente desde el projecto y no por separado

### obtener_proyectos
La función es solo dar los proyectos existentes del usuario

### obtener_proyectos
La función es dar tanto los proyectos junto con todas las tareas que contiene cada una

### eliminar
Elimina el proyecto generado por el usuario

## Tareas
### tareas
El archivo contiene todas las importaciones que usan los archivos de la misma carpeta

### create_tarea
El archivo crea una tarea, pero es como añadirla fuera del proyecto

### actualizar
El archivo actualiza los nuevos valores a los datos ya colocados

### eliminar_tarea
El archivo elimina una tarea de un respectivo proyecto

### obtener_tarea
El archivo me da todas las taras de un proyecto

### estadisticas
Me envía toda la información que contiene un proyecto (cantidad de tareas, cantidad de tareas completadas, etc)



# TECNOLOGÍAS
- Python
- Flask
- Swagger
- SQL SERVER
- GIT 
- GITHUB

# Archivo principal 
- app.py



