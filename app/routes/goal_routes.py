from flask import Blueprint, abort, make_response, request, Response
from app.models.goal import Goal
import os
import requests
from ..db import db

goals_bp = Blueprint("goals_bp", __name__, url_prefix="/goals")


# VALIDATE
def validate_goal(goal_id):
    try:
        goal_id = int(goal_id)
    except ValueError:
        response = {"message": f"goal {goal_id} invalid"}
        abort(make_response(response, 400))

    query = db.select(Goal).where(Goal.id == goal_id)
    goal = db.session.scalar(query)

    if not goal:
        response = {"message": f"goal {goal_id} not found"}
        abort(make_response(response, 404))

    return goal


@goals_bp.post("")
def create_goal():
    request_body = request.get_json()

    if not request_body:
        return {"details": "Invalid data"}, 400

    title = request_body["title"]

    new_goal = Goal(title=title)

    db.session.add(new_goal)
    db.session.commit()

    return {"goal": new_goal.to_dict()}, 201

# GET ALL
@goals_bp.get("")
def get_all_goals():

    query = db.select(Goal)
    goals = db.session.scalars(query)

    return [goal.to_dict() for goal in goals], 200

# GET ONE
@goals_bp.get("/<goal_id>")
def get_one_goals(goal_id):
    goal = validate_goal(goal_id)

    return {"goal": goal.to_dict()}, 200

# UPDATE
@goals_bp.put("/<goal_id>")
def update_task(goal_id):
    goal = validate_goal(goal_id)
    request_body = request.get_json()

    goal.title = request_body["title"]
    db.session.commit()

    return {"goal": goal.to_dict()}, 200

# DELETE
@goals_bp.delete("/<goal_id>")
def delete_task(goal_id):
    goal = validate_goal(goal_id)
    goal_title = goal.title
    db.session.delete(goal)
    db.session.commit()

    return {"details": f'Goal {goal_id} "{goal_title}" successfully deleted'}, 200
