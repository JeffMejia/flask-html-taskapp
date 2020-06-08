from flask import Flask, request, jsonify, render_template, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

# Flask-SQLAlchemy integration requires marshmallow-sqlalchemy to be installed.

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://root@localhost/flaskmysql"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
ma = Marshmallow(app)


class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(30), unique=True)
    description = db.Column(db.String(150))
    author = db.Column(db.String(20))

    def __init__(self, title, description, author):
        self.title = title
        self.description = description
        self.author = author


db.create_all()


class TaskSchema(ma.Schema):
    class Meta:
        fields = ('id', 'title', 'description', 'author')


task_schema = TaskSchema()
tasks_schema = TaskSchema(many=True)


@app.route('/tasks', methods=['POST'])
def create_task():
    title = request.form['title']
    description = request.form['description']
    author = request.form['author']
    task = Task(title, description, author)

    db.session.add(task)
    db.session.commit()
    return get_tasks()


@app.route('/', methods=['GET'])
def index():
    return render_template('index.html', title="Main Page")


@app.route('/tasks', methods=['GET'])
def get_tasks():
    all_tasks = Task.query.all()
    result = tasks_schema.dump(all_tasks)
    return render_template('all_tasks.html', tasks=result, title="Task App")


@app.route('/task/<int:id>', methods=['GET'])
def get_task(id):
    task = Task.query.get(id)
    return render_template('edit_task.html', task=task, title="Edit Task")


@app.route('/edit/<int:id>', methods=['POST'])
def update_task(id):
    task = Task.query.get(id)

    title = request.form['title']
    description = request.form['description']
    author = request.form['author']

    task.title = title
    task.description = description
    task.author = author

    db.session.commit()
    return redirect('/tasks')


@app.route('/delete/<int:id>', methods=['POST'])
def delete_task(id):
    Task.query.filter_by(id=int(id)).delete()
    db.session.commit()
    return redirect('/tasks')


if __name__ == "__main__":
    app.run(debug=True, port=3000)


# pip install flask flask-sqlalchemy flask-marshmallow marshmallow-sqlalchemy pymysql
# pip install ng
# pip install Jinja2
