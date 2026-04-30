from pydantic import BaseModel, SecretStr


class LoginCredential(BaseModel):
    login: int
    password: SecretStr
    server: str
    path: str | None = None


LoginCredentials = LoginCredential
