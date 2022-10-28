from flask import Flask, render_template, request, redirect, jsonify, abort
from flask_sqlalchemy import SQLAlchemy
import sys

#============ CONFIGURATIONS ==========================#
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] ='postgresql://jamal:0987jJ@localhost:5432/todoapp'
app.app_context().push()
db = SQLAlchemy(app)

#============ MODELS ==========================#

class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(), nullable=False)

    def __repr__(self):
        return f'<Todo id={self.id} description={self.description}>'

db.create_all()

#=========== CONTROLLERS =========================================#
@app.route('/')
def index():
    return render_template('index.html', data=Todo.query.all())

@app.route('/todos/create', methods=['POST'])
def create():
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