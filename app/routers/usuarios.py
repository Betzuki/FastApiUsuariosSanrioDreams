from fastapi import APIRouter, HTTPException
from app.database import get_conexion

#vamos a crear la variable para las rutas:
router = APIRouter(
    prefix="/usuarios",
    tags=["Usuarios"]
)

#endpoints: GET, GET, POST, PUT, DELETE, PATCH
@router.get("/")
def obtener_usuarios():
    try:
        cone = get_conexion()
        cursor = cone.cursor()
        cursor.execute("SELECT id_usuario, nombre_completo, correo, contrasenna, direccion, telefono, rol from USUARIO")
        usuarios = []
        for id_usuario, nombre_completo, correo, contrasenna, direccion, telefono, rol in cursor:
            usuarios.append({
                "id_usuario": id_usuario,
                "nombre_completo": nombre_completo,
                "correo": correo,
                "contrasenna":contrasenna,
                "direccion":direccion,
                "telefono":telefono,
                "rol":rol
            })
        cursor.close()
        cone.close()
        return usuarios
    except Exception as ex:
        raise HTTPException(status_code=500, detail=str(ex))

@router.get("/{id_buscar}")
def obtener_usuario(id_buscar: int):
    try:
        cone = get_conexion()
        cursor = cone.cursor()
        cursor.execute("SELECT nombre_completo, correo, contrasenna, direccion, telefono, rol FROM usuario WHERE id_usuario = :id_usuario"
                       ,{"id_usuario": id_buscar})
        usuario = cursor.fetchone()
        cursor.close()
        cone.close()
        if not usuario:
            raise HTTPException(status_code=404, detail="Usuario no encontrado")
        return {
            "id_usuario": id_buscar,
            "nombre_completo": usuario[0],
            "correo": usuario[1],
            "contrasenna": usuario[2],
            "direccion": usuario[3],
            "telefono": usuario[4],
            "rol": usuario[5]
        }
    except Exception as ex:
        raise HTTPException(status_code=500, detail=str(ex))

@router.post("/")
def agregar_usuario(id_usuario:str, nombre_completo:str, correo:str, contrasenna:str, direccion:str, telefono:str, rol:str):
    try:
        cone = get_conexion()
        cursor = cone.cursor()
        cursor.execute("""
            INSERT INTO usuario 
            VALUES(:id_usuario, :nombre_completo, :correo, :contrasenia, :direccion, :telefono, :rol)
        """,{"id_usuario":id_usuario, "nombre_completo":nombre_completo, "correo":correo, "contrasenna":contrasenna, "direccion":direccion,"telefono":telefono, "rol":rol})
        cone.commit()
        cursor.close()
        cone.close()
        return {"mensaje": "Usuario agregado con éxito"}
    except Exception as ex:
        raise HTTPException(status_code=500, detail=str(ex))

@router.put("/{id_actualizar}")
def actualizar_usuario(id_actualizar:str, nombre_completo:str, correo:str, contrasenna:str, direccion:str, telefono:str, rol:int):
    try:
        cone = get_conexion()
        cursor = cone.cursor()
        cursor.execute ("""
                UPDATE usuario
                SET nombre_completo = :nombre, correo = :correo, contrasenna = :contrasenna, direccion = :direccion, telefono = :telefono, rol = :rol
                WHERE id_usuario = :id_usuario
        """ , {"nombre_completo":nombre_completo, "correo":correo, "contrasenna":contrasenna, "direccion" :direccion, "telefono":telefono, "rol":rol, "id_usuario":id_actualizar})
        if cursor.rowcount==0:
            cursor.close()
            cone.close()
            raise HTTPException(status_code=404, detail="Usuario no encontrado")
        cone.commit()
        cursor.close()
        cone.close()
        return {"mensaje": "Usuario actualizado con éxito"}
    except Exception as ex:
        raise HTTPException(status_code=500, detail=str(ex))

@router.delete("/{id_eliminar}")
def eliminar_usuario(id_eliminar: str):
    try:
        cone = get_conexion()
        cursor = cone.cursor()
        cursor.execute("DELETE FROM usuario WHERE id_usuario = :id_usuario"
                       ,{"id_usuario": id_eliminar})
        if cursor.rowcount==0:
            cursor.close()
            cone.close()
            raise HTTPException(status_code=404, detail="Usuario no encontrado")
        cone.commit()
        cursor.close()
        cone.close()
        return {"mensaje": "Usuario eliminado con éxito"}
    except Exception as ex:
        raise HTTPException(status_code=500, detail=str(ex))


from typing import Optional

@router.patch("/{id_actualizar}")
def actualizar_parcial(id_actualizar:str, nombre_completo:Optional[str]=None, correo:Optional[str]=None, contrasenia:Optional[str]=None, direccion:Optional[str]=None, telefono:Optional[str]=None, rol:Optional[str]=None):
    try:
        if not nombre_completo and not correo:
            raise HTTPException(status_code=400, detail="Debe enviar al menos 1 dato")
        cone = get_conexion()
        cursor = cone.cursor()

        campos = []
        valores = {"id_usuario": id_actualizar}
        if nombre_completo:
            campos.append("nombre_completo = :nombre")
            valores["nombre_completo"] = nombre_completo
        if correo:
            campos.append("correo = :correo")
            valores["correo"] = correo
        if contrasenia:
            campos.append("contrasenna = :contrasenia")
            valores["contrasenna"]= contrasenia
        if direccion:
            campos.append("direccion = :direccion")
            valores["direccion"]= direccion
        if telefono:
            campos.append("telefono = :telefono")
            valores["telefono"] = telefono
        if rol:
            campos.append("rol = :rol")
            valores["rol"]= rol

        cursor.execute(f"UPDATE usuario SET {', '.join(campos)} WHERE id_usuario = :id_usuario"
                       ,valores)
        if cursor.rowcount==0:
            cursor.close()
            cone.close()
            raise HTTPException(status_code=404, detail="Usuario no encontrado")
        cone.commit()
        cursor.close()
        cone.close()        
        return {"mensaje": "Usuario actualizado con éxito"}
    except Exception as ex:
        raise HTTPException(status_code=500, detail=str(ex))
