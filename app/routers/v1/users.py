from fastapi import APIRouter, Body
from app.services.custom_fastapi_keycloak import CustomFastAPIKeycloak
from fastapi import Depends, HTTPException, status, Request
from fastapi_keycloak import OIDCUser, UsernamePassword
from app.models.users import KeycloakUser, PartialKeycloakUser, PasswordData, CreateUserData
from app.core.config import settings
from typing_extensions import Annotated

idp = CustomFastAPIKeycloak(
    server_url=settings.KEYCLOAK_SERVER_URL,
    client_id=settings.KEYCLOAK_CLIENT_ID,
    client_secret=settings.KEYCLOAK_CLIENT_SECRET,
    admin_client_secret=settings.KEYCLOAK_ADMIN_CLIENT_SECRET,
    realm=settings.KEYCLOAK_REALM,
    callback_uri=settings.KEYCLOAK_CALLBACK_URI
)

async def authorize_user_or_admin(
    request: Request,
    user = Depends(idp.get_current_user(extra_fields=['permissionLevel'])),
):
    user_id = request.path_params.get('user_id')
    if not user_id:
        body = await request.json()
        user_id = (body.get('id') or body.get('user_id'))
    if user.extra_fields['permissionLevel'] == "Admin":
        return user
    elif user_id == user.sub:
        if body.get('attributes') and body.get('attributes').get('permissionLevel') != user.extra_fields.get('permissionLevel'):
            raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="Only admin has permission to update permissionLevel",
                )
        else:
            return user
    else:
        raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Only admin or same user is permitted to do this action",
            )

async def authorize_admin(
    request: Request,
    user = Depends(idp.get_current_user(extra_fields=['permissionLevel'])),
):
    if user.extra_fields['permissionLevel'] == "Admin":
        return user
    else:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only admin is permitted to do this action",
        )

router = APIRouter()

@router.get("/user/{user_id}", tags=["user-management"])
def get_user(user_id: str = None):
    try:
        return idp.get_user(user_id=user_id)
    except Exception as e:
        raise HTTPException(
            status_code=e.status_code,
            detail=e.reason,
        )

@router.get("/users", tags=["user-management"])
def get_users(user: OIDCUser = Depends(authorize_admin)):
    try:
        return idp.get_all_users()
    except Exception as e:
        raise HTTPException(
            status_code=e.status_code,
            detail=e.reason,
        )

@router.post("/users", tags=["user-management"])
def create_user(user_data: CreateUserData):
    try:
        return idp.create_user(first_name=user_data.firstName, last_name=user_data.lastName, username=user_data.email, email=user_data.email, password=user_data.password)
    except Exception as e:
        raise HTTPException(
            status_code=e.status_code,
            detail=e.reason,
        )

@router.delete("/user/{user_id}", tags=["user-management"])
def delete_user(user_id: Annotated[str, Body()], user: OIDCUser = Depends(authorize_user_or_admin)):
    try:
        return idp.delete_user(user_id=user_id)
    except Exception as e:
        raise HTTPException(
            status_code=e.status_code,
            detail=e.reason,
        )

@router.put("/user", tags=["user-management"])
def update_user(user_data: KeycloakUser, user: OIDCUser = Depends(authorize_user_or_admin)):
    response = idp.custom_update_user(user=user_data)
    if response.status_code == 204:
        return idp.get_user(user_id=user_data.id)
    else:
        raise HTTPException(
            status_code=response.status_code,
            detail=response.json(),
        )
        

@router.patch("/user", tags=["user-management"])
def partial_update_user(user_data: PartialKeycloakUser, user: OIDCUser = Depends(authorize_user_or_admin)):
    response = idp.custom_update_user(user=user_data)
    if response.status_code == 204:
        return idp.get_user(user_id=user_data.id)
    else:
        raise HTTPException(
            status_code=response.status_code,
            detail=response.json(),
        )

@router.put("/user/change-password", tags=["user-management"])
def change_password(password_data: PasswordData, user: OIDCUser = Depends(authorize_user_or_admin)):
    try:
        idp.change_password(user_id=password_data.user_id, new_password=password_data.new_password)
        return  {"detail": "Password changed successfully."}
    except Exception as e:
        raise HTTPException(
            status_code=e.status_code,
            detail=e.reason,
        )

@router.get("/login", tags=["user-management"])
def login(user: UsernamePassword = Depends()):
    return idp.user_login(username=user.username, password=user.password.get_secret_value())