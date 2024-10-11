from flask import Flask, request, jsonify
from models.task import Task 
app = Flask(__name__)

tasks = []
task_id_control = 1

@app.route('/tasks', methods=['POST'])
def create_task():
    global task_id_control
    data = request.get_json()
    new_task = Task(id=task_id_control, title=data['title'], description=data.get('description', ''))
    task_id_control += 1
    tasks.append(new_task)
    return jsonify(new_task.to_dict()), 201 

@app.route('/tasks/all', methods=['GET'])
def get_all_tasks():
    task_list = [task.to_dict() for task in tasks]
    total_tasks = len(tasks)
    return jsonify({
        'tasks': task_list,
        'total_tasks': total_tasks 
    }), 200

@app.route('/tasks/<int:id>', methods=['GET'])
def get_task(id):
    task = next((task for task in tasks if task.id == id), None)
    if task:
        return jsonify(task.to_dict()), 200  # Ensure correct status code and response
    return jsonify({'message': 'Task not found'}), 404

@app.route('/tasks/<int:id>', methods=['PUT'])
def update_task(id):
    data = request.get_json()
    task = next((task for task in tasks if task.id == id), None)
    if not task:
        return jsonify({'message': 'Task not found'}), 404  
    task.title = data.get('title', task.title)
    task.description = data.get('description', task.description)
    
    if 'completed' in data and isinstance(data['completed'], bool):
        task.completed = data['completed']
    
    return jsonify({'message': 'Task updated successfully'}), 200

@app.route('/tasks/<int:id>', methods=['DELETE'])
def delete_task(id):
    global tasks
    tasks = [task for task in tasks if task.id != id]
    return jsonify({'message': 'Task deleted successfully'}), 200

@app.route('/tasks/clear', methods=['POST'])
def clear_tasks():
    global tasks, task_id_control
    tasks = []
    task_id_control = 1
    return jsonify({'message': 'All tasks cleared'}), 200

if __name__ == '__main__':
    app.run(debug=True)
