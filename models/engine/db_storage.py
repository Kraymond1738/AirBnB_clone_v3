#!/usr/bin/python3
"""
This module contains the DBStorage class
which interacts with the MySQL database.
"""

import os
import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from models.base_model import BaseModel, Base
from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User

classes = {
    "Amenity": Amenity,
    "City": City,
    "Place": Place,
    "Review": Review,
    "State": State,
    "User": User
}


class DBStorage:
    """
    This class interacts with the MySQL database.
    """

    __engine = None
    __session = None

    def __init__(self):
        """
        Instantiate a DBStorage object.
        """

        self.__engine = create_engine('mysql+mysqldb://{}:{}@{}/{}'.
                                      format(os.getenv('HBNB_MYSQL_USER'),
                                             os.getenv('HBNB_MYSQL_PWD'),
                                             os.getenv('HBNB_MYSQL_HOST'),
                                             os.getenv('HBNB_MYSQL_DB')))
        if os.getenv('HBNB_ENV') == "test":
            Base.metadata.drop_all(self.__engine)

    def all(self, cls=None):
        """
        Query on the current database session.
        """
        new_dict = {}
        if cls:
            if type(cls) == str:
                cls = classes.get(cls, None)
            objs = self.__session.query(cls).all()
        else:
            for cls in classes.values():
                objs = self.__session.query(cls).all()
        for obj in objs:
            key = "{}.{}".format(type(obj).__name__, obj.id)
            new_dict[key] = obj
        return new_dict

    def new(self, obj):
        """
        Add the object to the current database session.
        """
        self.__session.add(obj)

    def save(self):
        """
        Commit all changes of the current database session.
        """
        self.__session.commit()

    def delete(self, obj=None):
        """
        Delete from the current database session obj if not None.
        """
        if obj:
            self.__session.delete(obj)

    def reload(self):
        """
        Reloads data from the database.
        """
        Base.metadata.create_all(self.__engine)
        sess_factory = sessionmaker(bind=self.__engine,
                                    expire_on_commit=False)
        Session = scoped_session(sess_factory)
        self.__session = Session()

    def get(self, cls, id):
        """
        Retrieve one object.
        """
        if cls and id:
            objs = self.all(cls)
            for obj in objs.values():
                if obj.id == id:
                    return obj
        return None

    def count(self, cls=None):
        """
        Count the number of objects in storage.
        """
        if cls:
            objs = self.all(cls)
            return len(objs)
        else:
            count = 0
            for cls in classes.values():
                objs = self.all(cls)
                count += len(objs)
            return count

    def close(self):
        """
        Call remove() method on the private session attribute.
        """
        self.__session.remove()
