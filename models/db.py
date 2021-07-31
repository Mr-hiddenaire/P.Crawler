from config import database
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

engine = create_engine('mysql+mysqlconnector://'+database.DB_USERNAME+':'+database.DB_PASSWORD+'@'+database.DB_HOST+':'+database.DB_PORT+'/'+database.DB_NAME+'', echo=True)
_SessionFactory = sessionmaker(bind=engine)

Base = declarative_base()

def session_factory():
    Base.metadata.create_all(engine)
    return _SessionFactory()

def to_dict(self):
    return {c.name: getattr(self, c.name, None) for c in self.__table__.columns}

Base.to_dict = to_dict