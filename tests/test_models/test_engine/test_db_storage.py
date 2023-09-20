#!/usr/bin/python3
"""Unittests for DBstorage"""
import unittest
from models.engine.db_storage import DBStorage
from models import storage
from os import getenv
from models.base_model import Base, BaseModel
from models.user import User
from models.place import Place
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.review import Review
from datetime import datetime
import MySQLdb


@unittest.skipIf(getenv('HBNB_TYPE_STORAGE') != 'db',
                 'db_storage test is not supported oustside db')
class Test_Dbstorage(unittest.TestCase):
    """tests for the new storage DBstorage"""

    def test_dbstorage_save_method(self):
        """test for save method of dbstorage"""
        conn = MySQLdb.connect(user=getenv('HBNB_MYSQL_USER'),
                               passwd=getenv('HBNB_MYSQL_PWD'),
                               host=getenv('HBNB_MYSQL_HOST'),
                               port=3306,
                               db=getenv('HBNB_MYSQL_DB'))
        new_state = State(name="Tetouan")
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM states")
        before_save = cursor.fetchall()
        cursor.close()
        conn.close()
        new_state.save()
        self.assertTrue(new_state in storage.all(State).values())
        conn = MySQLdb.connect(user=getenv('HBNB_MYSQL_USER'),
                               passwd=getenv('HBNB_MYSQL_PWD'),
                               host=getenv('HBNB_MYSQL_HOST'),
                               port=3306,
                               db=getenv('HBNB_MYSQL_DB'))
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM states")
        after_save = cursor.fetchall()
        self.assertEqual(before_save[0][0] + 1, after_save[0][0])
        cursor.close()
        conn.close()

    def test_dbstorage_new_method(self):
        """test for new method of dbstorage"""
        new_state = State(name="Tetouan")
        self.assertFalse(new_state in storage.all(State).values())
        storage.new(new_state)
        storage.save()
        self.assertTrue(new_state in storage.all(State).values())

    # def test_dbstorage_delete_method(self):
    #     """test for delete method of dbstorage"""
    #     state = State(name="Tetouan")
    #     self.assertFalse(state in storage.all(State).values())
    #     state.save()
    #     self.assertTrue(state in storage.all(State).values())
    #     state.delete()

    def test_dbstorage_reload_method(self):
        """test for reload method of dbstorage"""
        conn = MySQLdb.connect(user=getenv('HBNB_MYSQL_USER'),
                               passwd=getenv('HBNB_MYSQL_PWD'),
                               host=getenv('HBNB_MYSQL_HOST'),
                               port=3306,
                               db=getenv('HBNB_MYSQL_DB'))
        cursor = conn.cursor()
        n_state = State(id="random-id", name="Tanger",
                        created_at=str(datetime.now()),
                        updated_at=str(datetime.now()))
        n_state.save()
        conn.commit()
        storage.reload()
        self.assertIn('[State].(random-id)', storage.all().keys())
        cursor.close()
        conn.close()
