from fastapi import APIRouter, Body
from fastapi import Depends, HTTPException
from fastapi_keycloak import OIDCUser, UsernamePassword
from app.models.users import (
    KeycloakUser, PartialKeycloakUser, PasswordData, CreateUserData
)
from typing_extensions import Annotated
from app.services.auth import idp, authorize_user_or_admin, authorize_admin

router = APIRouter()

# get user with user_id
@router.get("/user/{user_id}", tags=["user-management"])
def get_user(user_id: str = None):
    try:
        return idp.get_user(user_id=user_id)
    except Exception as e:
        raise HTTPException(
            status_code=e.status_code,
            detail=e.reason,
        )

# list add users
@router.get("/users", tags=["user-management"])
def get_users(user: OIDCUser = Depends(authorize_admin)):
    try:
        return idp.get_all_users()
    except Exception as e:
        raise HTTPException(
            status_code=e.status_code,
            detail=e.reason,
        )

# create user
@router.post("/users", tags=["user-management"])
def create_user(user_data: CreateUserData):
    try:
        return idp.create_user(
            first_name=user_data.firstName, last_name=user_data.lastName,
            username=user_data.email, email=user_data.email, password=user_data.password
        )
    except Exception as e:
        raise HTTPException(
            status_code=e.status_code,
            detail=e.reason,
        )
# delete user
@router.delete("/user/{user_id}", tags=["user-management"])
def delete_user(
        user_id: Annotated[str, Body()],
        user: OIDCUser = Depends(authorize_user_or_admin)
    ):
    try:
        return idp.delete_user(user_id=user_id)
    except Exception as e:
        raise HTTPException(
            status_code=e.status_code,
            detail=e.reason,
        )
# update user
@router.put("/user", tags=["user-management"])
def update_user(
        user_data: KeycloakUser,
        user: OIDCUser = Depends(authorize_user_or_admin)
    ):
    response = idp.custom_update_user(user=user_data)
    if response.status_code == 204:
        return idp.get_user(user_id=user_data.id)
    else:
        raise HTTPException(
            status_code=response.status_code,
            detail=response.json(),
        )
        
# partial update user
@router.patch("/user", tags=["user-management"])
def partial_update_user(
        user_data: PartialKeycloakUser,
        user: OIDCUser = Depends(authorize_user_or_admin)
    ):
    response = idp.custom_update_user(user=user_data)
    if response.status_code == 204:
        return idp.get_user(user_id=user_data.id)
    else:
        raise HTTPException(
            status_code=response.status_code,
            detail=response.json(),
        )

# change password
@router.put("/user/change-password", tags=["user-management"])
def change_password(
        password_data: PasswordData,
        user: OIDCUser = Depends(authorize_user_or_admin)
    ):
    try:
        idp.change_password(
            user_id=password_data.user_id,
            new_password=password_data.new_password
        )
        return  {"detail": "Password changed successfully."}
    except Exception as e:
        raise HTTPException(
            status_code=e.status_code,
            detail=e.reason,
        )

# user login
@router.get("/login", tags=["user-management"])
def login(user: UsernamePassword = Depends()):
    return idp.user_login(
            username=user.username,
            password=user.password.get_secret_value()
        )