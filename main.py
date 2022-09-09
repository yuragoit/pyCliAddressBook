import pickle
import os
from datetime import datetime, time
from tools import autocompletion as ui
# import aiopath

CLI_UI = '''
CMD HELPER: 1. Add (new contact) 2. View all 3. Search (contact) 4. Update (contact) 5. Delete (contact) 6. Reset all 
7. File sort 8. Exit
'''

# some change test


class Person():

    def __init__(self, name: str = None, address: str = None, phone: str = None, email: str = None, birthday: datetime.date = None):
        # planned refactoring to private methods (getter + setter)
        if name:
            self.name = name
        if address:
            self.address = address
        if phone:
            self.phone = phone
        if email:
            self.email = email
        if birthday:
            self.birthday = birthday

    # @property
    # def name(self):
    #     return self.__name

    # @name.setter
    # def name(self, value):
    #     if isinstance(value, str) and value.isalpha():
    #         self.__value = value
    #     else:
    #         print("Please enter a valid Name")
    #     return self.__value

    def __str__(self):
        return "{} {:^15} {:>15} {:>15} {:>15}".format(self.name, self.address, self.phone, self.email, self.birthday)


class Application():

    def __init__(self, database):
        self.database = database
        self.persons = {}
        if not os.path.exists(self.database):
            file_pointer = open(self.database, 'wb')
            pickle.dump({}, file_pointer)
            file_pointer.close()
        else:
            with open(self.database, 'rb') as person_list:
                self.persons = pickle.load(person_list)

    def add(self):
        name, address, phone, email, birthday = self.get_details()
        if name not in self.persons:
            self.persons[name] = Person(name, address, phone, email, birthday)
        else:
            print("Contact already present")

    def view_all(self):
        if self.persons:
            print("{} {:>15} {:>15} {:>15} {:>15}".format(
                'NAME', 'ADDRESS', 'PHONE', 'EMAIL', 'BIRTHDAY'))
            for person in self.persons.values():
                print(person)
        else:
            print("No match contacts in database")

    def search(self):
        name = input("Enter the name: ")
        if name in self.persons:
            print(self.persons[name])
        else:
            print("Contact not found")

    def get_details(self):
        name = input("Name: ")
        address = input("Address: ")
        phone = input("Phone: ")
        email = input("Email: ")
        birthday = input("Birthday: ")
        return name, address, phone, email, birthday

    def update(self):
        _name = input("Enter the name: ")
        if _name in self.persons:
            print("Found. Enter new details")
            name, address, phone, email, birthday = self.get_details()
            self.persons[_name].__init__(name, address, phone, email, birthday)
            print("Address book successfully updated")
        else:
            print("Contact not found")

    def delete(self):
        name = input("Enter the name to delete: ")
        if name in self.persons:
            del self.persons[name]
            print("Deleted the contact")
        else:
            print("Contact not found in the app")

    def reset(self):
        self.persons = {}

    def __del__(self):
        with open(self.database, 'wb') as db:
            pickle.dump(self.persons, db)

    def __str__(self):
        return CLI_UI


def CLI():
    app = Application('contacts.data')
    choice = ''
    while choice != 'exit':
        print(app)
        choice = ui.autocomplete()
        match choice:
            case 'add':
                app.add()
            case 'view_all':
                app.view_all()
            case 'search':
                app.search()
            case 'update':
                app.update()
            case 'delete':
                app.delete()
            case 'reset':
                app.reset()
            # scheduled developing process - integrate module from HW6, HW7
            case 'file_sort':
                pass
            case 'exit':
                print("Exiting...")
            case _:
                print("Invalid choice.")


if __name__ == '__main__':
    CLI()
