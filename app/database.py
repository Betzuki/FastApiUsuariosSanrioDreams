import oracledb

def get_conexion():
    try:
        conexion = oracledb.connect(
            user="C##SanrioDreams",
            password="12345",
            dsn="localhost:1521/orcl"
        )
        return conexion
    except Exception as ex:
        raise Exception(f"Error al conectar a la base de datos: {ex}")
