from flask import Flask, render_template

from src.common.database import Database

app = Flask(__name__)
app.config.from_object('config')
app.secret_key = 'some_secret'

@app.before_first_request
def init_db():
    Database.initialize()

@app.route('/')
def main_page():
    return render_template('main_page.html')


@app.route('/about')
def about():
    return render_template('about.html')


from src.models.users.views import user_blueprint
app.register_blueprint(user_blueprint, url_prefix='/users')

from src.models.exercises.views import exercise_blueprint
app.register_blueprint(exercise_blueprint, url_prefix='/exercises')

