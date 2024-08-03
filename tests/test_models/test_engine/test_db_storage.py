#!/usr/bin/python3
"""
Contains the TestDBStorageDocs and TestDBStorage classes
"""

from datetime import datetime
import inspect
import models
from models import storage
from models.engine.db_storage import DBStorage, classes
from models.amenity import Amenity
from models.base_model import BaseModel
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User
import json
import pep8
import unittest


class TestDBStorageDocs(unittest.TestCase):
    """Tests to check the documentation and style of DBStorage class"""
    @classmethod
    def setUpClass(cls):
        """Set up for the doc tests"""
        cls.dbs_f = inspect.getmembers(DBStorage, inspect.isfunction)

    def test_pep8_conformance_db_storage(self):
        """Test that models/engine/db_storage.py conforms to PEP8."""
        pep8s = pep8.StyleGuide(quiet=True)
        result = pep8s.check_files(['models/engine/db_storage.py'])
        self.assertEqual(result.total_errors, 0,
                         "Found code style errors (and warnings).")

    def test_pep8_conformance_test_db_storage(self):
        """Test tests/test_models/test_db_storage.py conforms to PEP8."""
        pep8s = pep8.StyleGuide(quiet=True)
        result = pep8s.check_files(['tests/test_models/test_engine/\
test_db_storage.py'])
        self.assertEqual(result.total_errors, 0,
                         "Found code style errors (and warnings).")

    def test_db_storage_module_docstring(self):
        """Test for the db_storage.py module docstring"""
        self.assertIsNot(DBStorage.__doc__, None,
                         "db_storage.py needs a docstring")
        self.assertTrue(len(DBStorage.__doc__) >= 1,
                        "db_storage.py needs a docstring")

    def test_db_storage_class_docstring(self):
        """Test for the DBStorage class docstring"""
        self.assertIsNot(DBStorage.__doc__, None,
                         "DBStorage class needs a docstring")
        self.assertTrue(len(DBStorage.__doc__) >= 1,
                        "DBStorage class needs a docstring")

    def test_dbs_func_docstrings(self):
        """Test for the presence of docstrings in DBStorage methods"""
        for func in self.dbs_f:
            self.assertIsNot(func[1].__doc__, None,
                             "{:s} method needs a docstring".format(func[0]))
            self.assertTrue(len(func[1].__doc__) >= 1,
                            "{:s} method needs a docstring".format(func[0]))


class TestDBStorage(unittest.TestCase):
    """Test the FileStorage class"""
    @unittest.skipIf(models.storage_t != 'db', "not testing db storage")
    def setUp(self):
        """setUp method"""
        self.my_key = sorted(storage.all())
        self.first_key = list(self.my_key)[0]
        classname, self.id = self.first_key.split(".")
        self.classname = classes[classname]

        self.obj_state = storage.get(self.classname, self.id)

    @unittest.skipIf(models.storage_t != 'db', "not testing db storage")
    def tearDown(self):
        """Close db session"""
        storage.close()

    @unittest.skipIf(models.storage_t != 'db', "not testing db storage")
    def test_db_get_method(self):
        """Test get method for DB storage"""
        self.assertEqual(self.obj_state, storage.get(self.classname, self.id))

    @unittest.skipIf(models.storage_t != 'db', "not testing db storage")
    def test_db_get_method_attr(self):
        """Test get method return type for DB storage"""
        self.assertEqual(self.obj_state.id, self.id)

    @unittest.skipIf(models.storage_t != 'db', "not testing db storage")
    def test_db_count_method_cls_none(self):
        """Test count method where no class is passed"""
        objs_count = len(storage.all())
        count = storage.count()
        self.assertEqual(count, objs_count)

    @unittest.skipIf(models.storage_t != 'db', "not testing db storage")
    def test_db_count_method_cls(self):
        """Test count method, when a class is passed"""
        objs_count = len(storage.all(self.classname))
        count = storage.count(self.classname)
        self.assertEqual(count, objs_count)

    @unittest.skipIf(models.storage_t != 'db', "not testing db storage")
    def test_db_count_method_cls_none_type(self):
        """Test count method where no class is passed return type"""
        objs_count = storage.count()
        self.assertEqual(type(objs_count), int)

    @unittest.skipIf(models.storage_t != 'db', "not testing db storage")
    def test_db_count_method_cls_type(self):
        """Test count method where class is passed return type"""
        objs_count = storage.count(self.classname)
        self.assertEqual(type(objs_count), int)

    @unittest.skipIf(models.storage_t != 'db', "not testing db storage")
    def test_all_returns_dict(self):
        """Test that all returns a dictionaty"""
        self.assertIs(type(models.storage.all()), dict)

    @unittest.skipIf(models.storage_t != 'db', "not testing db storage")
    def test_all_no_class(self):
        """Test that all returns all rows when no class is passed"""

    @unittest.skipIf(models.storage_t != 'db', "not testing db storage")
    def test_new(self):
        """test that new adds an object to the database"""

    @unittest.skipIf(models.storage_t != 'db', "not testing db storage")
    def test_save(self):
        """Test that save properly saves objects to file.json"""
