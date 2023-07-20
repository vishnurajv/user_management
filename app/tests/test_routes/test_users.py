from starlette.testclient import TestClient

from app.main import app

client = TestClient(app)


def create_access_token():
    response = client.get("/latest/login?username=vishnu&password=password")
    result = response.json()
    return result.get('access_token')

def create_user():
    access_token = create_access_token()
    headers = {
        'Authorization': 'Bearer {}'.format(access_token)
    }
    form_data = {}
    response = client.post(  
        "/latest/users?first_name=test2&last_name=test2&email=test3%40test.com&password=password", 
        data=form_data,
        headers={ 'Content-Type': 'application/json'}
    )
    assert response.status_code == 200
    result = response.json()
    return result.get('id')


def test_get_user():
    access_token = create_access_token()
    headers = {
        'Authorization': 'Bearer {}'.format(access_token)
    }
    response = client.get('/latest/user/514a6071-1714-4ee6-8374-472c080d8a94', headers=headers)
    result = response.json()
    assert response.status_code == 200

def test_get_users():
    access_token = create_access_token()
    headers = {
        'Authorization': 'Bearer {}'.format(access_token)
    }
    response = client.get('/latest/users', headers=headers)
    result = response.json()
    assert response.status_code == 200

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

    result = response.json()
    assert response.status_code == 200

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
    result = response.json()
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
    result = response.json()
    assert response.status_code == 200
