#!/usr/bin/python3
"""AirBnB cloned v2 data storage class"""
import os
from models.base_model import BaseModel, Base
from models.user import User
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.place import Place
from models.review import Review
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session


class DBStorage:
    """This class save instances to a mysql db and
    get instances from the db
    Attributes:
        __engine: create the interfaces of comunication with db
        __session: open a comunication with the db
    """
    __engine = None
    __session = None

    def __init__(self):
        """Initializes the SQL database storage"""
        user = os.getenv('HBNB_MYSQL_USER')
        pword = os.getenv('HBNB_MYSQL_PWD')
        host = os.getenv('HBNB_MYSQL_HOST')
        db_name = os.getenv('HBNB_MYSQL_DB')
        env = os.getenv('HBNB_ENV')
        DATABASE_URL = "mysql+mysqldb://{}:{}@{}/{}".format(
            user, pword, host, db_name
        )
        self.__engine = create_engine(
            DATABASE_URL,
            pool_pre_ping=True
        )
        if env == 'test':
            Base.metadata.drop_all(self.__engine)


    def all(self, cls=None):
        """Returns a dictionary of models currently in storage"""
        classes = {
               'BaseModel': BaseModel, 'User': User, 'Place': Place,
               'State': State, 'City': City, 'Amenity': Amenity,
               'Review': Review
              }
        temp_dict = {}
        """
        if cls:
            objects = self.__session.query(classes[cls]).all()"""
        if cls:
            if type(cls) is str:
                cls = eval(cls)
            objects = self.__session.query(cls).all()
        else:
            all_classes = list(classes.values())
            objects = []
            for c in all_classes:
                objects.extend(self.__session.query(c).all())
        for obj in objects:
            key = f"{obj.__class__.__name__}.{obj.id}"
            temp_dict[key] = obj
        return temp_dict

    def new(self, obj):
        """Adds new object to storage database"""
        if obj is not None:
            try:
                self.__session.add(obj)
                self.__session.flush()
                self.__session.refresh(obj)
            except Exception as ex:
                self.__session.rollback()
                raise ex

    def save(self):
        """commit all changes of the current database session"""
        self.__session.commit()

    def delete(self, obj=None):
        """ delete from the current database session"""
        if obj is not None:
            self.__session.query(type(obj)).filter(
                type(obj).id == obj.id).delete(
                synchronize_session=False
            )

    def reload(self):
        """ reload all the objs"""
        Base.metadata.create_all(self.__engine)
        Session = scoped_session(sessionmaker(
            bind=self.__engine, expire_on_commit=False))
        self.__session = Session()

    def close(self):
        """Close session"""
        self.__session.close()
