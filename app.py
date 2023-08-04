import os
from flask import Flask, request, jsonify
#from flask_mysql_connector import MySQL, Params
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

app = Flask(__name__)

# Get the JAWSDB_URL from environment variables
db_url = os.environ.get('JAWSDB_URL')

# Configure the MySQL connection
#app.config['SQLALCHEMY_DATABASE_URI'] = db_url
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://wkxbnldfzj6jvjs5:d86wgakop2kdfxpj@wb39lt71kvkgdmw0.cbetxkdyhwsb.us-east-1.rds.amazonaws.com:3306/yyw0pmpuv1euqny3'

db = SQLAlchemy(app)
ma = Marshmallow(app)
#app.config[Params.MYSQL_HOST] = 'wb39lt71kvkgdmw0.cbetxkdyhwsb.us-east-1.rds.amazonaws.com'
#app.config[Params.MYSQL_USER] = 'wkxbnldfzj6jvjs5'
#app.config[Params.MYSQL_PASSWORD] = 'd86wgakop2kdfxpj'
#app.config[Params.MYSQL_DATABASE] = 'yyw0pmpuv1euqny3'

#connection = mysql.connector.connect(user='wkxbnldfzj6jvjs5',
#                                     password= 'd86wgakop2kdfxpj' ,
#                                     host='wb39lt71kvkgdmw0.cbetxkdyhwsb.us-east-1.rds.amazonaws.com' ,
#                                     database='yyw0pmpuv1euqny3' )


# Create the MySQL object
#mysql = MySQL(app)

# CREATE TASK TABLE
class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    status = db.Column(db.String(100))

    def __init__(self, name, status):
        self.name = name 
        self.status = status
    
class TaskSchema(ma.Schema):
    class Meta:
        fields = ('id', 'name', 'status')

task_schema = TaskSchema()
tasks_schema = TaskSchema(many=True)

# Endpoint to add a new task to the database
@app.route('/api/tasks', methods=['POST'])
def add_task():
    data = request.json
    task_name = data.get('taskName')
    task_status = data.get('taskStatus')

    new_task = Task(task_name, task_status)
    db.session.add(new_task)
    db.session.commit()
    

    # Insert the new task into the database
    #cursor = mysql.new_cursor()
    #add_task_query = "INSERT INTO tasks (task_name, task_status) VALUES (%s, %s)"
    #cursor.execute(add_task_query, (task_name, task_status))
    #mysql.connection.commit()
    #cursor.close()

    return jsonify({'message': 'Task added successfully'}), 201

# Endpoint to fetch all tasks from the database
@app.route('/api/tasks', methods=['GET'])
def get_tasks():
    tasks = Task.query.all()
    return jsonify(tasks_schema.dump(tasks))
    # Fetch all tasks from the database
    #cursor = mysql.new_cursor(dictionary=True)
   # get_tasks_query = "SELECT * FROM tasks"
    #cursor.execute(get_tasks_query)
   # tasks = [{'id': task[0], 'taskName': task[1], 'taskStatus': task[2]} for task in cursor.fetchall()]
   # cursor.close()


    return jsonify({'tasks': tasks})

if __name__ == '__main__':
    app.run()




