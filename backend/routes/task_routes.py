from flask import Blueprint, request, jsonify
from pymongo import MongoClient
from bson.objectid import ObjectId

task_bp = Blueprint('task_bp', __name__)

# MongoDB Connection
client = MongoClient("YOUR_ATLAS_URL")

db = client["taskdb"]

tasks = db["tasks"]

# -----------------------------------
# GET ALL TASKS
# -----------------------------------
@task_bp.route('/tasks', methods=['GET'])
def get_tasks():

    all_tasks = []

    for task in tasks.find():
        task['_id'] = str(task['_id'])
        all_tasks.append(task)

    return jsonify(all_tasks)

# -----------------------------------
# ADD TASK
# -----------------------------------
@task_bp.route('/tasks', methods=['POST'])
def add_task():

    data = request.json

    new_task = {
        "title": data['title'],
        "status": data['status']
    }

    tasks.insert_one(new_task)

    return jsonify({
        "message": "Task Added Successfully"
    })

# -----------------------------------
# UPDATE TASK
# -----------------------------------
@task_bp.route('/tasks/<id>', methods=['PUT'])
def update_task(id):

    data = request.json

    tasks.update_one(
        {"_id": ObjectId(id)},
        {
            "$set": {
                "title": data['title'],
                "status": data['status']
            }
        }
    )

    return jsonify({
        "message": "Task Updated Successfully"
    })

# -----------------------------------
# DELETE TASK
# -----------------------------------
@task_bp.route('/tasks/<id>', methods=['DELETE'])
def delete_task(id):

    tasks.delete_one({
        "_id": ObjectId(id)
    })

    return jsonify({
        "message": "Task Deleted Successfully"
    })