from pydantic import BaseModel

class LoginInput(BaseModel):
    user: str
    password: str
