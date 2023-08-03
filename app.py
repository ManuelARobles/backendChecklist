import os
from mysql import connector
from flask import Flask, request, jsonify

app = Flask(__name__)

# Get the JAWSDB_URL
db_url = os.environ.get('JAWSDB_URL')

# Function for database connection
def get_db_connection():
    return connector.connect(url=db_url)

# Endpoint to add task to database
@app.route('/api/tasks', methods=['POST'])
def add_task():
    data = request.json
    task_name = data.get('taskName')
    task_status = data.get('taskStatus')

    # Insert new task into database
    connection = get_db_connection()
    cursor = connection.cursor()
    add_task_query = "INSERT INTO tasks (task_name, task_status) VALUES (%s, %s)"
    cursor.execute(add_task_query, (task_name, task_status))
    connection.commit()
    cursor.close()
    connection.close()

    return jsonify({'message': 'Task added successfully'}), 201

# Endpoint to fetch all tasks from database
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

