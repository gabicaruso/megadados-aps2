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


def test_read_tasks():
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

    def expected_responses(dic,res):
        dic.update({res['task_id'] :
        { "task_id" : res['task_id'], 
        "name" : res['name'] ,
        "description": res['description'],
        "status": res['status']}}
        )

    for task in fake_db :
        response = client.post(
            '/tasks',
            json = task
        )
        response = response.json()
        expected_responses(response_get, response)
        if response['status'] == False:
            expected_responses(response_not_done, response)
        if response['status'] == True:
            expected_responses(response_done, response)

    response = client.get('/tasks_list/')
    assert response.status_code == 200
    assert response.json() == response_get

    response =  client.get('/tasks_list/?status=not_done')
    assert response.status_code == 200
    assert response.json() == response_not_done
  
    response =  client.get('/tasks_list/?status=done')
    assert response.status_code == 200
    assert response.json() == response_done

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

def test_delete_task() :
    response = client.post(
        '/tasks',
        json={
            "name": "task 1",
            "description": "task 1 description"
        }
    )

    response = response.json()
    uuid = response["task_id"]
    response = client.delete(
        f'/task_delete/{uuid}'
    )
    assert response.status_code == 200


# def patch_id_not_found():
#     response = client.post(
#         '/tasks',
#         json={
#             "name": "task 1",
#             "description": "task 1 description"
#         }
#     )

    

# def delete_id_not_found():
#      response = client.delete(
#         '/task_delete/a8a76e99-de76-421b-918b-1de772e686d1'
#     )
#      response = response.json() 
#      assert response.status_code == 500
#      assert response.json() == {'message': 'Internal Server Error'}
    



    









