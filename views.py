from datetime import datetime
from uuid import uuid4

from flask import make_response, request, Blueprint
from app import app
from db import task_storage

bp = Blueprint('tasks', __name__)
@bp.route("/")
def list_tasks():
    completed_flag = request.args.get('completed', '') #fetch the user parameter
    if completed_flag and completed_flag.lower() not in ('true', 'false'):
        return make_response(({'message': 'Invalid completed flag, must match "true" or "false"'}), 400)

    flag_mapping = {'true': True, 'false': False}
    if not completed_flag:
        tasks = task_storage
    else:
        tasks = {
            task_id: task_info for task_id, task_info in task_storage.items()
            if task_info['is_completed'] == flag_mapping[completed_flag.lower()]
        }

    return make_response(tasks)

@bp.post('/')
def create_task():
    task_id = uuid4().hex #generate unique task id
    #task data here
    task_info = {
        'title': request.json.get('title', 'Missed title'),
        'created_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'is_completed': False,
    }

    task_storage[task_id] = task_info #save the task in storage
    return make_response({'id':task_id}) #return task id

@bp.put('/<task_id>')
def complete_task(task_id):
    task = task_storage.get(task_id) #trying to find and get task by id and return 404 if not found
    if not task:
        return make_response(({"Message":"No task found"}), 404)
    task['is_completed'] = True #change the status of task to completed

    return make_response({'is_completed': True})

@bp.delete('/<task_id>')
def delete_task(task_id):
    task = task_storage.pop(task_id, None) #trying to pop task by id and return 404 if not gound
    if not task:
        return make_response(({'message': 'No task found'}), 404)

    return make_response({'deleted': True}) #return deleted status