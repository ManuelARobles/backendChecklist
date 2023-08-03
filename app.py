import os
from flask import Flask, request, jsonify
from flaskext.mysql import MySQL

app = Flask(__name__)

# Get the JAWSDB_URL from environment variables
db_url = os.environ.get('JAWSDB_URL')

# Configure the MySQL connection
app.config['MYSQL_DATABASE_HOST'] = db_url.split('@')[1].split('/')[0]
app.config['MYSQL_DATABASE_USER'] = db_url.split('://')[1].split(':')[0]
app.config['MYSQL_DATABASE_PASSWORD'] = db_url.split('://')[1].split(':')[1].split('@')[0].split(':')[1]
app.config['MYSQL_DATABASE_DB'] = db_url.split('/')[-1]

# Create the MySQL object
mysql = MySQL(app)

# Endpoint to add a new task to the database
@app.route('/api/tasks', methods=['POST'])
def add_task():
    data = request.json
    task_name = data.get('taskName')
    task_status = data.get('taskStatus')

    # Insert the new task into the database
    connection = mysql.connect()
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
    connection = mysql.connect()
    cursor = connection.cursor()
    get_tasks_query = "SELECT * FROM tasks"
    cursor.execute(get_tasks_query)
    tasks = [{'id': task[0], 'taskName': task[1], 'taskStatus': task[2]} for task in cursor.fetchall()]
    cursor.close()
    connection.close()

    return jsonify({'tasks': tasks})

if __name__ == '__main__':
    app.run()



