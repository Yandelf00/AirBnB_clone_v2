#!/usr/bin/python3
"""Contains the entry point of the command interpreter.
"""
import cmd
import re
from models import storage
from models.base_model import BaseModel
from models.user import User
from models.place import Place
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.review import Review


class HBNBCommand(cmd.Cmd):
    """class for command processor.

    Args:
        cmd (_type_): _description_
    """

    prompt = '(hbnb) '
    classes = {
               'BaseModel': BaseModel, 'User': User, 'Place': Place,
               'State': State, 'City': City, 'Amenity': Amenity,
               'Review': Review
              }
    def do_quit(self, line):
        """Quit command to exit the program
        """
        return True

    def do_EOF(self, line):
        """EOF command to exit the program at end of file (Ctrl-D)
        """
        print()
        return True

    def emptyline(self):
        """Empty line shouldn't execute anything
        """
        pass

    def do_create(self, line):
        """developed a new instance of BaseModel, saves it
        Exceptions:
            SyntaxError: when there is no args given
            NameError: when there is no object taht has the name
        """

        try:
            if not line:
                raise SyntaxError()
            my_list = line.split(" ")
            obj= HBNBCommand.classes[my_list[0]]()
            for element in my_list[1:]:
                key, val = element.split('=')
                val = val.replace('_', ' ')
                if hasattr(obj, key):
                    setattr(obj, key, eval(val))
            obj.save()
            print("{}".format(obj.id))
        except SyntaxError:
            print("** class name missing **")
        except NameError:
            print("** class doesn't exist **")

    def do_show(self, arg):
        """Prints the string representation of an instance.
        """
        if arg == "" or arg is None:
            print("** class name missing **")
        else:
            args = arg.split(' ')
            if args[0] not in storage.classes():
                print("** class doesn't exist **")
            elif len(args) < 2:
                print("** instance id missing **")
            else:
                key = "{}.{}".format(args[0], args[1])
                if key not in storage.all():
                    print("** no instance found **")
                else:
                    print(storage.all()[key])

    def do_destroy(self, arg):
        """Deletes an instance based on the class name and id.
        """
        if arg == "" or arg is None:
            print("** class name missing **")
        else:
            args = arg.split(' ')
            if args[0] not in storage.classes():
                print("** class doesn't exist **")
            elif len(args) < 2:
                print("** instance id missing **")
            else:
                key = "{}.{}".format(args[0], args[1])
                if key not in storage.all():
                    print("** no instance found **")
                else:
                    del storage.all()[key]
                    storage.save()

    def do_all(self, arg):
        """Prints all string representation of all
        instances based or not on the class name"""
        args = arg.split()
        if not args:
            all_instances = list(storage.all().values())
        else:
            class_name = args[0]
            if class_name not in self.classes:
                print("** class doesn't exist **")
                return
            all_instances = [value for key, value in storage.all().items()
                             if key.startswith(class_name)]
        print([str(all_instance) for all_instance in all_instances])

    def do_update(self, arg):
        """Updates an instance with a new attribute value"""
        args = arg.split()
        obj_dict = storage.all()
        if not args:
            print("** class name missing **")
            return
        if args[0] not in storage.classes():
            print("** class doesn't exist **")
            return
        if len(args) == 1:
            print("** instance id missing **")
            return
        key = "{}.{}".format(args[0], args[1])
        if key not in obj_dict:
            print("** no instance found **")
            return
        if len(args) == 2:
            print("** attribute name missing **")
            return
        if len(args) == 3:
            print("** value missing **")
            return
        attr_name = args[2]
        attr_value = args[3]
        instance = obj_dict[key]
        # Check if the attribute name is not one of the reserved attributes
        if attr_name in ["id", "created_at", "updated_at"]:
            print("** cannot update reserved attribute **")
            return
        # Update the attribute with proper casting
        setattr(instance, attr_name, attr_value)
        instance.save()

    def do_count(self, arg):
        """Counts the instances of a class."""
        args = arg.split(' ')
        count = 0
        if not args[0]:
            print("** class name missing **")
        elif args[0] not in storage.classes():
            print("** class doesn't exist **")
        else:
            for obj in storage.all().values():
                if args[0] == obj.__class__.__name__:
                    count += 1
            print(count)

    def default(self, arg):
        """Default behavior for cmd module when input is invalid"""
        args_dict = {
            "all": self.do_all,
            "count": self.do_count,
            "show": self.do_show,
            "destroy": self.do_destroy,
            "update": self.do_update
        }
        match = re.search(r"\.", arg)
        if match is not None:
            args = [arg[:match.span()[0]], arg[match.span()[1]:]]
            match = re.search(r"\((.*?)\)", args[1])
            if match is not None:
                command = [args[1][:match.span()[0]], match.group()[1:-1]]
                if command[0] in args_dict.keys():
                    call = "{} {}".format(args[0], command[1])
                    return args_dict[command[0]](call)
        print("*** Unknown syntax: {}".format(arg))
        return False


if __name__ == '__main__':
    HBNBCommand().cmdloop()
