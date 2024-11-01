from flask import Blueprint, abort, make_response, request, Response
from app.models.task import Task
from ..db import db

tasks_bp = Blueprint("tasks_bp", __name__, url_prefix="/tasks")

# VALIDATE
def validate_task(task_id):
    try:
        task_id = int(task_id)
    except ValueError:
        response = {"message": f"task {task_id} invalid"}
        abort(make_response(response, 400))

    query = db.select(Task).where(Task.id == task_id)
    task= db.session.scalar(query)

    if not task:
        response = {"message": f"task {task_id} not found"}
        abort(make_response(response, 404))

    return task

# CREATE
@tasks_bp.post("")
def create_task():
    request_body = request.get_json()

    if "title" not in request_body or "description" not in request_body:
        return {"details": "Invalid data"}, 400
    
    title = request_body["title"]
    description=request_body["description"]

    new_task = Task(
        title=title, description=description
    )

    db.session.add(new_task)
    db.session.commit()

    return {"task": new_task.to_dict()}, 201

# READ ALL
@tasks_bp.get("")
def get_all_tasks():
    query = db.select(Task)

    title_param = request.args.get("title")
    if title_param:
        query = query.where(Task.title.ilike(f"%{title_param}%"))

    description_param = request.args.get("description")
    if description_param:
        query = query.where(Task.description.ilike(f"%{description_param}%"))

    sort_param = request.args.get("sort")
    if sort_param:
        if sort_param.lower() == "desc":
            query = query.order_by(Task.title.desc())
        elif sort_param.lower() == "asc":
            query = query.order_by(Task.title.asc())
        else:
            query = query.order_by(Task.id)
    else:
        query = query.order_by(Task.id)

    tasks = db.session.scalars(query)

    return [task.to_dict() for task in tasks], 200

# READ ONE
@tasks_bp.get("/<task_id>")
def get_one_task(task_id):
    task = validate_task(task_id)

    return {"task": task.to_dict()}, 200

# UPDATE
@tasks_bp.put("/<task_id>")
def update_task(task_id):
    task = validate_task(task_id)
    request_body = request.get_json()

    task.title = request_body["title"]
    task.description = request_body["description"]
    db.session.commit()

    return {"task": task.to_dict()}, 200

# DELETE
@tasks_bp.delete("/<task_id>")
def delete_task(task_id):
    task = validate_task(task_id)
    task_title = task.title
    db.session.delete(task)
    db.session.commit()

    return {"details": f'Task {task_id} "{task_title}" successfully deleted'}, 200

@tasks_bp.patch("/<task_id>/mark_complete")
def mark_task_complete(task_id):
    task = validate_task(task_id)

    task.mark_complete()

    db.session.commit()

    return {"task": task.to_dict()}, 200


@tasks_bp.patch("/<task_id>/mark_incomplete")
def mark_task_incomplete(task_id):
    task = validate_task(task_id)

    task.mark_incomplete()

    db.session.commit()

    return {"task": task.to_dict()}, 200
