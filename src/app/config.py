import os
import sqlalchemy as db
from sqlalchemy_utils import create_database, database_exists
from sqlalchemy.orm import sessionmaker 

class Config:
    db_driver = str(os.getenv("DB_DRIVER"))
    db_user = str(os.getenv("DB_USER"))
    db_password = str(os.getenv("DB_PASSWORD"))
    db_host = str(os.getenv("DB_HOST"))
    db_port = str(os.getenv("DB_PORT"))
    db_name = str(os.getenv("DB_NAME"))
    db_debug = os.getenv("DB_DEBUG") if os.getenv("DB_DEBUG") is not None else False
    db_url = db_driver + '://' + db_user + ':' + db_password + '@' + db_host + ':' + db_port + '/' + db_name
    if not database_exists(db_url):
        create_database(db_url)
    db_engine = db.create_engine(db_url, echo=True if db_debug == 1 or db_debug == "yes" else False)
    db_session = sessionmaker(bind=db_engine)()

    def __init__(self):
        pass
