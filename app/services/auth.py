from app.services.custom_fastapi_keycloak import CustomFastAPIKeycloak
from fastapi import Depends, HTTPException, status, Request
from app.core.config import settings

idp = CustomFastAPIKeycloak(
    server_url=settings.KEYCLOAK_SERVER_URL,
    client_id=settings.KEYCLOAK_CLIENT_ID,
    client_secret=settings.KEYCLOAK_CLIENT_SECRET,
    admin_client_secret=settings.KEYCLOAK_ADMIN_CLIENT_SECRET,
    realm=settings.KEYCLOAK_REALM,
    callback_uri=settings.KEYCLOAK_CALLBACK_URI
)

# over riding fastapi_keycloak authorization to support checking permissionLevel

# authorize user or admin
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

# authorize admin
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