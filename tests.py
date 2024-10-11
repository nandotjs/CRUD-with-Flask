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

