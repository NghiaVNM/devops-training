from flask import Flask, request, jsonify
from pymongo import MongoClient
from prometheus_client import Counter, Histogram, generate_latest, CONTENT_TYPE_LATEST
import time
import os
import logging
from dotenv import load_dotenv
from datetime import datetime
import json

load_dotenv()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)

REQUEST_COUNT = Counter('http_requests_total', 'Total HTTP requests', ['method', 'endpoint', 'status_code'])
REQUEST_DURATION = Histogram('http_request_duration_seconds', 'HTTP request duration', ['method', 'endpoint'])
DB_OPERATIONS = Counter('mongodb_operations_total', 'Total MongoDB operations', ['operation', 'collection'])
DB_ERRORS = Counter('mongodb_errors_total', 'Total MongoDB errors', ['operation', 'error_type'])

try:
  mongo_uri = os.getenv('MONGODB_URI', 'mongodb://admin:adminpassword@mongodb:27017')
  client = MongoClient(mongo_uri)
  db = client[os.getenv('MONGODB_DATABASE', 'myapp')]
  users_collection = db[os.getenv('MONGODB_COLLECTION', 'users')]
  
  client.admin.command('ping')
  logger.info("Connected to MongoDB successfully")
except Exception as e:
  logger.error(f"Failed to connect to MongoDB: {e}")
  client = None

@app.before_request
def before_request():
  request.start_time = time.time()

@app.after_request
def after_request(response):
  request_duration = time.time() - request.start_time
  
  REQUEST_COUNT.labels(
    method=request.method,
    endpoint=request.endpoint or 'unknown',
    status_code=response.status_code
  ).inc()
  
  REQUEST_DURATION.labels(
    method=request.method,
    endpoint=request.endpoint or 'unknown'
  ).observe(request_duration)
  
  response.headers['X-Response-Time'] = f"{request_duration:.4f}s"
  
  return response

@app.route('/')
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'app': os.getenv('APP_NAME', 'python-web-app'),
        'version': os.getenv('APP_VERSION', '1.0.0'),
        'timestamp': datetime.utcnow().isoformat()
    })

@app.route('/users', methods=['GET'])
def get_users():
  """Get all users from MongoDB"""
  try:
    if not client:
      return jsonify({'error': 'Database connection not available'}), 503
    
    DB_OPERATIONS.labels(operation='find', collection='users').inc()
    
    users = list(users_collection.find({}, {'_id': 0}))
    return jsonify({
      'users': users,
      'count': len(users),
      'timestamp': datetime.utcnow().isoformat()
    })
  except Exception as e:
    DB_ERRORS.labels(operation='find', error_type=type(e).__name__).inc()
    logger.error(f"Error fetching users: {e}")
    return jsonify({'error': 'Failed to fetch users'}), 500

@app.route('/users', methods=['POST'])
def create_user():
  """Create a new user"""
  try:
    if not client:
      return jsonify({'error': 'Database connection not available'}), 503
    
    data = request.get_json()
    if not data or 'name' not in data or 'email' not in data:
      return jsonify({'error': 'Name and email are required'}), 400
    
    user = {
      'name': data['name'],
      'email': data['email'],
      'created': datetime.utcnow(),
      'updated': datetime.utcnow()
    }
    
    DB_OPERATIONS.labels(operation='insert', collection='users').inc()
    result = users_collection.insert_one(user)
    
    user['_id'] = str(result.inserted_id)
    return jsonify({
      'message': 'User created successfully',
      'user': user
    }), 201
      
  except Exception as e:
    DB_ERRORS.labels(operation='insert', error_type=type(e).__name__).inc()
    logger.error(f"Error creating user: {e}")
    return jsonify({'error': 'Failed to create user'}), 500

@app.route('/users/<user_id>', methods=['GET'])
def get_user(user_id):
  """Get a specific user by ID"""
  try:
    if not client:
      return jsonify({'error': 'Database connection not available'}), 503
  
    from bson import ObjectId
    
    DB_OPERATIONS.labels(operation='findone', collection='users').inc()
    user = users_collection.find_one({'_id': ObjectId(user_id)}, {'_id': 0})
    
    if not user:
      return jsonify({'error': 'User not found'}), 404
  
    return jsonify({
      'user': user,
      'timestamp': datetime.utcnow().isoformat()
    })
      
  except Exception as e:
    DB_ERRORS.labels(operation='findone', error_type=type(e).__name__).inc()
    logger.error(f"Error fetching user {user_id}: {e}")
    return jsonify({'error': 'Failed to fetch user'}), 500

@app.route('/slow')
def slow_endpoint():
  """Simulate a slow endpoint for monitoring"""
  import random
  sleep_time = random.uniform(1, 3)
  time.sleep(sleep_time)
  
  return jsonify({
    'message': 'This was a slow operation',
    'sleep_time': sleep_time,
    'timestamp': datetime.utcnow().isoformat()
  })

@app.route('/error')
def error_endpoint():
  """Simulate an error for monitoring"""
  import random
  
  error_codes = [400, 404, 500, 503]
  status_code = random.choice(error_codes)
  
  return jsonify({
    'error': f'Simulated error with status {status_code}',
    'timestamp': datetime.utcnow().isoformat()
  }), status_code

@app.route('/db-test')
def db_test():
  """Test database connectivity"""
  try:
    if not client:
      return jsonify({'error': 'Database connection not available'}), 503
  
    result = client.admin.command('ping')
    user_count = users_collection.count_documents({})
    
    return jsonify({
      'database': 'connected',
      'ping_result': result,
      'user_count': user_count,
      'timestamp': datetime.utcnow().isoformat()
    })
      
  except Exception as e:
    logger.error(f"Database test failed: {e}")
    return jsonify({
      'database': 'disconnected',
      'error': str(e),
      'timestamp': datetime.utcnow().isoformat()
      }), 500

@app.route('/metrics')
def metrics():
  """Prometheus metrics endpoint"""
  return generate_latest(), 200, {'Content-Type': CONTENT_TYPE_LATEST}

if __name__ == '__main__':
  port = int(os.getenv('FLASK_PORT', 5000))
  app.run(host='0.0.0.0', port=port, debug=os.getenv('FLASK_DEBUG', 'False').lower() == 'true')