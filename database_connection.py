from databases import Database
import time

database = Database("mysql://root:123456@127.0.0.1/cloud_basedatos")

async def connect_db():
    await database.connect()

async def disconnect_db():
    await database.disconnect()

async def verify_user(name: str, password: str):
    # Cambiamos la query para que coincida con las nuevas columnas
    query = "SELECT idUsuario, nombres, codigo, contraseña FROM usuario WHERE codigo = :name"
    
    user = await database.fetch_one(query, {"name": name})
    if user:
        user_dict = {
            "idUsuario": user[0],
            "nombres": user[1],
            "codigo": user[2],
            "contraseña": user[3],
        }
        if password == user_dict["contraseña"]:
            print(user_dict)  # Imprimir el objeto user completo
            return user_dict
        else:
            return None
    else:
        return None
async def insert_into_slice(topologia, nro_vms, ram_vms, storage_vms, nro_cores_vms, workers_idworkers, usuario_idusuario):
    query = """INSERT INTO slice (topologia, nro_vms, ram_vms, storage_vms, nro_cores_vms, workers_idworkers, usuario_idusuario) 
               VALUES (:topologia, :nro_vms, :ram_vms, :storage_vms, :nro_cores_vms, :workers_idworkers, :usuario_idusuario)"""
    
    values = {
        "topologia": topologia,
        "nro_vms": nro_vms,
        "ram_vms": ram_vms,
        "storage_vms": storage_vms,
        "nro_cores_vms": nro_cores_vms,
        "workers_idworkers": workers_idworkers,
        "usuario_idusuario": usuario_idusuario
    }
    
    await database.execute(query, values)
    last_record_id = await database.fetch_one("SELECT LAST_INSERT_ID()")
    return last_record_id[0]

async def insert_into_vms(slice_id, worker_id, user_id, ram_vms, storage_vms, nro_cores_vms, num_vms):
    query = """INSERT INTO vms (slice_idSlice, slice_workers_idworkers, slice_usuario_idusuario, 
                                ramVM, storageVM, nro_cores_VM, ip_VM) 
               VALUES (:slice_idSlice, :slice_workers_idworkers, :slice_usuario_idusuario, 
                       :ramVM, :storageVM, :nro_cores_VM, :ip_VM)"""
    
    values = {
        "slice_idSlice": slice_id,
        "slice_workers_idworkers": worker_id,
        "slice_usuario_idusuario": user_id,
        "ramVM": ram_vms,
        "storageVM": storage_vms,
        "nro_cores_VM": nro_cores_vms,
        "ip_VM": None
    }
    
    for _ in range(num_vms):
        await database.execute(query, values)

async def list_slices_for_user(user_id):
    # Consulta SQL para obtener las filas que hagan match con el user_id
    query = "SELECT * FROM slice WHERE usuario_idusuario = :user_id"
    
    # Ejecución de la consulta SQL
    rows = await database.fetch_all(query, {"user_id": user_id})
    
    # Transformar los resultados a un formato que puedas retornar como respuesta
    results = [dict(row) for row in rows]
    
    return results
