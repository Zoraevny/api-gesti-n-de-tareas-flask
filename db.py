import pyodbc


try:
    conexion = pyodbc.connect(
    'DRIVER={ODBC Driver 17 for SQL Server};'
    'SERVER=localhost;'
    'DATABASE=EjemploCRUD;'
    'Trusted_Connection=yes;'
    )

    cursor = conexion.cursor()
    script_table = """
    IF NOT EXISTS (SELECT * FROM sysobjects WHERE name = 'Usuarios' and xtype='U')
    BEGIN
        CREATE TABLE Usuarios(
        id_usuario INT PRIMARY KEY NOT NULL IDENTITY(1,1),
        nombre VARCHAR(50) NOT NULL,
        apellidos VARCHAR(100) NOT NULL,
        usuario VARCHAR(50) NOT NULL,
        contrasenia VARCHAR(MAX) NOT NULL
        )
    END
    """

    cursor.execute(script_table)

    conexion.commit()

    script_table_tokens = """
    IF NOT EXISTS(SELECT * FROM sysobjects WHERE name = 'tokensRevocados' and xtype='U')
    BEGIN
        CREATE TABLE tokensRevocados(
        id_token INT PRIMARY KEY IDENTITY(1,1),
        jti varchar(50) NOT NULL
        )
    END
    """

    cursor.execute(script_table_tokens)
    conexion.commit()

    script_proyectos = """
    IF NOT EXISTS (SELECT * FROM sysobjects WHERE name= 'Proyectos' and xtype = 'U')
    BEGIN
        CREATE TABLE Proyectos (
        id_proyecto INT PRIMARY KEY NOT NULL IDENTITY(1,1),
        nombre VARCHAR(100) NOT NULL,
        descripcion VARCHAR(MAX) NOT NULL,
        id_usuario INT NOT NULL,
        FOREIGN KEY (id_usuario) REFERENCES Usuarios(id_usuario)
        )
    END
    """

    cursor.execute(script_proyectos)
    conexion.commit()



    script_tareas = """
    IF NOT EXISTS (SELECT * FROM sysobjects WHERE name = 'Tareas' and xtype = 'U')
    BEGIN
        CREATE TABLE Tareas(
        id_tarea INT PRIMARY KEY IDENTITY(1,1) NOT NULL,
        titulo VARCHAR(50) NOT NULL,
        descripcion TEXT NOT NULL,
        completada BIT NOT NULL,
        id_proyecto INT NOT NULL,
        FOREIGN KEY (id_proyecto) REFERENCES Proyectos(id_proyecto) ON DELETE CASCADE
        )
    END
    """
    cursor.execute(script_tareas)
    conexion.commit()






except Exception as e:
    print(f"Ocurrio un error: {e}")

