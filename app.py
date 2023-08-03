from flask import Flask, request, jsonify
import os
import mysql.connector

app = Flask(__name__)

# Get MySQL credentials from environment variable
JAWSDB_URL = os.environ.get('JAWSDB_URL')

# Function to create and return a database connection
def get_db_connection():
    return mysql.connector.connect(pool_name='my_pool', pool_size=5, **JAWSDB_URL)

# Endpoint to add a new task to the database
@app.route('/api/tasks', methods=['POST'])
def add_task():
    data = request.json
    task_name = data.get('taskName')
    task_status = data.get('taskStatus')

    # Insert the new task into the database
    connection = get_db_connection()
    cursor = connection.cursor()
    add_task_query = "INSERT INTO tasks (task_name, task_status) VALUES (%s, %s)"
    cursor.execute(add_task_query, (task_name, task_status))
    connection.commit()
    cursor.close()
    connection.close()

    return jsonify({'message': 'Task added successfully'}), 201

# Endpoint to fetch all tasks from the database
@app.route('/api/tasks', methods=['GET'])
def get_tasks():
    # Fetch all tasks from the database
    connection = get_db_connection()
    cursor = connection.cursor()
    get_tasks_query = "SELECT * FROM tasks"
    cursor.execute(get_tasks_query)
    tasks = [{'id': task[0], 'taskName': task[1], 'taskStatus': task[2]} for task in cursor.fetchall()]
    cursor.close()
    connection.close()

    return jsonify({'tasks': tasks})

if __name__ == '__main__':
    app.run()



