from rich.console import Console

console = Console()

def display_authenticated_interface(user_session):
    if "idusuario" in user_session and "name" in user_session:
        console.print(f"Bienvenido {user_session['name']}, tu id es {user_session['idusuario']}")
    else:
        console.print("Error: Los campos 'idusuario' y 'name' no están presentes en el diccionario.")