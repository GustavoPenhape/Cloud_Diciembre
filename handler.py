from fastapi import FastAPI , HTTPException, Request, Depends

from clases import LoginInput  # Asegúrate de importar también LoginResponse
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import httpx
from threading import Thread
import time
from user_interface import display_authenticated_interface
import jwt
from jwt import ExpiredSignatureError

app = FastAPI()
security = HTTPBearer()

def verify_token(auth: HTTPAuthorizationCredentials = Depends(security)):
    token = auth.credentials
    try:
        payload = jwt.decode(token, "GustavoCLOUD", algorithms=["HS256"])
        return payload
    except ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expirado")
    except Exception as e:  # Puedes especificar más excepciones si lo deseas
        raise HTTPException(status_code=401, detail="Token inválido")

@app.post("/login/")
async def login(credentials: LoginInput):
    async with httpx.AsyncClient() as client:
        r = await client.post("http://127.0.0.1:9600/login/", json=credentials.dict())
    if r.status_code == 200:
        user_data = r.json()
        print(f"Debug: user_data antes de llamar a display_authenticated_interface: {user_data}")
        print(f"Token: {user_data['token']}")  # Imprime el token en la consola
        display_authenticated_interface(user_data['user'])  # Llama a la función con el sub-diccionario 'user'
        return {"status": "Success", "token": user_data['token']}
    else:
        raise HTTPException(status_code=401, detail="Credenciales inválidas")
    
@app.post("/create_vms/")
async def create_vms(request: Request, payload: dict = Depends(verify_token)):
    user_id = payload.get("name_user")  # Suponiendo que el user_id está en el payload del token
    print(f"User ID: {user_id}")
    print(f"Payload completo: {payload}") 

    original_payload = await request.json()
    
    # Mezcla los dos diccionarios
    merged_payload = {**original_payload, **payload}
    
    print(f"Payload combinado: {merged_payload}")
    
    async with httpx.AsyncClient() as client:
        r = await client.post("http://127.0.0.1:9700/management/process_vms/", json=merged_payload)
    
    if r.status_code == 200:
        response_data = r.json()
        payload_received = response_data.get("payload_received", {})
        num_vms_created = payload_received.get("num_vms", "desconocido")
        
        # Combina 'status' y 'response_data' en un solo JSON
        combined_response = {
            "status": f"Se ha creado correctamente sus {num_vms_created} VMs",
            "response_data": response_data
        }
        return combined_response
    else:
        return {"status": "Error en la creación de VM"}
    
@app.get("/listSlices/")
async def list_slices(request: Request, payload: dict = Depends(verify_token)):
    async with httpx.AsyncClient() as client:
        r = await client.post("http://127.0.0.1:9700/listSlices/", json=payload)
        
    if r.status_code == 200:
        response_data = r.json()
        print(response_data)
        return response_data  # Reenviando la respuesta del servicio en 9700
    else:
        return {
            "status": "Error al listar slices",
        }