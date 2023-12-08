from fastapi import FastAPI, Request
from database_connection import insert_into_slice, insert_into_vms, list_slices_for_user, connect_db, disconnect_db
import random

app = FastAPI()
@app.on_event("startup")
async def startup():
    await connect_db()

@app.on_event("shutdown")
async def shutdown():
    await disconnect_db()


@app.post("/management/process_vms/")
async def process_vms(request: Request):
    payload = await request.json()
    print(payload)
    user_id = payload.get('user_id')    
    num_vms = payload.get('num_vms')
    topology = payload.get('topology')
    ram_vms = payload.get('ram')
    storage_vms = payload.get('storage')
    nro_cores_vms = payload.get('cores')
    
    worker = random.choice(['worker1', 'worker2', 'worker3'])
    worker_id = {'worker1': 1, 'worker2': 2, 'worker3': 3}[worker]
    
    last_slice_id = await insert_into_slice(
            topology, 
            num_vms, 
            ram_vms, 
            storage_vms, 
            nro_cores_vms, 
            worker_id, 
            user_id
        )
    
    await insert_into_vms(
        last_slice_id, 
        worker_id, 
        user_id, 
        ram_vms, 
        storage_vms, 
        nro_cores_vms, 
        num_vms
    )

    return {"status": f"VMs creadas para el usuario {user_id}",
            "payload_received": payload}

@app.post("/listSlices/")
async def list_slices(request: Request):
    payload = await request.json()
    user_id = payload.get('user_id')
    print(payload)
    
    # Llamada a la función para obtener los slices
    slices = await list_slices_for_user(user_id)
    for slice_ in slices:
        slice_.pop('usuario_idusuario', None)
        slice_.pop('workers_idworkers', None)
        slice_.pop('idSlice', None)
    
    return {"status": "Operación exitosa", "slices": slices}