"""
This file initializes logging for the whole application/service
"""
import logging
from flask import Flask

app = Flask(__name__)


def init_app():
    if __name__ != 'VendorRating.logger':
        gunicorn_logger = logging.getLogger('gunicorn.error')
        tf_logger = logging.getLogger('tensorflow')
        tf_logger.setLevel(logging.ERROR)
        app.logger.handlers = gunicorn_logger.handlers
        app.logger.setLevel(gunicorn_logger.level)


def debug(*messages):
    """
    Log debug messages
    
    Args:
        messages: The message
    """
    app.logger.debug(*messages)


def info(*messages):
    """
    Log info messages
    
    Args:
        messages: The message
    """
    app.logger.info(*messages)


def warning(*messages):
    """
    Log warning messages
    
    Args:
        messages: The message
    """
    app.logger.warning(*messages)


def error(*messages):
    """
    Log error messages
    
    Args:
        messages: The message
    """
    app.logger.error(*messages)


def critical(*messages):
    """
    Log critical messages
    
    Args:
        messages: The message
    """
    app.logger.critical(*messages)
