from flask import Flask, make_response, request
from uuid import uuid4
from datetime import datetime

app = Flask("Task Manager")

task_storage = {} #used for data storage

@app.route("/")
def list_tasks():
    tasks = task_storage
    completed_flag = request.args.get('completed', '') #fetch the user parameter
    if completed_flag.lower() == 'true': #filtering only completed tasks
        tasks = {
            task_id: task_info for task_id, task_info in tasks.items() if task_info["is_completed"]
        }

    elif completed_flag.lower() == 'false': #filtering not completed tasks
        tasks = {
            task_id: task_info for task_id, task_info in tasks.items() if not task_info["is_completed"]
        }
    return make_response(tasks)  #return tasks
@app.post('/')
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

@app.put('/<task_id>')
def complete_task(task_id):
    task = task_storage.get(task_id) #trying to find and get task by id and return 404 if not found
    if not task:
        return make_response(({"Message":"No task found"}), 404)
    task['is_completed'] = True #change the status of task to completed

    return make_response({'is_completed': True})

@app.delete('/<task_id>')
def delete_task(task_id):
    task = task_storage.pop(task_id, None) #trying to pop task by id and return 404 if not gound
    if not task:
        return make_response(({'message': 'No task found'}), 404)

    return make_response({'deleted': True}) #return deleted status

if __name__ == '__main__':
    app.run(debug=True)