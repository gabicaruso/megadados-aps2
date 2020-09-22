from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def test_read_main_returns_not_found():
    response = client.get('/')
    assert response.status_code == 404
    assert response.json() == {'detail': 'Not Found'}


def test_check_if_is_running():
    response = client.get('/check')
    assert response.status_code == 200
    assert response.json() == {'Check': 'Running'}


def test_read_tasks_without_any():
    response = client.get('/tasks_list/')
    assert response.status_code == 200
    assert response.json() == {}


# def test_read_tasks():
#     fake_db = {
#         "24433581-0225-4011-ba36-f65c97d2aa8c": {
#             "task_id": "24433581-0225-4011-ba36-f65c97d2aa8c",
#             "name": "t3",
#             "description": "task3",
#             "status": False
#         },
#         "d47b55fe-109e-41c9-8dee-4288df4fecb6": {
#             "task_id": "d47b55fe-109e-41c9-8dee-4288df4fecb6",
#             "name": "t4",
#             "description": "task4",
#             "status": False
#         },
#         "ca7ca4e5-6158-45ca-9351-6d110db6a178": {
#             "task_id": "ca7ca4e5-6158-45ca-9351-6d110db6a178",
#             "name": "t5",
#             "description": "task5",
#             "status": True
#         }
#     }
#     response = client.get('/tasks_list/')
#     assert response.status_code == 200
#     assert response.json() == {
#         "24433581-0225-4011-ba36-f65c97d2aa8c": {
#             "task_id": "24433581-0225-4011-ba36-f65c97d2aa8c",
#             "name": "t3",
#             "description": "task3",
#             "status": False
#         },
#         "d47b55fe-109e-41c9-8dee-4288df4fecb6": {
#             "task_id": "d47b55fe-109e-41c9-8dee-4288df4fecb6",
#             "name": "t4",
#             "description": "task4",
#             "status": False
#         },
#         "ca7ca4e5-6158-45ca-9351-6d110db6a178": {
#             "task_id": "ca7ca4e5-6158-45ca-9351-6d110db6a178",
#             "name": "t5",
#             "description": "task5",
#             "status": True
#         }
#     }

def test_create_task():
    response = client.post(
        '/tasks',
        json={
            "name": "task 1",
            "description": "task 1 description"
        }
    )
    assert response.status_code == 200
    response = response.json()
    assert response['task_id']
    assert response['name'] == 'task 1'
    assert response['description'] == 'task 1 description'
    assert response['status'] == False


def test_create_task_without_description():
    response = client.post(
        '/tasks',
        json={
            "name": "task 2"
        }
    )
    assert response.status_code == 422
    assert response.json() == {
        "detail": [
            {
                "loc": [
                    "body",
                    "description"
                ],
                "msg": "field required",
                "type": "value_error.missing"
            }
        ]
    }


def test_create_task_without_name():
    response = client.post(
        '/tasks',
        json={
            "description": "task 2 description"
        }
    )
    assert response.status_code == 422
    assert response.json() == {
        "detail": [
            {
                "loc": [
                    "body",
                    "name"
                ],
                "msg": "field required",
                "type": "value_error.missing"
            }
        ]
    }
