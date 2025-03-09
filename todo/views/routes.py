from flask import Blueprint, jsonify, request
from todo.models import db
from todo.models.todo import Todo
from datetime import datetime, timedelta

api = Blueprint('api', __name__, url_prefix='/api/v1') 

TEST_ITEM = {
    "id": 1,
    "title": "Watch CSSE6400 Lecture",
    "description": "Watch the CSSE6400 lecture on ECHO360 for week 1",
    "completed": True,
    "deadline_at": "2023-02-27T00:00:00",
    "created_at": "2023-02-20T00:00:00",
    "updated_at": "2023-02-20T00:00:00"
}
 
@api.route('/health') 
def health():
    """Return a status of 'ok' if the server is running and listening to request"""
    return jsonify({"status": "ok"})


@api.route('/todos', methods=['GET'])
def get_todos():
    completed = request.args.get('completed')
    window = request.args.get('window')

    todos = Todo.query.all()
    result = []
    for todo in todos:
        if completed is not None:
            if str(todo.completed).lower() != completed:
                continue

        if window is not None:
            date_limit = datetime.utcnow() + timedelta(days=int(window))
            if todo.deadline_at > date_limit:
                continue

        result.append(todo.to_dict())
    return jsonify(result)

@api.route('/todos/<int:todo_id>', methods=['GET'])
def get_todo(todo_id):
    todo = Todo.query.get(todo_id)
    if todo is None:
        return jsonify({'error': 'Todo not found'}), 404
    return jsonify(todo.to_dict())

@api.route('/todos', methods=['POST'])
def create_todo():
    todo = Todo(
        title = request.json.get('title'),
        description = request.json.get('description'),
        completed = request.json.get('completed', False),
    )
    if 'deadline_at' in request.json:
        todo.deadline_at = datetime.fromisoformat(request.json.get('deadline_at'))
    for item in request.json:
        if item not in TEST_ITEM.keys():
            return jsonify({'error': 'extra words'}), 400
    if "title" not in request.json:
        return jsonify({'error': 'missing title'}), 400
    db.session.add(todo)
    db.session.commit()
    return jsonify(todo.to_dict()), 201

@api.route('/todos/<int:todo_id>', methods=['PUT'])
def update_todo(todo_id):
    todo = Todo.query.get(todo_id)
    if todo is None:
        return jsonify({'error': 'Todo not found'}), 404
    
    # for item in request.json:
    #     if item not in TEST_ITEM.keys():
    #         return jsonify({'error': 'extra words'}), 400

    if not set(request.json.keys()).issubset(set(('title', 'description', 'completed', 'deadline_at'))):
        return jsonify({'error': 'extra fields'}), 400
    

    todo.title = request.json.get('title',todo.title)
    todo.description = request.json.get('description',todo.description)
    todo.completed = request.json.get('completed',todo.completed)
    todo.deadline_at = request.json.get('deadline_at',todo.deadline_at)

    db.session.commit()
    return jsonify(todo.to_dict())

@api.route('/todos/<int:todo_id>', methods=['DELETE'])
def delete_todo(todo_id):
    todo = Todo.query.get(todo_id)
    if todo is None:
        return jsonify({}), 200
    
    db.session.delete(todo)
    db.session.commit()
    return jsonify(todo.to_dict()), 200
 
