# import models

from flask import Flask, jsonify, request, render_template, redirect, url_for, flash, Blueprint, current_app
from flask_login import login_user, logout_user, current_user
from itsdangerous import URLSafeTimedSerializer
from werkzeug.security import generate_password_hash
import jwt
import datetime
from functools import wraps
import uuid

from models.karaoke import db, User, Token

users_blueprint = Blueprint('users', __name__)

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None

        if 'x-access-token' in request.headers:
            token = request.headers['x-access-token']

        if not token: 
            return jsonify({
                'status': 'fail', 
                'message': 'Token is missing'
                }), 401
        
        try:
            data = jwt.decode(token, current_app.config['SECRET_KEY'])
            current_user = User.query.filter_by(public_id=data['public_id']).first()
        except:
            return jsonify({
                'status': 'fail', 
                'message': 'Token is invalid!'
                }), 401

        return f(current_user, *args, **kwargs)

    return decorated

@users_blueprint.route('/register', methods=['get', 'post'])
def register():
    user = User.query.filter_by(username=request.json['username']).first()

    if user:
        return jsonify({
            'status': 'fail', 
            'message': 'Username has been exist'
        })

    new_user = User(public_id=str(uuid.uuid4()),
                    username=request.json['username'],
                    password=request.json['password'],
                    email=request.json['email'])
                    

    new_user.set_password(request.json['password'])

    db.session.add(new_user)
    db.session.commit()

    return jsonify({
        'status': 'success', 
        'message': 'Done signing up'
        })

@users_blueprint.route('/login', methods=['post'])
def login():
    log_user = User.query.filter_by(username=request.json['username']).first()

    if log_user is None:
        return jsonify({
            'status': 'fail', 
            'message': "username doesn't exist!!"
            })


    if not log_user.check_password(request.json['password']):
        return jsonify({
            'status': 'fail', 
            'message': 'wrong password'
            })
    
    login_user(log_user)

    if log_user.token:
        token = log_user.token.token

    else: 
        token = jwt.encode({'public_id': log_user.public_id, 'exp': datetime.datetime.utcnow() + datetime.timedelta(weeks=1)}, current_app.config['SECRET_KEY'])
        token = token.decode('UTF-8')
        new_token = Token(user_id=log_user.id, token=token)
        db.session.add(new_token)
        db.session.commit()

    return jsonify({
        'status': 'success', 
        'message': 'login successfully', 
        'username': log_user.username, 
        'token': token})

@users_blueprint.route('/logout', methods=['GET'])
@token_required
def logout(current_user):
    logout_user()
    token = current_user.token
    
    db.session.delete(token)
    db.session.commit()

    return jsonify({
        'status': 'success', 
        'message': 'logged out'
        })

@users_blueprint.route('/current', methods=['GET'])
@token_required
def current(current_user):
    login_user(current_user)
    return jsonify({
        'status': 'success', 
        'message': 'log in successfully', 
        'user': current_user.username
        })