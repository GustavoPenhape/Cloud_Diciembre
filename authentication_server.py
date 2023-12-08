from fastapi import FastAPI, HTTPException
from clases import LoginInput
from token_manager import create_jwt
import database_connection
import time
app = FastAPI()

@app.on_event("startup")
async def startup():
    await database_connection.connect_db()

@app.on_event("shutdown")
async def shutdown():
    await database_connection.disconnect_db()
    
@app.post("/login/")
async def login(credentials: LoginInput):
    user = await database_connection.verify_user(credentials.user, credentials.password)
    
   
    if user:
        print(user)
     
        id_usuario = user["idUsuario"]
        nombre_usuario = user["nombres"]
        token = create_jwt(id_usuario)
        
        response_data = {
            "message": "Login exitoso",
            "user": {
                "idusuario": id_usuario,
                "name": nombre_usuario
            },
            "token": token
        }
        return response_data
    else:
        raise HTTPException(status_code=401, detail="Credenciales inválidas")
