from fastapi_keycloak import FastAPIKeycloak, OIDCUser, UsernamePassword, HTTPMethod, KeycloakGroup, KeycloakUser
from requests import Response
import requests, json

class CustomFastAPIKeycloak(FastAPIKeycloak):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def _custom_admin_request(
            self,
            url: str,
            method: HTTPMethod,
            data: dict = None,
            content_type: str = "application/json",
    ) -> Response:
        """Private method that is the basis for any requests requiring admin access to the api. Will append the
        necessary `Authorization` header

        Args:
            url (str): The URL to be called
            method (HTTPMethod): The HTTP verb to be used
            data (dict): The payload of the request
            content_type (str): The content type of the request

        Returns:
            Response: Response of Keycloak
        """
        headers = {
            "Content-Type": content_type,
            "Authorization": f"Bearer {self.admin_token}",
        }
        if data.__dict__['attributes']:
            data.__dict__['attributes'] = data.__dict__['attributes'].__dict__
        body = json.dumps(data.__dict__)
        return requests.request(
            method=method.name, url=url, data=body, headers=headers, timeout=self.timeout,
        )

    def custom_update_user(self, user: KeycloakUser):
        """Updates a user. Requires the whole object.

        Args:
            user (KeycloakUser): The (new) user object

        Returns:
            KeycloakUser: The updated user

        Raises:
            KeycloakError: If the resulting response is not a successful HTTP-Code (>299)

        Notes: - You may alter any aspect of the user object, also the requiredActions for instance. There is no
        explicit function for updating those as it is a user update in essence
        """
        response = self._custom_admin_request(
            url=f"{self.users_uri}/{user.id}", data=user, method=HTTPMethod.PUT
        )
        return response