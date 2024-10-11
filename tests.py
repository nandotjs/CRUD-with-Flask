import requests
import pytest

BASE_URL = 'http://127.0.0.1:5000'

@pytest.fixture(autouse=True)
def run_before_each_test():
    # Limpar o estado do servidor antes de cada teste
    requests.post(f'{BASE_URL}/tasks/clear')

def test_create_task():
    response = requests.post(f'{BASE_URL}/tasks', json={
        'title': 'Test Task', 
        'description': 'This is a test task'
    })
    assert response.status_code == 201
    task = response.json()
    assert 'id' in task
    assert task['title'] == 'Test Task'
    assert task['description'] == 'This is a test task'

def test_get_all_tasks():
    # Criar uma tarefa antes de buscar todas as tarefas
    response = requests.post(f'{BASE_URL}/tasks', json={
        'title': 'Test Task', 
        'description': 'This is a test task'
    })
    assert response.status_code == 201

    response = requests.get(f'{BASE_URL}/tasks/all')
    assert response.status_code == 200
    assert isinstance(response.json(), dict)
    assert len(response.json()['tasks']) == 1  # Deve haver exatamente uma tarefa
    task = response.json()['tasks'][0]
    assert task['title'] == 'Test Task'
    assert task['description'] == 'This is a test task'

def test_get_task():
    # Criar uma tarefa para buscar
    response = requests.post(f'{BASE_URL}/tasks', json={
        'title': 'Test Task', 
        'description': 'This is a test task'
    })
    assert response.status_code == 201
    task_id = response.json()['id']

    # Buscar a tarefa criada
    response = requests.get(f'{BASE_URL}/tasks/{task_id}')
    assert response.status_code == 200
    task = response.json()
    assert task['id'] == task_id
    assert task['title'] == 'Test Task'
    assert task['description'] == 'This is a test task'

def test_update_task():
    # Criar uma tarefa para atualizar
    response = requests.post(f'{BASE_URL}/tasks', json={
        'title': 'Test Task', 
        'description': 'This is a test task'
    })
    assert response.status_code == 201
    task_id = response.json()['id']

    # Atualizar a tarefa criada
    response = requests.put(f'{BASE_URL}/tasks/{task_id}', json={
        'title': 'Updated Task', 
        'description': 'This is an updated test task',
        'completed': True
    })
    assert response.status_code == 200

    # Verificar se a tarefa foi atualizada
    response = requests.get(f'{BASE_URL}/tasks/{task_id}')
    assert response.status_code == 200
    task = response.json()
    assert task['title'] == 'Updated Task'
    assert task['description'] == 'This is an updated test task'
    assert task['completed'] is True

def test_delete_task():
    # Criar uma tarefa para deletar
    response = requests.post(f'{BASE_URL}/tasks', json={
        'title': 'Test Task', 
        'description': 'This is a test task'
    })
    assert response.status_code == 201
    task_id = response.json()['id']

    # Deletar a tarefa criada
    response = requests.delete(f'{BASE_URL}/tasks/{task_id}')
    assert response.status_code == 200

    # Verificar se a tarefa foi deletada
    response = requests.get(f'{BASE_URL}/tasks/{task_id}')
    assert response.status_code == 404

