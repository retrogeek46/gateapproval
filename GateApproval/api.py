import base64
from time import time
import bcrypt
from flask import Blueprint, request
from flask_cors import cross_origin
from datetime import datetime, timedelta
import json
import requests
import os
import jwt
from functools import wraps
from pprint import pprint
import traceback
from . import logger, db, utils
from .db import db_session
from .models import User


bp = Blueprint('api', __name__, url_prefix='/api')


def token_required(f):
    """
    This method acts as a middleware and validates + extracts data from the jwt

    Args:
        f (request): The request object

    Returns:
        object: The request object with modifications
    """
    @wraps(f)
    def decorated(*args, **kwargs):
        try:
            token = request.headers.get('Authorization').split(' ')[1]
            if not token:
                return {'message': 'Token is missing!'}, 403
            # logger.error(config('FLASK_SECRET_KEY'))
            data = jwt.decode(token, utils.get_config_value(
                'JWT_SECRET_KEY'), algorithms=["HS256"])
            if request.json is None:
                request.data = {}
            request.json['clientID'] = data['clientID']
            request.json['userID'] = data['userID']
        except Exception as e:
            logger.error(traceback.format_exc())
            return {'message': 'Token is invalid!'}, 403
        return f(*args, **kwargs)
    return decorated


@bp.route('/login', methods=['POST'])
@cross_origin()
def login():
    """
    This api logs in user based on loginID and password

    Returns:
        response: Client details and jwt upon successful login
    """
    result = ''
    try:
        user = User.query.filter(User.email==request.json["email"]).first()
        if user and utils.verify_password(request.json["password"], user.password):
            token = jwt.encode({'id': user.id, 'exp': datetime.utcnow() + 
                                timedelta(days=1)}, utils.get_config_value('JWT_SECRET_KEY'))
            result = {
                "name": user.name,
                "token": token
            }
            return {'message': result}, 200
        return {'message': 'Invalid Credentials'}
    except Exception as e:
        logger.error(traceback.format_exc())
        return {'message': 'Could not process request due to error in server'}, 500

@bp.route('/verify_visitor', methods=['POST'])
@cross_origin()
def verify_visitor():
    """
    This api logs in user based on loginID and password

    Returns:
        response: Client details and jwt upon successful login
    """
    try:
        name = request.form['name']
        document_file = request.files['document']
        visitor_file = request.files['visitor']
        
        document_path, visitor_path = utils.save_visitor_files(name, document_file, visitor_file)

        verify_result = utils.compare_faces_deepface(document_path, visitor_path)
        return {'message': 'Verified' if verify_result['verified'] else 'Unverified'}
    except Exception as e:
        logger.error(traceback.format_exc())
        return {'message': 'Could not process request due to error in server'}, 500


@bp.route('/test_api', methods=['POST'])
@cross_origin()
# @token_required
def test_api():
    return "Hello World"


@bp.route('/create_user', methods=['POST'])
@cross_origin()
# @token_required
def create_user():
    try:
        name = request.json["name"]
        email = request.json["email"]
        password = request.json["password"]
        role = request.json["role"]
        
        hashed_pass = utils.create_hashed_password(password)
        
        u = User(name, email, role, hashed_pass)
        db_session.add(u)
        db_session.commit()
        
        return "User {} created".format(name)
    except:
        return "Error: {}".format(traceback.format_exc())


@bp.route('/get_users', methods=['POST'])
@cross_origin()
# @token_required
def get_users():
    try:
        users = User.query.all()
        users_response = []
        for user in users:
            users_response.append({'id': user.id, 'name': user.name, 'email': user.email})
        print(users_response)
        return {'message':users_response}
    except:
        return "Error: {}".format(traceback.format_exc())
        

# TODO: remove in prod
@bp.route('/clear_db', methods=['POST'])
@cross_origin()
# @token_required
def clear_db():
    db.clear_db()
    return "DB Cleared"

