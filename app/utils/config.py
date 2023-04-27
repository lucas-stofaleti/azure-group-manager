from pydantic import BaseSettings


class Settings(BaseSettings):
    scope: str = ""
    domain: str = "http://localhost:8000"
    tenant_id: str
    app_id: str
    client_secret: str

    class Config:
        env_file = ".env"

settings = Settings()