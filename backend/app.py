from flask import Flask, request, jsonify
from flask_cors import CORS
from pymongo import MongoClient
from bson.objectid import ObjectId
import os

app = Flask(__name__)

# Enable CORS
CORS(app)

# ----------------------------------------
# MongoDB Atlas Connection
# ----------------------------------------
client = MongoClient(
    "mongodb+srv://jefft1260_db_user:Jeff123@cluster0.qvtk6ar.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
)

# Database
db = client["taskdb"]

# Collection
tasks = db["tasks"]

# ----------------------------------------
# HOME ROUTE
# ----------------------------------------
@app.route('/')
def home():
    return jsonify({
        "message": "Task API Running Successfully on Render 🚀"
    })

# ----------------------------------------
# GET ALL TASKS
# ----------------------------------------
@app.route('/tasks', methods=['GET'])
def get_tasks():

    all_tasks = []

    for task in tasks.find():

        task['_id'] = str(task['_id'])

        all_tasks.append(task)

    return jsonify(all_tasks)

# ----------------------------------------
# ADD TASK
# ----------------------------------------
@app.route('/tasks', methods=['POST'])
def add_task():

    data = request.json

    new_task = {
        "title": data.get('title'),
        "status": data.get('status')
    }

    tasks.insert_one(new_task)

    return jsonify({
        "message": "Task Added Successfully"
    })

# ----------------------------------------
# UPDATE TASK
# ----------------------------------------
@app.route('/tasks/<id>', methods=['PUT'])
def update_task(id):

    data = request.json

    tasks.update_one(
        {"_id": ObjectId(id)},
        {
            "$set": {
                "title": data.get('title'),
                "status": data.get('status')
            }
        }
    )

    return jsonify({
        "message": "Task Updated Successfullyy"
    })

# ----------------------------------------
# DELETE TASK
# ----------------------------------------
@app.route('/tasks/<id>', methods=['DELETE'])
def delete_task(id):

    tasks.delete_one({
        "_id": ObjectId(id)
    })

    return jsonify({
        "message": "Task Deleted Successfully"
    })

# ----------------------------------------
# RUN FLASK APP
# ----------------------------------------
if __name__ == '__main__':

    port = int(os.environ.get("PORT", 5000))

    app.run(
        host='0.0.0.0',
        port=port
    )