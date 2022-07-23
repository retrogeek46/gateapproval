"""
This file loads the application/service based on parameters given in cli
"""
from setuptools import setup

setup(
    name='GateApproval',
    packages=['GateApproval'],
    include_package_data=True,
    install_requires=[
        'Flask==2.1.3', 'Flask-Cors==3.0.10', 'PyJWT==2.0.1',
        'pandas==1.4.3', 'requests==2.28.1', 'SQLAlchemy==1.4.39',
        'deepface==0.0.75', 'gunicorn==20.1.0', 'bcrypt==3.2.2']
)