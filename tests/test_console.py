#!/usr/bin/python3
"""Unittest module for the console"""

import unittest
from os import getenv, path, remove
import pycodestyle
from io import StringIO
from console import HBNBCommand
from models import storage
from models.engine.file_storage import FileStorage
from unittest.mock import patch
from models.user import User
from models.place import Place
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.review import Review


class TestConsole(unittest.TestCase):
    """Suite of test for the console"""

    def test_quit(self):
        """Test the quit command"""
        output = "Exits the program with formatting\n\n"
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("help quit")
            self.assertEqual(f.getvalue(), output)

    def test_EOF(self):
        """Test the EOF command"""
        output = "Exits the program without formatting\n\n"
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("help EOF")
            self.assertEqual(f.getvalue(), output)

    def test_emptyline(self):
        """Test an emptyline input"""
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("\n")
            self.assertEqual(f.getvalue(), "")

    def test_help(self):
        """Test all variations of the help command"""
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("help")
            self.assertIsInstance(f.getvalue(), str)
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("?")
            self.assertIsInstance(f.getvalue(), str)
        output = "Creates a class of any type\n[Usage]: create <className>"
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("help create")
            self.assertEqual(f.getvalue().strip(), output)
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("? create")
            self.assertEqual(f.getvalue().strip(), output)
        output = "Shows an individual instance of a class\n[Usage]: " \
            "show <className> <objectId>"
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("help show")
            self.assertEqual(f.getvalue().strip(), output)
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("? show")
            self.assertEqual(f.getvalue().strip(), output)
        output = "Destroys an individual instance of a class\n[Usage]: " \
            "destroy <className> <objectId>"
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("help destroy")
            self.assertEqual(f.getvalue().strip(), output)
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("? destroy")
            self.assertEqual(f.getvalue().strip(), output)
        output = "Shows all objects, or all of a class\n[Usage]: " \
            "all <className>"
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("help all")
            self.assertEqual(f.getvalue().strip(), output)
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("? all")
            self.assertEqual(f.getvalue().strip(), output)
        output = "Updates an object with new information\nUsage: " \
            "update <className> <id> <attName> <attVal>"
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("help update")
            self.assertEqual(f.getvalue().strip(), output)
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("? update")
            self.assertEqual(f.getvalue().strip(), output)

    def testPycodeStyle(self):
        """Pycodestyle test for console.py"""
        style = pycodestyle.StyleGuide(quiet=True)
        p = style.check_files(['console.py'])
        self.assertEqual(p.total_errors, 0, "fix pep8")

    def test_doc_console(self):
        self.assertIsNotNone(HBNBCommand.__doc__)
        self.assertIsNotNone(HBNBCommand.do_all.__doc__)
        self.assertIsNotNone(HBNBCommand.do_create.__doc__)
        self.assertIsNotNone(HBNBCommand.do_destroy.__doc__)
        self.assertIsNotNone(HBNBCommand.do_quit.__doc__)
        self.assertIsNotNone(HBNBCommand.do_EOF.__doc__)
        self.assertIsNotNone(HBNBCommand.do_update.__doc__)
        self.assertIsNotNone(HBNBCommand.emptyline.__doc__)


class TestCommand(unittest.TestCase):
    """Class that tests the console"""

    def setUp(self):
        """Function empties file.json"""
        FileStorage._FileStorage__objects = {}
        FileStorage().save()

    @unittest.skipIf(getenv('HBNB_TYPE_STORAGE') == 'db', "Not FileStorage")
    def test_create_fs(self):
        """test the create command"""
        storage = FileStorage()
        storage.reload()
        opt = r'[0-9a-f]{8}-[0-9a-f]{4}-4[0-9a-f]{3}-[0-9a-f]{4}-[0-9a-f]{12}'
        with self.assertRaises(TypeError):
            with patch('sys.stdout', new=StringIO()) as f:
                HBNBCommand().onecmd("create BaseModel updated_at=0.0"
                                     " created_at=0.0")
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd('create User email="cluck@wanadoo.fr"'
                                 ' password="jesustakethewheel"')
        result = f.getvalue().strip()
        self.assertRegex(result, opt)
        email = storage.all()[f'User.{result}'].email
        self.assertEqual(email, "cluck@wanadoo.fr")
        password = storage.all()[f'User.{result}'].password
        self.assertEqual(password, "jesustakethewheel")
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd('create State johnny="bravo"'
                                 ' number="7" pi="3.14"')
        result = f.getvalue().strip()
        self.assertRegex(result, opt)
        johnny = storage.all()[f'State.{result}'].johnny
        self.assertEqual(johnny, "bravo")
        number = storage.all()[f'State.{result}'].number
        self.assertEqual(number, '7')
        pi = storage.all()[f'State.{result}'].pi
        self.assertEqual(pi, '3.14')
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd('create City johnny="bravo" number="7"'
                                 ' pi="3.14"')
        result = f.getvalue().strip()
        self.assertRegex(result, opt)
        johnny = storage.all()[f'City.{result}'].johnny
        self.assertEqual(johnny, "bravo")
        number = storage.all()[f'City.{result}'].number
        self.assertEqual(number, '7')
        pi = storage.all()[f'City.{result}'].pi
        self.assertEqual(pi, '3.14')
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd('create Amenity johnny="bravo"'
                                 ' number="7" pi="3.14"')
        result = f.getvalue().strip()
        self.assertRegex(result, opt)
        johnny = storage.all()[f'Amenity.{result}'].johnny
        self.assertEqual(johnny, "bravo")
        number = storage.all()[f'Amenity.{result}'].number
        self.assertEqual(number, '7')
        pi = storage.all()[f'Amenity.{result}'].pi
        self.assertEqual(pi, '3.14')
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd('create Place johnny="bravo"'
                                 ' number="7" pi="3.14"')
        result = f.getvalue().strip()
        self.assertRegex(result, opt)
        johnny = storage.all()[f'Place.{result}'].johnny
        self.assertEqual(johnny, "bravo")
        number = storage.all()[f'Place.{result}'].number
        self.assertEqual(number, '7')
        pi = storage.all()[f'Place.{result}'].pi
        self.assertEqual(pi, '3.14')
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd('create Review johnny="bravo"'
                                 ' number="7" pi="3.14"')
        result = f.getvalue().strip()
        self.assertRegex(result, opt)
        johnny = storage.all()[f'Review.{result}'].johnny
        self.assertEqual(johnny, "bravo")
        number = storage.all()[f'Review.{result}'].number
        self.assertEqual(number, '7')
        pi = storage.all()[f'Review.{result}'].pi
        self.assertEqual(pi, '3.14')
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd('create')
        opt = '** class name missing **\n'
        self.assertEqual(f.getvalue(), opt)
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd('create NotClass')
        opt = '** class doesn\'t exist **\n'
        self.assertEqual(f.getvalue(), opt)


if __name__ == '__main__':
    unittest.main()
