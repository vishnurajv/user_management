
from typing import List, Union

from pydantic import AnyHttpUrl, validator, BaseSettings


class Settings(BaseSettings):
    PROJECT_NAME: str
    PROJECT_VERSION: str
    BACKEND_CORS_ORIGINS: List[AnyHttpUrl] = []

    @validator("BACKEND_CORS_ORIGINS", pre=True)
    def assemble_cors_origins(cls, v: Union[str, List[str]]) -> Union[List[str], str]:
        if isinstance(v, str) and not v.startswith("["):
            return [i.strip() for i in v.split(",")]
        elif isinstance(v, (list, str)):
            return v
        raise ValueError(v)

    SECRET_KEY: str

    KEYCLOAK_SERVER_URL: str
    KEYCLOAK_CALLBACK_URI: str
    KEYCLOAK_CLIENT_ID: str
    KEYCLOAK_CLIENT_SECRET: str
    KEYCLOAK_ADMIN_CLIENT_SECRET: str
    KEYCLOAK_REALM: str

    class Config:
        case_sensitive = True
        env_file = ".env"


settings = Settings()
