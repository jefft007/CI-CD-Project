from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_bcrypt import Bcrypt
from pymongo import MongoClient
from bson.objectid import ObjectId
import os
import jwt
import datetime
from functools import wraps

app = Flask(__name__)

# Enable CORS
CORS(app)
bcrypt = Bcrypt(app)

app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'my-super-secret-key')

# ----------------------------------------
# MongoDB Atlas Connection
# ----------------------------------------
client = MongoClient(
    "mongodb+srv://jefft1260_db_user:Jeff123@cluster0.qvtk6ar.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
)

# Database
db = client["taskdb"]

# Collections
tasks = db["tasks"]
users = db["users"]

# ----------------------------------------
# AUTH MIDDLEWARE
# ----------------------------------------
def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        if 'Authorization' in request.headers:
            parts = request.headers['Authorization'].split()
            if len(parts) == 2 and parts[0] == 'Bearer':
                token = parts[1]
        
        if not token:
            return jsonify({'message': 'Token is missing!'}), 401

        try:
            data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=["HS256"])
            current_user = users.find_one({"_id": ObjectId(data['user_id'])})
            if not current_user:
                return jsonify({'message': 'User not found!'}), 401
        except Exception as e:
            return jsonify({'message': 'Token is invalid!'}), 401

        return f(current_user, *args, **kwargs)
    return decorated

# ----------------------------------------
# AUTH ENDPOINTS
# ----------------------------------------
@app.route('/signup', methods=['POST'])
def signup():
    data = request.json
    email = data.get('email')
    password = data.get('password')
    
    if not email or not password:
        return jsonify({'message': 'Email and password required'}), 400
        
    if users.find_one({"email": email}):
        return jsonify({'message': 'User already exists'}), 400
        
    hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
    users.insert_one({
        "email": email,
        "password": hashed_password
    })
    
    return jsonify({'message': 'User registered successfully'})

@app.route('/login', methods=['POST'])
def login():
    data = request.json
    email = data.get('email')
    password = data.get('password')
    
    user = users.find_one({"email": email})
    
    if user and bcrypt.check_password_hash(user['password'], password):
        token = jwt.encode({
            'user_id': str(user['_id']),
            'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=24)
        }, app.config['SECRET_KEY'], algorithm="HS256")
        
        return jsonify({'token': token})
        
    return jsonify({'message': 'Invalid credentials'}), 401

@app.route('/forgot-password', methods=['POST'])
def forgot_password():
    data = request.json
    email = data.get('email')
    
    user = users.find_one({"email": email})
    if not user:
        return jsonify({'message': 'If that email exists, a reset link has been sent.'}), 200
        
    reset_token = jwt.encode({
        'reset_password': str(user['_id']),
        'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=1)
    }, app.config['SECRET_KEY'], algorithm="HS256")
    
    # In a real app, send an email here using smtplib or a service
    print(f"Mock Email Sent to {email}")
    print(f"Reset Link: http://localhost:4200/reset-password?token={reset_token}")
    
    return jsonify({'message': 'If that email exists, a reset link has been sent.'})

@app.route('/reset-password', methods=['POST'])
def reset_password():
    data = request.json
    token = data.get('token')
    new_password = data.get('password')
    
    if not token or not new_password:
        return jsonify({'message': 'Token and new password required'}), 400
        
    try:
        data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=["HS256"])
        user_id = data.get('reset_password')
        
        if not user_id:
            return jsonify({'message': 'Invalid token'}), 400
            
        hashed_password = bcrypt.generate_password_hash(new_password).decode('utf-8')
        users.update_one(
            {"_id": ObjectId(user_id)},
            {"$set": {"password": hashed_password}}
        )
        return jsonify({'message': 'Password has been reset successfully'})
    except jwt.ExpiredSignatureError:
        return jsonify({'message': 'Reset token expired'}), 400
    except jwt.InvalidTokenError:
        return jsonify({'message': 'Invalid reset token'}), 400

# ----------------------------------------
# HOME ROUTE
# ----------------------------------------
@app.route('/')
def home():
    return jsonify({
        "message": "Task API Running Successfully on Render 🚀"
    })

# ----------------------------------------
# TASK ENDPOINTS (Protected)
# ----------------------------------------
@app.route('/tasks', methods=['GET'])
@token_required
def get_tasks(current_user):
    all_tasks = []
    for task in tasks.find({"user_id": str(current_user['_id'])}):
        task['_id'] = str(task['_id'])
        all_tasks.append(task)
    return jsonify(all_tasks)

@app.route('/tasks', methods=['POST'])
@token_required
def add_task(current_user):
    data = request.json
    new_task = {
        "title": data.get('title'),
        "status": data.get('status'),
        "user_id": str(current_user['_id'])
    }
    tasks.insert_one(new_task)
    return jsonify({"message": "Task Added Successfully"})

@app.route('/tasks/<id>', methods=['PUT'])
@token_required
def update_task(current_user, id):
    data = request.json
    result = tasks.update_one(
        {"_id": ObjectId(id), "user_id": str(current_user['_id'])},
        {"$set": {
            "title": data.get('title'),
            "status": data.get('status')
        }}
    )
    if result.matched_count == 0:
        return jsonify({"message": "Task not found or unauthorized"}), 404
    return jsonify({"message": "Task Updated Successfully"})

@app.route('/tasks/<id>', methods=['DELETE'])
@token_required
def delete_task(current_user, id):
    result = tasks.delete_one({
        "_id": ObjectId(id),
        "user_id": str(current_user['_id'])
    })
    if result.deleted_count == 0:
        return jsonify({"message": "Task not found or unauthorized"}), 404
    return jsonify({"message": "Task Deleted Successfully"})

# ----------------------------------------
# RUN FLASK APP
# ----------------------------------------
if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(
        host='0.0.0.0',
        port=port
    )