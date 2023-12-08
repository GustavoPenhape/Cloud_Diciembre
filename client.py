import os
import getpass
import requests
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from prettytable import PrettyTable
from networkX_draw import draw_topology
import time

# Constantes globales
LOGO = """
"""


class UserSession:
    def __init__(self, user_id, nombre, rol):
        self.user_id = user_id
        self.nombre = nombre
        self.rol = rol

console = Console()

def clear_console():
    os.system('cls' if os.name == 'nt' else 'clear')

def display_login():
    clear_console()
    print(LOGO)
    console.print("[bold blue]Iniciar Sesión[/bold blue]")    
    user = input("Usuario: ")
    password = getpass.getpass("Contraseña: ")
    return user, password

def display_invalid_credentials_options():
    console.rule("[red]Credenciales inválidas[/red]", style="bold")
    console.print("""
        [bold]1)[/bold] Volver
        [bold]2)[/bold] Salir
    """)
    
    choice = input("Selecciona una opción: ")

    if choice == "1":
        return True
    elif choice == "2":
        return False
#
def display_interface():
    while True:
        user, password = display_login()
        #response = requests.post("http://10.20.10.10:9900/login/", json={"user": user, "password": password})
        response = requests.post("http://127.0.0.1:9900/login/", json={"user": user, "password": password})
        
        if response.status_code == 200:
            results = response.json()
            token = results.get('token', '')  # Asumiendo que el token está en la respuesta
            #print(f"Resultados: {results}")
            should_continue = True     
            while should_continue:  # Bucle interno para las opciones
                clear_console()
                print(f"Bienvenido {user}")
                print("¿Qué quieres hacer?")
                print("1. Listar Slices")
                print("2. Editar VMs")
                print("3. Crear Slices")
                print("4. Salir")
                choice = input("Selecciona una opción: ")
                headers = {'Authorization': f'Bearer {token}'}  # Agregar token al header
                                
                if choice == '1':
                    # Llamada a la API usando el token
                    response = requests.get("http://127.0.0.1:9900/listSlices/", headers=headers)
                    #response = requests.get("http://10.20.10.10:9900/listSlices/", headers=headers)

                    # Verificar que la respuesta sea 200 OK
                    if response.status_code == 200:
                        # Procesar respuesta
                        response_data = response.json()
                        slices = response_data.get('slices', [])
                        
                        # Crear una tabla
                        x = PrettyTable()

                        # Asumiendo que todos los diccionarios en `slices` tienen las mismas claves
                        if slices:
                            field_names = ['idSlice'] + list(slices[0].keys())  # Agregar 'idSlice' al inicio
                            x.field_names = field_names

                            for index, slice_ in enumerate(slices, start=1):  # Empezar el conteo desde 1
                                row_values = [index] + list(slice_.values())  # Agregar el 'idSlice'
                                x.add_row(row_values)
                        print(x)
                         # Pregunta para el usuario
                        # Pregunta al usuario si desea ver un slice en particular
                        while True:
                            see_slice = input("¿Deseas ver algún slice? (si/no): ")

                            # Si el usuario desea ver un slice
                            if see_slice.lower() == 'si':
                                slice_id = int(input("Ingresa el id del Slice: "))  # Convertir a entero

                                if slice_id > 0 and slice_id <= len(slices):  # Verificar que el ID sea válido y positivo
                                    selected_slice = slices[slice_id - 1]  # Asumimos que el slice_id comienza desde 1
                                    topology_type = selected_slice.get('topologia')
                                    num_vms = int(selected_slice.get('nro_vms'))  # Convertir a entero
                                    # Dibujar la topología
                                    draw_topology(topology_type, num_vms)
                                    print("******    Opciones    ******")
                                    print("1. Ver otro slice")
                                    print("2. Volver al menú principal")
                                    next_choice = input("Selecciona una opción: ")
                                    if next_choice == '2':
                                        break  # Salir del bucle interno y volver al menú principal
                                else:
                                    print("ID de Slice inválido. Debe ser un número positivo y dentro del rango de Slices disponibles.")
                                    time.sleep(3)
                            else:
                                break 

                    else:
                        print(f"Error: Received status code {response.status_code}")
                    should_continue = display_final_options()
                    if not should_continue:
                        print("Sesión cerrada.")  # Aquí puedes agregar el código para cerrar la sesión si lo necesitas
                        break  # Salir del bucle interno 

                elif choice == '2':
                    # Llamada a la API usando el token
                    response = requests.get("http://127.0.0.1:9900/opcion2/", headers=headers)
                    # Procesar respuesta
                elif choice == '3':  # Supongamos que la opción 3 es para crear VMs
                    print("---------------------------------")
                    num_vms = input("Número de VMs a crear: ")   
                    print("---------------------------------")
                    # Preguntar por la Memoria RAM para cada VM
                    ram = input("Cantidad de Memoria RAM en GB para cada VM: ")

                    # Preguntar por el Almacenamiento para cada VM
                    storage = input("Cantidad de Almacenamiento en GB para cada VM: ")

                    # Preguntar por los Cores para cada VM
                    cores = input("Número de Cores para cada VM: ")

                    while True:
                        available_options = available_topologies(int(num_vms))
                        print("Selecciona la topología:")

                        # Crear una nueva lista para almacenar las claves ordenadas
                        sorted_keys = sorted(available_options.keys(), key=lambda x: int(x))
                        
                        # Crear un diccionario de mapeo
                        mapping = {}
                        for index, key in enumerate(sorted_keys, 1):
                            mapping[str(index)] = key
                            print(f"{index}. {available_options[key]}")

                        topology_choice = input("Opción: ")
                        original_key = mapping.get(topology_choice, None)
                        topology = available_options.get(original_key, None)
                        if topology is not None:  # Si se seleccionó una opción válida, salir del bucle
                            break
                        else:
                            print("Opción no válida. Vuelve a intentarlo.")
                   
                    payload = {
                        "num_vms": int(num_vms),
                        "topology": topology,
                        "name_user": user,
                        "ram": ram,        # Añadido aquí
                        "storage": storage,  # Añadido aquí
                        "cores": cores      # Añadido aquí
                    }

                        #print(f"Enviando el siguiente JSON: {payload}")

                    # Aquí haces la solicitud POST para crear las VMs
                    #response = requests.post("http://127.0.0.1:9900/create_vms/", json=payload, headers=headers)
                    response = requests.post("http://10.20.10.10:9900/create_vms/", json=payload, headers=headers)

                    if response.status_code == 200:
                        server_response = response.json()
                        print(f"Respuesta del servidor: {server_response}")

                        # Extraer 'response_data' del JSON de respuesta del servidor
                        response_data = server_response.get("response_data", {})

                        # Extraer 'topology' de 'response_data'
                        received_topology = response_data.get("payload_received", {}).get("topology", None)

                        # Dibujar la topología aquí
                        if received_topology:
                            draw_topology(received_topology, int(num_vms))
                    else:
                        print(f"Error en la solicitud: {response.status_code}")
                    should_continue = display_final_options()
                    if not should_continue:
                        print("Sesión cerrada.")  # Aquí puedes agregar el código para cerrar la sesión si lo necesitas
                        break  # Salir del bucle interno
                elif choice == '4':
                    break  # Salir del bucle interno
        else:
            print("Credenciales inválidas. Inténtalo de nuevo.")
            if not display_invalid_credentials_options():
                break  # Salir del bucle si el usuario selecciona "Salir"

def display_final_options():
    while True:
        print("******    Opciones    ******")
        print("1. Volver al menú principal")
        print("2. Cerrar sesión")
        choice = input("Selecciona una opción: ")

        if choice == '1':
            return True  # True significa que el usuario quiere volver al menú principal
        elif choice == '2':
            return False  # False significa que el usuario quiere cerrar la sesión
        else:
            print("Opción inválida. Inténtalo de nuevo.")

def available_topologies(num_vms):
    topologies = {}
    
    # Para topología Lineal y Bus, siempre es posible
    topologies["1"] = "Lineal"
    topologies["5"] = "Bus"
    
    # Para Malla, verificar si el número es un cuadrado perfecto
    if int(num_vms ** 0.5) ** 2 == num_vms:
        topologies["2"] = "Malla"
    
    # Para Árbol, verificar si el número puede formar un árbol "casi completo"
    k = 0
    nodes = 0
    while nodes < num_vms:
        nodes += 2 ** k
        k += 1
    
    # Restricción para que Árbol solo aparezca si hay al menos 4 nodos
    if num_vms >= 4:
        topologies["3"] = "Árbol"
        
    # Para Anillo, siempre es posible si num_vms >= 3
    if num_vms >= 3:
        topologies["4"] = "Anillo"
    
    return topologies


# Punto de entrada
if __name__ == "__main__": 
    display_interface()
