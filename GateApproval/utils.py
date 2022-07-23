from logging import raiseExceptions
import traceback
import jwt
import requests
import os
import json
import gzip
from flask import g
from . import db, logger
import pandas as pd
from datetime import datetime, timedelta
import bcrypt
from deepface import DeepFace
import uuid

def get_config_value(key):
    """
    This method returns value for specific key from environment config file

    Args:
        key (string): Key for which value is to be returned

    Returns:
        string: value for given key
    """
    configFilePath = 'config.json'
    try:
        if os.path.exists(configFilePath):
            with open(configFilePath) as json_file:
                configJson = json.load(json_file)
                return configJson[key]
    except:
        logger.error(traceback.format_exc())
        return ''

def create_hashed_password(password):
    salt = bcrypt.gensalt()
    hashed_pass = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed_pass

def verify_password(password, hash):
    print(password, hash)
    return bcrypt.checkpw(password.encode('utf-8'), hash)

def save_visitor_files(name, visitor, document):
    file_path = get_config_value("FILE_PATH")
    if not os.path.exists(file_path):
        os.makedirs(file_path)
    uuid_str = uuid.uuid4().hex
    document_name = ''
    visitor_name = file_path + '/{}-vis-{}.jpg'.format(name, uuid_str)
    visitor.save(visitor_name)
    if document:
        document_name = file_path + '/{}-doc-{}.jpg'.format(name, uuid_str)    
        document.save(document_name)
    
    return document_name, visitor_name

def compare_faces_deepface(document, visitor):
    verify_result = DeepFace.verify(document, visitor)
    return verify_result

def find_faces_deepface(visitor):
    find_result = DeepFace.find(img_path=visitor, db_path=get_config_value('FACE_DB_PATH'), enforce_detection=False)
    return find_result

def get_verifier_id_from_jwt(headers):
    token = headers.get('Authorization').split(' ')[1]
    data = jwt.decode(token, get_config_value(
                'JWT_SECRET_KEY'), algorithms=["HS256"])
    return data['id']

# def compare_faces_face_recognition(document, visitor):
#     document = 