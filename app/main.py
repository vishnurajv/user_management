import uvicorn
from fastapi import FastAPI
from app.routers.v1 import users
from app.core.config import settings

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.PROJECT_VERSION
)


app.swagger_ui_init_oauth = {
    "usePkceWithAuthorizationCodeGrant": True,
    "clientId": settings.KEYCLOAK_CLIENT_ID,
    "clientSecret": settings.KEYCLOAK_CLIENT_SECRET,
}

app.include_router(users.router, prefix="/v1")
app.include_router(users.router, prefix="/latest")

if __name__ == '__main__':
    uvicorn.run('app.main:app', host="127.0.0.1", port=8000)

    #uvicorn app.main:app --reload