from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

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
    todo = Todo(description=request.form.get('description'))
    try:
        db.session.add(todo)
        db.session.commit()
    except:
        db.session.rollback()
    finally:
        db.session.close()
        return redirect(url_for('index'))