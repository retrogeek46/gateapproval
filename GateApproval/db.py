from ctypes import util
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

from . import logger, utils
import os

# basedir = os.path.abspath(os.path.dirname(__file__))
# engine = create_engine('sqlite:///'+ basedir + '/test.db', convert_unicode=True)
engine = create_engine(utils.get_config_value('DB_CONN_STR'), convert_unicode=True)
db_session = scoped_session(sessionmaker(autocommit=False,
                                         autoflush=False,
                                         bind=engine))
Base = declarative_base()
Base.query = db_session.query_property()

def init_db():
    # import all modules here that might define models so that
    # they will be registered properly on the metadata.  Otherwise
    # you will have to import them first before calling init_db()
    import GateApproval.models
    Base.metadata.create_all(bind=engine)


def clear_db():
    Base.metadata.drop_all(bind=engine)