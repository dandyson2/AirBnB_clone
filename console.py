#!/usr/bin/python3


"""Module for the entry point of the command interpreter (console)"""


import re
import cmd
import json
from models import storage
from models.user import User
from models.city import City
from models.state import State
from models.place import Place
from models.review import Review
from models.amenity import Amenity
from models.base_model import BaseModel
from models.engine.file_storage import FileStorage


class HBNBCommand(cmd.Cmd):
    """This is the Class for the command interpreter."""
    prompt = "(hbnb) "

    def default(self, record):
        """Catch commands if nothing else matches then."""
        self._precmd(record)

    def _precmd(self, record):
        """Intercepts commands to test for class.syntax()"""
        match = re.search(r"^(\w*)\.(\w+)(?:\(([^)]*)\))$", record)
        if not match:
            return (record)
        classname = match.group(1)
        method = match.group(2)
        args = match.group(3)
        match_uid_and_args = re.search('^"([^"]*)"(?:, (.*))?$', args)
        if match_uid_and_args:
            uid = match_uid_and_args.group(1)
            attr_or_dict = match_uid_and_args.group(2)
        else:
            uid = args
            attr_or_dict = False

        attr_and_value = ""
        if method == "update" and attr_or_dict:
            match_dict = re.search('^({.*})$', attr_or_dict)
            if match_dict:
                self.update_dict(classname, uid, match_dict.group(1))
                return ("")
            match_attr_and_value = re.search(
                '^(?:"([^"]*)")?(?:, (.*))?$', attr_or_dict)
            if match_attr_and_value:
                attr_and_value = (match_attr_and_value.group(
                    1) or "") + " " + (match_attr_and_value.group(2) or "")
        command = method + " " + classname + " " + uid + " " + attr_and_value
        self.onecmd(command)
        return (command)

    def update_dict(self, classname, uid, s_dict):
        """This is the helper method for update() with a dictionary."""
        s = s_dict.replace("'", '"')
        d = json.loads(s)
        if not classname:
            print("** class name missing **")
        elif classname not in storage.classes():
            print("** class doesn't exist **")
        elif uid is None:
            print("** instance id missing **")
        else:
            key = "{}.{}".format(classname, uid)
            if key not in storage.all():
                print("** no instance found **")
            else:
                attributes = storage.attributes()[classname]
                for attribute, value in d.items():
                    if attribute in attributes:
                        value = attributes[attribute](value)
                    setattr(storage.all()[key], attribute, value)
                storage.all()[key].save()

    def do_EOF(self, record):
        """To handles End Of File as to exit program."""
        print()
        return (True)

    def do_quit(self, record):
        """This exits the program."""
        return (True)

    def emptyline(self):
        """This doesn't do anything on ENTER."""
        pass

    def do_create(self, record):
        """Creates new instance of BaseModel, save it and print id."""
        if record == "" or record is None:
            print("** class name missing **")
        elif record not in storage.classes():
            print("** class doesn't exist **")
        else:
            storage.classes()[record]()
            storage.save()
            print(storage.id)

    def do_show(self, record):
        """Prints string representation of an instance base on:
        class name & id"""
        if record == "" or record is None:
            print("** class name missing **")
        else:
            element = record.split(" ")
            if element[0] not in storage.classes():
                print("** class doesn't exist **")
            elif len(element) < 2:
                print("** instance id missing **")
            else:
                key = "{}.{}".format(element[0], element[1])
                if key not in storage.all():
                    print("** no instance found **")
                else:
                    print(storage.all()[key])

    def do_destroy(self, record):
        """
        Deletes an instance based on the class name and id.
            then save it
        """
        if record == "" or record is None:
            print("** class name missing **")
        else:
            element = record.split(' ')
            if element[0] not in storage.classes():
                print("** class doesn't exist **")
            elif len(element) < 2:
                print("** instance id missing **")
            else:
                key = "{}.{}".format(element[0], element[1])
                if key not in storage.all():
                    print("** no instance found **")
                else:
                    del storage.all()[key]
                    storage.save()

    def do_all(self, record):
        """
        Prints all string representation of all instances.
        Base on:
        Class name or
        Not on class name.
        """
        if record != "":
            element = record.split(' ')
            if element[0] not in storage.classes():
                print("** class doesn't exist **")
            else:
                case = [str(obj) for key, obj in storage.all().items()
                        if type(obj).__name__ == element[0]]
                print(case)
        else:
            new_record = [str(obj) for key,
                          obj in storage.all().items()]
            print(new_record)

    def do_count(self, record):
        """Counts the instances of a class."""
        element = record.split(" ")
        if not element[0]:
            print("** class name missing **")
        elif element[0] not in storage.classes():
            print("** class doesn't exist **")
        else:
            matches = [
                k for k in storage.all() if k.startswith(
                    element[0] + '.')]
            print(len(matches))

    def do_update(self, record):
        """
        Updates an instance by adding or updating attribute.
        Base on:
        Class name,
        id &
        save changes to JSON File.
        """
        if record == "" or record is None:
            print("** class name missing **")
            return ()

        rex = r'^(\S+)(?:\s(\S+)(?:\s(\S+)(?:\s((?:"[^"]*")|(?:(\S)+)))?)?)?'
        match = re.search(rex, record)
        classname = match.group(1)
        uid = match.group(2)
        attribute = match.group(3)
        value = match.group(4)
        if not match:
            print("** class name missing **")
        elif classname not in storage.classes():
            print("** class doesn't exist **")
        elif uid is None:
            print("** instance id missing **")
        else:
            key = "{}.{}".format(classname, uid)
            if key not in storage.all():
                print("** no instance found **")
            elif not attribute:
                print("** attribute name missing **")
            elif not value:
                print("** value missing **")
            else:
                entry = None
                if not re.search('^".*"$', value):
                    if '.' in value:
                        entry = float
                    else:
                        entry = int
                else:
                    value = value.replace('"', '')
                attributes = storage.attributes()[classname]
                if attribute in attributes:
                    value = attributes[attribute](value)
                elif entry:
                    try:
                        value = entry(value)
                    except ValueError:
                        pass
                setattr(storage.all()[key], attribute, value)
                storage.all()[key].save()


if __name__ == '__main__':
    HBNBCommand().cmdloop()
