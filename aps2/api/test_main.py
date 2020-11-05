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

#Checks if the request returns an empty dictionary 
def test_read_tasks_without_any():
    response = client.get('/task')
    assert response.status_code == 200
    assert response.json() == {}
    
#checks if the request with an invalid query returns a 422 code
#with a 'type_error.enum' message
def test_get_wrong_enum_value():
    response = client.get('/task?status=oi')
    assert response.status_code == 422
    assert response.json() ==  {
        'detail': 
        [
            {
            'ctx': {'enum_values': ['done', 'not_done']}, 
            'loc': ['query', 'status'],
            'msg': "value is not a valid enumeration member; permitted: 'done', 'not_done'",
            'type': 'type_error.enum'
            }
        ]
    }


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

    #Insert some tasks and check that all succeeded  
    for task in fake_db:
        response = client.post(
            '/task',
            json=task
        )
        assert response.status_code == 200
        response = response.json()
        uuids.append(response['task_id'])
        expected_responses(response_get, response)
        if response['status'] == False:
            expected_responses(response_not_done, response)
        if response['status'] == True:
            expected_responses(response_done, response)

    #Checks if the request returns a dictionary containing all tasks
    response = client.get('/task/')
    assert response.status_code == 200
    assert response.json() == response_get

    #Checks if the request returns a dictionary containing
    # all tasks which the status field is "False" 
    response = client.get('/task?status=not_done')
    assert response.status_code == 200
    assert response.json() == response_not_done

    #Check if the request returns a dictionary containing 
    #all tasks which the status field is "True" 
    response = client.get('/task?status=done')
    assert response.status_code == 200
    assert response.json() == response_done

    #Delete all tasks and check if the list of tasks is empty
    for uuid in uuids:
        response = client.delete(
            f'/task/{uuid}'
        )
        assert response.status_code == 200
    assert response.json() == {}

#Checks if the post request succeded 
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

#Insert a task with no description and checks if 
#returns a 422 code with a value_error.missing message
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

#Insert a task with no name and checks if 
#returns a 422 code with a "value_error.missing" message
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

#Checks if the delete request succeded 
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

#Try to delete a task with a non existing uuid as a parameter and 
#checks if returns a 404 code with a "Task not found" message
def test_delete_task_wrong_id():
    wrong_uuid = "5e6bff37-70b3-42bc-a0d0-8c731e12b411"
    response = client.delete(
        f'/task/{wrong_uuid}'
    )
    assert response.status_code == 404
    assert response.json() == {"detail": "Task not found"}

#Checks if a patch request succeded 
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

#Try to update a task with a non existing uuid as a parameter and 
#checks if returns a 404 code with a "Task not found" message
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

#Try to update a task without the description parameter and checks if 
#returns a 422 code with a "value_error.missing" message
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

#Try to update a task without the status parameter and checks if 
#returns a 422 code with a "value_error.missing" message
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

#Try to update a task using a string as a status parameter and
#checks if returns a 422 code with a "type_error.bool" message
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
