from fastapi.testclient import TestClient
from .main import app

client = TestClient(app)

def test_read_main_returns_not_found():
    response = client.get('/')
    assert response.status_code == 404
    assert response.json() == {'detail': 'Not Found'}


def test_check_if_is_running():
    response = client.get('/task/check')
    assert response.status_code == 200
    assert response.json() == {'Check': 'Running'}


def test_read_tasks_without_any():
    response = client.get('/task')
    assert response.status_code == 200
    assert response.json() == {}


def test_read_tasks_and_delete_then():
    fake_db = [
        {
            "name": "t3",
            "description": "task3",

        },
        {
            "name": "t4",
            "description": "task4",
        },
        {
            "name": "t5",
            "description": "task5",
        }
    ]
    response_get = {}
    response_done = {}
    response_not_done = {}
    uuids = []

    def expected_responses(dic, res):
        dic.update({res['task_id']:
                    {"task_id": res['task_id'],
                     "name": res['name'],
                     "description": res['description'],
                     "status": res['status']}}
                   )

    for task in fake_db:
        response = client.post(
            '/task',
            json=task
        )
        response = response.json()
        uuids.append(response['task_id'])
        expected_responses(response_get, response)
        if response['status'] == False:
            expected_responses(response_not_done, response)
        if response['status'] == True:
            expected_responses(response_done, response)

    response = client.get('/task/')
    assert response.status_code == 200
    assert response.json() == response_get

    response = client.get('/task?status=not_done')
    assert response.status_code == 200
    assert response.json() == response_not_done

    response = client.get('/task?status=done')
    assert response.status_code == 200
    assert response.json() == response_done

    for uuid in uuids:
        response = client.delete(
            f'/task/{uuid}'
        )
        assert response.status_code == 200
    assert response.json() == {}


def test_create_task():
    response = client.post(
        '/task',
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
        '/task',
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
        '/task',
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


def test_delete_task():
    response = client.post(
        '/task',
        json={
            "name": "task 7",
            "description": "task 7 description"
        }
    )
    response = response.json()
    uuid = response["task_id"]
    response = client.delete(
        f'/task/{uuid}'
    )
    assert response.status_code == 200


def test_delete_task_wrong_id():
    wrong_uuid = "5e6bff37-70b3-42bc-a0d0-8c731e12b411"
    response = client.delete(
        f'/task/{wrong_uuid}'
    )
    assert response.status_code == 404
    assert response.json() == {"detail": "Task not found"}


def test_update_task():
    response = client.post(
        '/task',
        json={
            "name": "task 10",
            "description": "task 10 description"
        }
    )
    response = response.json()
    uuid = response["task_id"]
    response = client.patch(
        f'/task/{uuid}',
        json={
            "description": "task 10 description",
            'status': True
        }
    )
    updated_task = response.json()
    assert updated_task['description'] == 'task 10 description'
    assert updated_task['status'] == True
    assert response.status_code == 200


def test_update_task_wrong_id():
    wrong_uuid = "5e6bff37-70b3-42bc-a0d0-8c731e12b411"
    response = client.patch(
        f'/task/{wrong_uuid}',
        json={
            "description": "task 2 description",
            "status": "True"
        }
    )
    assert response.status_code == 404
    assert response.json() == {"detail": "Task not found"}


def test_update_task_without_description():
    response = client.post(
        '/task',
        json={
            "name": "task 11",
            "description": "task 11 description"
        }
    )
    response = response.json()
    uuid = response["task_id"]
    response = client.patch(
        f'/task/{uuid}',
        json={
            'status': True
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


def test_update_task_without_status():
    response = client.post(
        '/task',
        json={
            "name": "task 12",
            "description": "task 12 description"
        }
    )
    response = response.json()
    uuid = response["task_id"]
    response = client.patch(
        f'/task/{uuid}',
        json={
            "description": "task 12 new description"
        }
    )
    assert response.status_code == 422
    assert response.json() == {
        "detail": [
            {
                "loc": [
                    "body",
                    "status"
                ],
                "msg": "field required",
                "type": "value_error.missing"
            }
        ]
    }


def test_update_task_with_wrong_status():
    response = client.post(
        '/task',
        json={
            "name": "task 13",
            "description": "task 13 description"
        }
    )
    response = response.json()
    uuid = response["task_id"]
    response = client.patch(
        f'/task/{uuid}',
        json={
            "description": "task 13 new description",
            'status': "string"
        }
    )
    assert response.status_code == 422
    assert response.json() == {
        "detail": [
            {
                "loc": [
                    "body",
                    "status"
                ],
                "msg": "value could not be parsed to a boolean",
                "type": "type_error.bool"
            }
        ]
    }
