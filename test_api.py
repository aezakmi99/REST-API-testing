import requests 
import uuid #random generiranje stringa za user-a

ENDPOINT = "https://todo.pixegami.io"
def test_can_call_endpoint():
    response = requests.get(ENDPOINT)
    assert response.status_code == 200

def test_can_create_task():
    payload = new_task_payload()
    create_task_response = create_task(payload) #payload -> request body koje ovaj API treba , create-task -> path do API-ja
    assert create_task_response.status_code == 200
    data = create_task_response.json()

    task_id = data["task"]["task_id"] 
    get_task_response = get_task(task_id)

    assert get_task_response.status_code == 200
    get_task_data = get_task_response.json() 

    assert get_task_data["content"] == payload["content"]
    assert get_task_data["user_id"] == payload["user_id"]

def test_can_update_task():
    #create task
    payload = new_task_payload()
    create_task_response = create_task(payload)
    assert create_task_response.status_code == 200
    task_id = create_task_response.json()["task"]["task_id"]
    #update task
    new_payload = {
        "user_id" : payload["user_id"],
        "task_id" : task_id,
        "content" : "my updatet content",
        "is_done" : True,
    }
    update_task_response = update_task(new_payload)
    assert update_task_response.status_code == 200
    
    #get and validate the changes
    get_task_response = get_task(task_id)
    assert get_task_response.status_code == 200
    get_task_data = get_task_response.json()
    assert get_task_data["content"] == new_payload["content"]
    assert get_task_data["is_done"] == new_payload["is_done"]


def test_can_list_tasks():
    #create N tasks
    N = 3
    payload = new_task_payload() #kreirana 3 taska sa istim contentom i user_id, različiti task_id jer ga generira server
    for _ in range(N):
        create_task_response = create_task(payload)
        assert create_task_response.status_code == 200

    #list tasks anc check that there are N items
    user_id = payload["user_id"]
    list_task_response = list_tasks(user_id)
    assert list_task_response.status_code == 200
    data = list_task_response.json()

    tasks = data["tasks"] #key object iz outputa od printa dolje, root node -> task key
    assert len(tasks) == N

    print(data)

def test_can_delete_task():
    #create
    payload = new_task_payload()
    create_task_response = create_task(payload)
    assert create_task_response.status_code == 200
    data = create_task_response.json()
    
    task_id = data["task"]["task_id"]

    #delete
    delete_task_response = delete_task(task_id)
    assert delete_task_response.status_code == 200

    #try to get task
    get_task_response = get_task(task_id)
    assert get_task_response.status_code == 404 #treba se dobit true, status code je 404 jer je task obrisan i ne mozemo ga dohvatit


def create_task(payload):
    return requests.put(ENDPOINT + "/create-task", json=payload)

def update_task(payload):
    return requests.put(ENDPOINT + "/update-task", json=payload)

def get_task(task_id):
    return requests.get(ENDPOINT + f"/get-task/{task_id}") 

def list_tasks(user_id):
    return requests.get(ENDPOINT + f"/list-tasks/{user_id}")

def delete_task(task_id):
    return requests.delete(ENDPOINT + f"/delete-task/{task_id}")

def new_task_payload():
    user_id = f"test_user_{uuid.uuid4().hex}" #prefix test_user
    content = f"test_content_{uuid.uuid4().hex}" #prefix test_content

    print(f"Creating task for user {user_id} with content {content}")

    return {
        "content": content,
        "user_id": user_id,
        "is_done":  False,
    }














