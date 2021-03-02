from flask import Flask
from flask import request, jsonify, abort, make_response
from flask import render_template
from datetime import datetime

app = Flask(__name__)

tasks = [
    {
        'id': 1,
        'title': u'ABCD55',
        'description': u'Matricula detectada', 
        'date': u'2021-01-03T19:25',
        'done': False
    },
    {
        'id': 2,
        'title': u'EFGAH22',
        'description': u'Matricula detectada',
        'date': u'2021-01-03T19:26',
        'done': False
    }
]

@app.route('/')
def index():
    return render_template("./index.html", tasks = tasks)
@app.route('/', methods=['GET'])
def get_tasks():
    # return jsonify({'tasks':tasks})
    return render_template("./index.html", tasks = tasks)

@app.route('/<int:task_id>', methods=['GET'])
def get_task(task_id):
    task = [task for task in tasks if task['id'] == task_id]
    if not task:
        abort(404)
    return jsonify({'task':task[0]})

@app.errorhandler(404)
def not_found(erorr):
    return make_response(jsonify({'error':'Not found'}), 404)

@app.route('/', methods=['POST'])
def create_task():
    task = {
        'id': tasks[-1]['id']+1,
        'title': request.json['title'],
        'description':request.json.get('description',""),
        'date': datetime.now().isoformat(timespec='minutes')
    }
    tasks.append(task)
    return jsonify({'task':task}), 201


if __name__ == '__main__':
    app.run(debug=True)
