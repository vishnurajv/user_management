import uvicorn
from fastapi import FastAPI
from app.routers import users
from app.core.config import settings

app = FastAPI()


app.swagger_ui_init_oauth = {
    "usePkceWithAuthorizationCodeGrant": True,
    "clientId": settings.KEYCLOAK_CLIENT_ID,
    "clientSecret": settings.KEYCLOAK_CLIENT_SECRET,
}

app.include_router(users.router)

if __name__ == '__main__':
    uvicorn.run('app.main:app', host="127.0.0.1", port=8000)

    #uvicorn app.main:app --reload