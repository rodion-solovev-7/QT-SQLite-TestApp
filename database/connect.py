from sqlalchemy import create_engine, event
from sqlalchemy.engine import Engine
from sqlalchemy.orm import scoped_session, sessionmaker

from database.models import metadata


@event.listens_for(Engine, "connect")
def set_sqlite_pragma(dbapi_connection, connection_record):
    """enable support foreign keys for sqlite"""
    cursor = dbapi_connection.cursor()
    cursor.execute("PRAGMA foreign_keys=ON")
    cursor.close()


dbecho = False

connection_string = f"sqlite:///test_db.sqlite"
engine = create_engine(connection_string, echo=dbecho)

make_session = scoped_session(
    sessionmaker(bind=engine,
                 autocommit=False,
                 autoflush=False,
                 expire_on_commit=True))

# clear tables from db
# metadata.drop_all(engine)

# create tables if not exists
metadata.create_all(engine)
