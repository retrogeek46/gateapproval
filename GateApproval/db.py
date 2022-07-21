from ctypes import util
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

from . import logger, utils
import os

engine = create_engine(utils.get_config_value('DB_CONN_STR'), convert_unicode=True)
db_session = scoped_session(sessionmaker(autocommit=False,
                                         autoflush=False,
                                         bind=engine))
Base = declarative_base()
Base.query = db_session.query_property()

def init_db():
    import GateApproval.models
    Base.metadata.create_all(bind=engine)


def clear_db():
    Base.metadata.drop_all(bind=engine)
