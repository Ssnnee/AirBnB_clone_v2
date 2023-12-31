#!/usr/bin/python3

"""This module defines a class to manage file storage for hbnb clone"""
from models.base_model import Base
from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User


class DBStorage:
    """ A class to manage storage of hbnb models in MySQL database"""
    __engine = None
    __session = None

    def __init__(self):
        """Instantiation of DBStorage class"""
        from sqlalchemy import create_engine
        from sqlalchemy.orm import sessionmaker
        from os import getenv

        user = getenv("HBNB_MYSQL_USER")
        pwd = getenv("HBNB_MYSQL_PWD")
        host = getenv("HBNB_MYSQL_HOST")
        db = getenv("HBNB_MYSQL_DB")

        self.__engine = create_engine('mysql+mysqldb://{}:{}@{}/{}'.
                                      format(user, pwd, host, db),
                                      pool_pre_ping=True)
        Base.metadata.create_all(self.__engine)
        Session = sessionmaker(bind=self.__engine)
        self.__session = Session()

    def all(self, cls=None):
        """Returns a dictionary of models currently in storage"""
        if cls is None:
            objs = self.__session.query(User).all()
            objs.extend(self.__session.query(State).all())
            objs.extend(self.__session.query(City).all())
            objs.extend(self.__session.query(Amenity).all())
            objs.extend(self.__session.query(Place).all())
            objs.extend(self.__session.query(Review).all())
        else:
            objs = self.__session.query(cls).all()
        return {
                "{}.{}".format(type(obj).__name__, obj.id): obj for obj in objs
        }

    def new(self, obj):
        """Adds new object to storage dictionary"""
        self.__session.add(obj)

    def save(self):
        """Saves storage dictionary to file"""
        self.__session.commit()

    def delete(self, obj=None):
        """Delete obj from __objects if it’s inside"""
        if obj is not None:
            self.__session.delete(obj)

    def reload(self):
        """Loads storage dictionary from file"""
        from sqlalchemy.orm import scoped_session
        from sqlalchemy.orm import sessionmaker

        Base.metadata.create_all(self.__engine)
        Session = scoped_session(sessionmaker(bind=self.__engine,
                                              expire_on_commit=False))
        self.__session = Session()

    def close(self):
        """Close session"""
        self.__session.close()
