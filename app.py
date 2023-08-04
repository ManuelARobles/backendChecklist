import os
from flask import Flask, request, jsonify
from flask_mysql_connector import MySQL

app = Flask(__name__)

# Get the JAWSDB_URL from environment variables
db_url = os.environ.get('JAWSDB_URL')

# Configure the MySQL connection
app.config['MYSQL_DATABASE_HOST'] = 'wb39lt71kvkgdmw0.cbetxkdyhwsb.us-east-1.rds.amazonaws.com'
app.config['MYSQL_DATABASE_USER'] = 'wkxbnldfzj6jvjs5'
app.config['MYSQL_DATABASE_PASSWORD'] = 'd86wgakop2kdfxpj'
app.config['MYSQL_DATABASE_DB'] = 'yyw0pmpuv1euqny3'

# Create the MySQL object
mysql = MySQL(app)

# Endpoint to add a new task to the database
@app.route('/api/tasks', methods=['POST'])
def add_task():
    data = request.json
    task_name = data.get('taskName')
    task_status = data.get('taskStatus')

    # Insert the new task into the database
    cursor = mysql.connection.cursor()
    add_task_query = "INSERT INTO tasks (task_name, task_status) VALUES (%s, %s)"
    cursor.execute(add_task_query, (task_name, task_status))
    mysql.connection.commit()
    cursor.close()

    return jsonify({'message': 'Task added successfully'}), 201

# Endpoint to fetch all tasks from the database
@app.route('/api/tasks', methods=['GET'])
def get_tasks():
    # Fetch all tasks from the database
    cursor = mysql.connection.cursor()
    get_tasks_query = "SELECT * FROM tasks"
    cursor.execute(get_tasks_query)
    tasks = [{'id': task[0], 'taskName': task[1], 'taskStatus': task[2]} for task in cursor.fetchall()]
    cursor.close()

    return jsonify({'tasks': tasks})

if __name__ == '__main__':
    app.run()




