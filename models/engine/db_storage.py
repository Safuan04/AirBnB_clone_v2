#!/usr/bin/python3
"""Defining a New Engine DBStorage"""
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
import os
from models.base_model import Base, BaseModel
from models.user import User
from models.place import Place
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.review import Review


class DBStorage():
    """Engine class DBStorage"""
    __engine = None
    __session = None

    def __init__(self):
        """Initialize engine"""
        user = os.getenv("HBNB_MYSQL_USER")
        pwd = os.getenv("HBNB_MYSQL_PWD")
        host = os.getenv("HBNB_MYSQL_HOST")
        db = os.getenv("HBNB_MYSQL_DB")
        link = f"""mysql+mysqldb://{user}:{pwd}@{host}/{db}"""

        self.__engine = create_engine(link, pool_pre_ping=True)

        if os.getenv('HBNB_ENV') == 'test':
            Base.metadata.drop_all(self.__engine)

    def all(self, cls=None):
        """returns all objects depending of the class name (argument cls)
        or all types of objects if cls is None"""
        dictionary = {}

        if cls is None:
            classes_to_query = [User, State, City, Amenity, Place, Review]
        else:
            if issubclass(cls, Base):
                classes_to_query = [cls]
            else:
                classes_to_query = []

        # now we found the classes to query and we will query them all
        for clss in classes_to_query:
            objts = self.__session.query(clss).all()
            # let's say we have one instance of class State
            # 'new_state = State(id=12, name="California")'
            # objets will be equal to objts = [new_state]
            # a list of all instances of class State
            for obj in objts:
                # Remove the _sa_instance_state attribute
                if hasattr(obj, '_sa_instance_state'):
                    delattr(obj, '_sa_instance_state')

                key = f"[{clss.__name__}].({obj.id})"
                dictionary[key] = obj

        return dictionary

    def new(self, obj):
        """Adds the object to the current database session"""
        self.__session.add(obj)

    def save(self):
        """Commits all changes of the current database session"""
        self.__session.commit()

    def delete(self, obj=None):
        """Deletes from the current database session object if not None"""
        if obj:
            self.__session.delete(obj)

    def reload(self):
        """Creates all tables in the database and the current
        database session
        """
        Base.metadata.create_all(self.__engine)
        Session = scoped_session(sessionmaker(bind=self.__engine,
                                              expire_on_commit=False))
        self.__session = Session()

    def close(self):
        """call close() method on the private session attribute"""
        self.__session.close()
