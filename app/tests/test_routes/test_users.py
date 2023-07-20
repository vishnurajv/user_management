from starlette.testclient import TestClient

from app.main import app

client = TestClient(app)

# Get access token from keycloak for requests
def create_access_token():
    response = client.get("/latest/login?username=vishnu&password=password")
    result = response.json()
    return result.get('access_token')

# User create
def create_user():
    access_token = create_access_token()
    {
        'Authorization': 'Bearer {}'.format(access_token)
    }
    response = client.post(  
        "/latest/users", 
        json={
          "firstName": "test2",
          "lastName": "test2",
          "email": "test3@test.com",
          "password": "password"
        },
        headers={ 'Content-Type': 'application/json'}
    )
    assert response.status_code == 200
    result = response.json()
    return result.get('id')

# Get user with ID
def test_get_user():
    access_token = create_access_token()
    headers = {
        'Authorization': 'Bearer {}'.format(access_token)
    }
    response = client.get(
        '/latest/user/514a6071-1714-4ee6-8374-472c080d8a94',
        headers=headers
    )
    response.json()
    assert response.status_code == 200

# Get all users
def test_get_users():
    access_token = create_access_token()
    headers = {
        'Authorization': 'Bearer {}'.format(access_token)
    }
    response = client.get('/latest/users', headers=headers)
    response.json()
    assert response.status_code == 200

# Create and Delete the same user
def test_create_and_delete_user():
    access_token = create_access_token()
    user_id = create_user()
    response = client.delete(  
        "/latest/user/{}".format(user_id), 
        headers={ 
            'Content-Type': 'application/json',
            'Authorization': 'Bearer {}'.format(access_token)
        }
    )

    response.json()
    assert response.status_code == 200

# User record updation
def test_update_and_partial_update_user():
    access_token = create_access_token()
    response = client.put(  
        "/latest/user", 
        headers={ 
            'Content-Type': 'application/json',
            'Authorization': 'Bearer {}'.format(access_token)
        },
        json={
            "id": "514a6071-1714-4ee6-8374-472c080d8a94",
            "firstName": "test_u",
            "lastName": "test_u",
            "email": "test@test1.com"
        }
    )
    response.json()
    assert response.status_code == 200
    response = client.patch(  
        "/latest/user", 
        headers={ 
            'Content-Type': 'application/json',
            'Authorization': 'Bearer {}'.format(access_token)
        },
        json={
            "id": "514a6071-1714-4ee6-8374-472c080d8a94",
            "firstName": "test",
            "lastName": "test",
            "email": "test@test.com"
        }
    )
    response.json()
    assert response.status_code == 200
