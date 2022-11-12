from flask import Flask, render_template, request, redirect, jsonify, abort, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import sys

#============ CONFIGURATIONS ==========================#
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] ='postgresql://jamal:0987jJ@localhost:5432/todoapp'
app.app_context().push()
db = SQLAlchemy(app)
migrate = Migrate(app, db)

#============ MODELS ==========================#

class Todo(db.Model):
    __tablename__ = 'todos'
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(), nullable=False)
    completed = db.Column(db.Boolean(), nullable=False, default=False)
    list_id = db.Column(db.Integer, db.ForeignKey('todolists.id'), nullable=False)

    def __repr__(self):
        return f'<Todo id={self.id} description={self.description} list_id={self.list_id}>'

class TodoList(db.Model):
    __tablename__ = 'todolists'
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(), nullable=False)
    todos = db.relationship('Todo', backref='list', lazy=True)

    def __repr__(self):
        return f'<TodoList id={self.id} name={self.name}>'



#=========== CONTROLLERS =========================================#
@app.route('/')
def index():
    return redirect(url_for('get_todo_list', list_id=1))

@app.route('/lists/<list_id>')
def get_todo_list(list_id):
    return render_template('index.html', data=Todo.query.filter_by(list_id = list_id).order_by('id').all())

@app.route('/todos/create', methods=['POST'])
def create_todo():
    error = False
    body = {} # prevents detached session error
    try:
        todo = Todo(description=request.get_json()['description']) # get description from request
        db.session.add(todo)
        db.session.commit()
        body['description'] = todo.description # add description to body after successful commit
    except:
        db.session.rollback()
        error = True
        print(sys.exc_info()) # print the exception error message
    finally:
        db.session.close()  # close session
        if error:
            abort(400) # abort the request incase of an error
        else:
            return jsonify(body) # return the json response back to the client

@app.route('/todos/<todo_id>/set-completed', methods=['POST'])
def set_completed_todo(todo_id):
    try:
        todo = Todo.query.get(todo_id)
        todo.completed = request.get_json()['completed']
        db.session.commit()
    except:
        db.session.rollback()
    finally:
        db.session.close()
    return redirect(url_for('index'))

@app.route('/todos/<todo_id>', methods=['DELETE'])
def delete_todo(todo_id):
    try:
        db.session.delete(Todo.query.get(todo_id))
        db.session.commit()
    except:
        db.session.rollback()
    finally:
        db.session.close()
    return jsonify({'success': True})