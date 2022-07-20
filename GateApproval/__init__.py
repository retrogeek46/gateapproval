import os
from flask import Flask
# from dotenv import load_dotenv, find_dotenv
# from decouple import config
from flask_cors import CORS
from GateApproval.db import db_session

def create_app(test_config=None):
    """
    This method is the entry point for the application

    Args:
        test_config ([type], optional): [description]. Defaults to None.

    Returns:
        [type]: [description]
    """
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.debug = False
    # app.config.from_mapping(
    #     SECRET_KEY=config('FLASK_SECRET_KEY')
    # )
    cors = CORS(app)
    app.config['CORS_HEADERS'] = 'Content-Type'

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    from . import logger
    from .db import init_db
    init_db()
    logger.init_app()
    # logger.error(config('FLASK_SECRET_KEY'))

    from . import api
    app.register_blueprint(api.bp)

    @app.route('/')
    def index():
        return 'Hello'

    @app.teardown_appcontext
    def shutdown_session(exception=None):
        db_session.remove()
    
    return app

