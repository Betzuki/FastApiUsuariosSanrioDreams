import oracledb

def get_conexion():
    conexion = oracledb.connect(
        user="SanrioDreams",
        password="12345",
        dsn="localhost:1521/XE"
    )
    return conexion

