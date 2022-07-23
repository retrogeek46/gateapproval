from ctypes import util
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

from . import logger, utils
import os
ROOT_DIR = os.path.abspath(os.curdir)
db_conn_str = 'sqlite:///' + ROOT_DIR + '/db.db'
# engine = create_engine(utils.get_config_value('DB_CONN_STR'), convert_unicode=True)
engine = create_engine(db_conn_str, convert_unicode=True)
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
