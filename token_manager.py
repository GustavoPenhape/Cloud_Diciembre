import jwt
import datetime

SECRET_KEY = "GustavoCLOUD"

def create_jwt(user_id: int):  # Cambiado a int
    expiration = datetime.datetime.utcnow() + datetime.timedelta(hours=1)
    payload = {"user_id": user_id, "exp": expiration}
    token = jwt.encode(payload, SECRET_KEY, algorithm="HS256")
    return token
