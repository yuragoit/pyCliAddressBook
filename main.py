import pickle
import os
import re
from datetime import datetime
from turtle import st
from tools import autocompletion as ui, validator
from tools import sorting
from dateutil import parser
from rich.console import Console
from rich.table import Table
# import aiopath

CLI_UI = '''
CMD HELPER: 1. Add (new contact) 2. View all 3. Search (contact) 4. Update (contact) 5. Delete (contact) 6. Reset all 
7. File sort 8. Exit
'''

console = Console()


class Person():

    def __init__(self, name: str = None, address: str = None, phone: str = None, email: str = None, birthday: datetime = None):
        self.name = name
        self.address = address
        self.phone = phone
        self.email = email
        self.birthday = parser.parse(birthday)

    def __str__(self):
        table = Table(show_header=False,
                      header_style="bold blue", show_lines=True)
        table.add_row(
            f'[cyan]{self.name}[/cyan]', f'[cyan]{self.address}[/cyan]', f'[cyan]{self.phone}[/cyan]',
            f'[cyan]{self.email}[/cyan]', f'[cyan]{self.birthday.date()}[/cyan]'
        )
        console.print(table)
        return f"{self.name}, {self.address}, {self.phone}, {self.email}, {self.birthday}"


class Note():
    def __init__(self, value: str, keyWords: list) -> None:
        self.date = datetime.now().isoformat()
        self.value = value
        self.keyWords = keyWords

    def get_keywords(self):
        return ", ".join(self.keyWords)

    def print_in_table(self):
        table = Table(show_header=False,
                      header_style="bold blue", show_lines=True)
        table.add_row(
            f'[cyan]{datetime.fromisoformat(self.date).strftime("%m/%d/%Y, %H:%M:%S")}[/cyan]', f'[cyan]{self.value}[/cyan]')
        console.print(table)

    def __str__(self):
        return "{:<25} {}".format(datetime.fromisoformat(self.date).strftime("%m/%d/%Y, %H:%M:%S"), self.value)


class AddressBook():

    def __init__(self, database):
        self.database = database
        self.persons = {}
        self.notes = {}
        if not os.path.exists(self.database):
            file_pointer = open(self.database, 'wb')
            pickle.dump({}, file_pointer)
            file_pointer.close()
        else:
            with open(self.database, 'rb') as Application:
                dict_application = pickle.load(Application)
                self.persons = dict_application.get("persons", self.persons)
                self.notes = dict_application.get("notes", self.notes)

    def add(self):

        name, _address, _phone, _email, _birthday = self.get_details()
        address = _address or "NULL"
        phone = _phone or "NULL"
        email = _email or "NULL"
        birthday = _birthday or "1900-01-01"
        if name not in self.persons:
            self.persons[name] = Person(name, address, phone, email, birthday)
        else:
            print("Contact already present")

    def add_note(self):
        value, keyWords = self.get_note()
        note = Note(value, keyWords)
        self.notes[note.date] = note

    def view_all(self):
        if self.persons:
            # print("{} {:>15} {:>15} {:>15} {:>15}".format(
            #     'NAME', 'ADDRESS', 'PHONE', 'EMAIL', 'BIRTHDAY'))
            table = Table(show_header=True,
                          header_style="bold blue", show_lines=True)
            table.add_column("#", style="dim", width=3, justify="center")
            table.add_column("NAME", min_width=12, justify="center")
            table.add_column("ADDRESS", min_width=10, justify="center")
            table.add_column("PHONE", min_width=18, justify="center")
            table.add_column("EMAIL", min_width=18, justify="center")
            table.add_column("BIRTHDAY", min_width=15, justify="center")
            for idx, person in enumerate(self.persons.values(), start=1):
                _ = person.__dict__
                table.add_row(
                    str(idx), f'[cyan]{_["name"]}[/cyan]', f'[cyan]{_["address"]}[/cyan]', f'[cyan]{_["phone"]}[/cyan]',
                    f'[cyan]{_["email"]}[/cyan]', f'[cyan]{_["birthday"].date()}[/cyan]'
                )
            console.print(table)
        else:
            print("No match contacts in database")

    def view_all_notes(self):
        if self.notes:
            table = Table(show_header=True,
                          header_style="bold blue", show_lines=True)
            table.add_column("#", style="dim",
                             width=3, justify="center")
            table.add_column("DATE", min_width=12, justify="center")
            table.add_column("VALUE", min_width=50, justify="center")

            for idx, note in enumerate(self.notes.values(), start=1):
                table.add_row(
                    str(idx), f'[cyan]{datetime.fromisoformat(note.date).strftime("%m/%d/%Y, %H:%M:%S")}[/cyan]', f'[cyan]{note.value}[/cyan]')

            console.print(table)
        else:
            print("No match notes in database")

    def search(self):
        name = input("Enter the name: ")
        if name in self.persons:
            print(self.persons[name])
        else:
            print("Contact not found")

    def search_notes(self):
        keyword = input("what to look for?: ")
        note_list_keyword = []
        note_list = []
        for note in self.notes.values():
            keywords = note.get_keywords()
            if keyword in keywords:
                note_list_keyword.append(note)

            if not note in note_list_keyword and keyword in str(note):
                note_list.append(note)

        if note_list_keyword or note_list:
            if note_list_keyword:

                table = Table(show_header=True,
                              header_style="bold blue", show_lines=True)
                table.add_column("by key", style="dim",
                                 width=3, justify="center")
                table.add_column("DATE", min_width=12, justify="center")
                table.add_column("VALUE", min_width=50, justify="center")

                for idx, note in enumerate(note_list_keyword, start=1):
                    table.add_row(
                        str(idx), f'[cyan]{datetime.fromisoformat(note.date).strftime("%m/%d/%Y, %H:%M:%S")}[/cyan]', f'[cyan]{note.value}[/cyan]')

                console.print(table)

            if note_list:
                table = Table(show_header=True,
                              header_style="bold blue", show_lines=True)
                table.add_column("by text", style="dim",
                                 width=4, justify="center")
                table.add_column("DATE", min_width=12, justify="center")
                table.add_column("VALUE", min_width=50, justify="center")

                for idx, note in enumerate(note_list, start=1):
                    table.add_row(
                        str(idx), f'[cyan]{datetime.fromisoformat(note.date).strftime("%m/%d/%Y, %H:%M:%S")}[/cyan]', f'[cyan]{note.value}[/cyan]')

                console.print(table)
        else:
            print(f"no notes with key word {keyword}")

    def find(self):
        obj = input('What do you want to find? ')
        for contact in self.persons.values():
            if obj in f'{contact.name} {contact.address} {contact.phone} {contact.email} {contact.birthday.date()}':
                print(contact)

    def get_details(self):
        name = validator.name_validator()
        address = input("Address: ")
        phone = validator.phone_check()
        email = validator.email_check()
        birthday = input("Birthday [format yyyy-mm-dd]: ")
        return name, address, phone, email, birthday

    def get_note(self):
        userInput = input("Note (keywords as #words#): ")
        keywords = re.findall(r"\#.+\#", userInput)
        value = userInput.strip()
        return value, [keyword.replace("#", "").strip() for keyword in keywords]

    def update(self):
        dict_name = input("Enter the name: ")
        if dict_name in self.persons:
            print("Found. Enter new details and keep empty fields if no any changes")
            _name, _address, _phone, _email, _birthday = self.get_details()
            name = _name or self.persons[dict_name].__dict__["name"]
            address = _address or self.persons[dict_name].__dict__["address"]
            phone = _phone or self.persons[dict_name].__dict__["phone"]
            email = _email or self.persons[dict_name].__dict__["email"]
            birthday = _birthday or self.persons[dict_name].__dict__[
                "birthday"]
            self.persons[dict_name].__init__(
                name, address, phone, email, birthday)
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

    def reset_notes(self):
        self.notes = {}

    def get_birthdays(self):
        gap_days = int(input("Enter timedelta for birthday: "))
        current_date = datetime.now()  # current date
        result = {}

        for name in self.persons:
            bday = self.persons[name].__dict__["birthday"]
            try:
                mappedbday = bday.replace(year=current_date.year)
            except ValueError:
                # 29 February cannot be mapped to non-leap year. Choose 28-Feb instead
                mappedbday = bday.replace(year=current_date.year, day=28)

            if 0 <= (mappedbday - current_date).days < gap_days:
                try:
                    result[mappedbday.strftime('%A')].append(name)
                except KeyError:
                    result[mappedbday.strftime('%A')] = [name]
            elif current_date.weekday() == 0:
                if -2 <= (mappedbday - current_date).days < 0:
                    try:
                        result[current_date.strftime('%A')].append(name)
                    except KeyError:
                        result[current_date.strftime('%A')] = [name]

        for day, names in result.items():
            # print(self.persons[name])
            print(f"Start reminder on {day}: {', '.join(names)}")
        return result

    def __del__(self):
        with open(self.database, 'wb') as db:
            pickle.dump({"persons": self.persons, "notes": self.notes}, db)

    def __str__(self):
        return CLI_UI


def CLI():
    app = AddressBook('contacts.data')
    choice = ''
    while choice != 'exit':
        print(app)
        choice = ui.autocomplete()
        match choice:
            case 'add':
                app.add()
            case 'add_notes':
                app.add_note()
            case 'view_all':
                app.view_all()
            case 'view_all_notes':
                app.view_all_notes()
            case 'search':
                app.search()
            case 'search_notes':
                app.search_notes()
            case 'find':
                app.find()
            case 'update':
                app.update()
            case 'delete':
                app.delete()
            case 'reset':
                app.reset()
            # scheduled developing process - integrate module from HW6, HW7
            case 'reset_notes':
                app.reset_notes()
            case 'file_sort':
                sorting.perform()
            case 'sort_birthday':
                app.get_birthdays()
            case 'exit':
                print("Exiting...")
            case _:
                print("Invalid choice.")


if __name__ == '__main__':
    CLI()
