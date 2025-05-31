import oracledb

def get_conexion():
    conexion = oracledb.connect(
        user="C##SanrioDreams",
        password="12345",
        dsn="localhost:1521/orcl"
    )
    return conexion

