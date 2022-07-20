import base64
from time import time
import bcrypt
from cv2 import split
from flask import Blueprint, request, send_from_directory, url_for
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
from .models import User, Visitor


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
            jwt.decode(token, utils.get_config_value(
                'JWT_SECRET_KEY'), algorithms=["HS256"])
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


@bp.route('/add_visitor', methods=['POST'])
@cross_origin()
@token_required
def add_visitor():
    """
    This api logs in user based on loginID and password

    Returns:
        response: Client details and jwt upon successful login
    """
    try:
        name = request.form['name']
        verifier_id = utils.get_verifier_id_from_headers(request.headers)
        document_file = request.files['document']
        visitor_file = request.files['visitor']
        
        document_path, visitor_path = utils.save_visitor_files(name, document_file, visitor_file)

        verify_result = utils.compare_faces_deepface(document_path, visitor_path)['verified']
        
        print(name, verifier_id, False, verify_result, document_path, visitor_path)
        
        visitor = Visitor(name, verifier_id, False, verify_result, document_path, visitor_path)
        db_session.add(visitor)
        db_session.commit()
        
        return {'message': 'Visitor Added'}
    except Exception as e:
        logger.error(traceback.format_exc())
        return {'message': 'Could not process request due to error in server'}, 500


@bp.route('/get_visitors', methods=['GET'])
@cross_origin()
@token_required
def get_visitors():
    """
    This api logs in user based on loginID and password

    Returns:
        response: Client details and jwt upon successful login
    """
    try:
        visitors = Visitor.query.filter(Visitor.approval_status == 0)
        visitors_response = []
        for visitor in visitors:
            visitors_response.append({
                'id': visitor.id,
                'name': visitor.name,
                'verification_status': visitor.verification_status,
                'document': utils.get_config_value('SERVER_URL') + '/images/' + visitor.document_img_path.split('/')[-1],
                'visitor': utils.get_config_value('SERVER_URL') + '/images/' + visitor.visitor_img_path.split('/')[-1]
            })
        print(visitors_response)
        return {'message': visitors_response}
    except Exception as e:
        logger.error(traceback.format_exc())
        return {'message': 'Could not process request due to error in server'}, 500


@bp.route('/approve_visitors', methods=['POST'])
@cross_origin()
@token_required
def approve_visitors():
    """
    This api logs in user based on loginID and password

    Returns:
        response: Client details and jwt upon successful login
    """
    try:
        visitors = request.json["visitors"]
        status = request.json["status"]
        print(visitors)
        visitor_update = Visitor.query.filter(Visitor.id.in_(visitors)).update(dict(approval_status=status))
        db_session.commit()
        
        return {'message': '{} visitor(s) {}'.format(visitor_update, 'approved' if status else 'rejected')}
    except Exception as e:
        logger.error(traceback.format_exc())
        return {'message': 'Could not process request due to error in server'}, 500


@bp.route('/create_user', methods=['POST'])
@cross_origin()
def create_user():
    try:
        name = request.json["name"]
        email = request.json["email"]
        password = request.json["password"]
        role = request.json["role"]
        
        hashed_pass = utils.create_hashed_password(password)
        
        user = User(name, email, role, hashed_pass)
        db_session.add(user)
        db_session.commit()
        
        return {'message': 'User {} created'.format(name)}
    except:
        return "Error: {}".format(traceback.format_exc())


@bp.route('/get_users', methods=['GET'])
@cross_origin()
@token_required
def get_users():
    try:
        users = User.query.all()
        users_response = []
        for user in users:
            users_response.append({
                'id': user.id,
                'name': user.name,
                'email': user.email,
                'role': user.role
            })
        return {'message':users_response}
    except:
        return "Error: {}".format(traceback.format_exc())
        

# TODO: remove in prod
@bp.route('/clear_db', methods=['POST'])
@cross_origin()
@token_required
def clear_db():
    db.clear_db()
    return "DB Cleared"


@bp.route('/test_api', methods=['POST'])
@cross_origin()
# @token_required
def test_api():
    return "Hello World"

