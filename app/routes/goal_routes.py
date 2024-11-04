from flask import Blueprint, abort, make_response, request, Response
from app.models.goal import Goal
import os
import requests
from ..db import db
from .route_utilities import validate_model

goals_bp = Blueprint("goals_bp", __name__, url_prefix="/goals")


# CREATE
@goals_bp.post("")
def create_goal():
    request_body = request.get_json()

    try:
        new_goal = Goal.from_dict(request_body)
    except KeyError:
        response = {"details": "Invalid data"}
        abort(make_response(response, 400))

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
    goal = validate_model(Goal, goal_id)

    return {"goal": goal.to_dict()}, 200

# UPDATE
@goals_bp.put("/<goal_id>")
def update_task(goal_id):
    goal = validate_model(Goal, goal_id)
    request_body = request.get_json()

    goal.title = request_body["title"]
    db.session.commit()

    return {"goal": goal.to_dict()}, 200

# DELETE
@goals_bp.delete("/<goal_id>")
def delete_task(goal_id):
    goal = validate_model(Goal, goal_id)
    goal_title = goal.title
    db.session.delete(goal)
    db.session.commit()

    return {"details": f'Goal {goal_id} "{goal_title}" successfully deleted'}, 200
