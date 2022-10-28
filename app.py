from flask import Flask, render_template

#============ FLASK CONFIGURATION ==========================#
app = Flask(__name__)


#=========== ROUTES =========================================#
@app.route('/')
def index():
    return render_template('index.html', data=[
        {'description': 'Todo1'},
        {'description': 'Todo2'},
        {'description': 'Todo3'},
        {'description': 'Todo4'}
    ])
