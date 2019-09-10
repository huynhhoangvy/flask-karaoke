import os
from flask import Flask, jsonify, request, render_template
from flask_migrate import Migrate
from flask_login import login_user, login_required, logout_user, LoginManager, UserMixin, current_user
from flask_apscheduler import APScheduler
from flask_cors import CORS

from models.karaoke import db, User, Song
from components.users import users_blueprint
from components.songs import songs_blueprint

app = Flask(__name__)

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

CORS(app)

# POSTGRES = {
#     'user': os.environ['POSTGRES_USER'],
#     'pw': os.environ['POSTGRES_PWD'],
#     'db': os.environ['POSTGRES_DB'],
#     'host': os.environ['POSTGRES_HOST'],
#     'port': os.environ['POSTGRES_PORT'],
# }

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://lqymamquruhlvj:c88bd52ca2cc03cf00d5fa1fbb9bb8a3ee1234878b9caa31ab5ea481e459cb6a@ec2-54-221-212-126.compute-1.amazonaws.com:5432/d9ll967ioeotcp'
# app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://%(user)s:%(pw)s@%(host)s:%(port)s/%(db)s' % POSTGRES

app.config['SECRET_KEY'] = 'karaokesecretkey'

db.init_app(app)

migrate = Migrate(app, db, compare_type=True)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view ='login'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

scheduler = APScheduler()

scheduler.start()

# set POSTGRES_USER=postgres
# set POSTGRES_PWD=301194
# set POSTGRES_DB=karaoke
# set POSTGRES_HOST=localhost
# set POSTGRES_PORT=5432

@app.route('/')
def default():
    return 'Welcome!!'

@app.route('/home')
def home():
    return render_template('base.html')

app.register_blueprint(users_blueprint, url_prefix='/users')
app.register_blueprint(songs_blueprint, url_prefix='/songs')
