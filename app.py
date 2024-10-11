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
    return jsonify({'message': 'Task created successfully'}), 201
    
@app.route('/tasks/all', methods=['GET'])
def get_all_tasks():
    task_list = [task.to_dict() for task in tasks]
    total_tasks = len(tasks)
    return jsonify({
        'tasks': task_list,
        'total_tasks': total_tasks 
    }), 200

if __name__ == '__main__':
    app.run(debug=True) 