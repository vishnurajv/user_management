from pydantic import BaseModel
from typing import Optional


class Attributes(BaseModel):
    permissionLevel: str

class KeycloakUser(BaseModel):
    id: str
    firstName: str
    lastName: str
    email: str
    attributes: Optional[Attributes]

class PartialKeycloakUser(BaseModel):
    id: str
    firstName: Optional[str]
    lastName: Optional[str]
    email: Optional[str]
    attributes: Optional[Attributes]

class PasswordData(BaseModel):
    user_id: str
    new_password: str