'''
entry.py
-Defines items to be added to a backlog list. An Entry object represents any sort of media that a user wishes/wished to
 consume i.e. books, movies, shows, etc.

Traven 'tkwtph' Gonzales 2019
'''


import datetime


class Entry:
    '''An Entry object is a piece of media a person wishes to consume in the future'''
    NOTES_LEN_LIMIT = 500


    # METHODS FOR ENTRY INITIALIZATION/EDITING
    def __init__(self, name: str, author: str, genre: str, price: float, release_year: int, priority: int, notes: str,
                 date_added: str = None, date_comp: str = None):
        '''Defines an Entry object's main attributes'''
        self._name = name
        self._author = author
        self._genre = genre
        self._price = price
        self._release_year = release_year
        self._priority = priority
        self._notes = self._truncate_notes(notes)
        self._datetime_added = self._str_to_datetime(date_added) if date_added != None else datetime.datetime.now()
        self._datetime_completed = self._str_to_datetime(date_comp) if date_comp != None else None

    @staticmethod
    def _truncate_notes(notes: str) -> str:
        '''Returns a truncated set of notes if they exceed a maximum length, otherwise returns the given notes'''
        result = notes
        if len(notes) > Entry.NOTES_LEN_LIMIT:
            result = notes[:Entry.NOTES_LEN_LIMIT]
        return result

    @staticmethod
    def _str_to_datetime(date_str: str) -> datetime.datetime:
        '''Returns a datetime converted from a datetime string'''
        return datetime.datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S.%f")


    # GENERAL OVERLOADED METHODS
    def __repr__(self) -> str:
        '''Returns a representation of an Entry object, mostly for debugging purposes'''
        result = f'Entry(name={self._name}, author={self._author} genre={self._genre}, price={self._price}, ' \
            f'release_year={self._release_year}, date_added={self._datetime_added}, priority={self._priority}, ' \
            f'notes={self._notes}'
        if self._datetime_completed is None:
            return result + ")"
        else:
            return result + f", date_completed={self._datetime_completed})"

    def __eq__(self, right) -> bool:
        '''Returns whether or not two entries are equal, so whether all of their member variables match in values'''
        return self._name == right._name and self._author == right._author and self._genre == right._genre and \
                self._price == right._price and self._release_year == right._release_year


    # GETTERS
    def get_name(self) -> str:
        '''Returns an Entry instant's name'''
        return self._name

    def get_author(self) -> str:
        '''Returns an Entry instant's author'''
        return self._author

    def get_genre(self) -> str:
        '''Returns an Entry instant's genre'''
        return self._genre

    def get_price(self) -> float:
        '''Returns an Entry instant's price'''
        return self._price

    def get_release_year(self) -> int:
        '''Returns an Entry instant's release year'''
        return self._release_year

    def get_datetime_added(self) -> datetime.datetime:
        '''Returns when an Entry was created'''
        return self._datetime_added

    def get_priority(self) -> int:
        '''Returns priority value of Entry'''
        return self._priority

    def get_notes(self) -> str:
        '''Returns an Entry instant's associated notes'''
        return self._notes

    def get_datetime_completed(self) -> datetime.datetime:
        '''Retrns when an entry was marked as completed'''
        return self._datetime_completed


    # SETTERS
    def set_name(self, new_info: str):
        '''Changes an Entry's instant name to a new given value'''
        self._name = new_info

    def set_author(self, new_info: str):
        '''Changes and Entry instant's author to a new given value'''
        self._author = new_info

    def set_genre(self, new_info: str):
        '''Changes an Entry instant's genre to a new given value'''
        self._genre = new_info

    def set_price(self, new_info: float):
        '''Changes an Entry instant's price to a new given value'''
        self._price = new_info

    def set_release_year(self, new_info: float):
        '''Changes an Entry instant's release year to a new given value'''
        self._release_year = new_info

    def set_priority(self, new_info: int):
        '''Changes an Entry instant's priority to a new given value'''
        self._priority = new_info

    def set_notes(self, new_info: str):
        '''Changes an Entry instant's notes to a new given value'''
        self._notes = self._truncate_notes(new_info)

    def set_completed(self):
        '''Sets an Entry object as completed'''
        self._datetime_completed = datetime.datetime.now()

    def set_incomplete(self):
        '''Sets an Entry object as incomplete'''
        self._datetime_completed = None


    # SHELF-SAV CONVERSION
    def convert_members_to_str(self) -> str:
        '''For use by the Billy program, this method converts the members of an Entry object into string such that the
        info may be written to a shelf file to be used later when recreating a Shelf object, and along with it the
        Entry objects it may store'''
        result = ""
        getters = [self.get_name, self.get_author, self.get_genre, self.get_price, self.get_release_year,
                   self.get_priority, self._encode_notes, self.get_datetime_added]
        if self._datetime_completed is not None:
            getters.append(self.get_datetime_completed)

        for getter in getters:
            result += f"{str(getter())}/*/"

        return result[:-3]

    @staticmethod
    def make_entry_from_str(entry_str: str) -> "Entry":
        '''Makes an Entry object from the Entry info recorded in a Shelf file'''
        entry_members = entry_str.split("/*/")

        name = entry_members[0]
        author = entry_members[1]
        genre = entry_members[2]
        price = float(entry_members[3])
        release = int(entry_members[4])
        priority = int(entry_members[5])
        notes = Entry._decode_notes(entry_members[6])
        date_add = entry_members[7]

        if len(entry_members) == 8:
            return Entry(name, author, genre, price, release, priority, notes, date_add)
        else:
            return Entry(name, author, genre, price, release, priority, notes, date_add, entry_members[8])

    def _encode_notes(self) -> str:
        '''Changes all instances of the newline character in an Entry object's notes section into the special set of
        characters ?=n such as not to interfere with th process of reading Shelf sav files in the Billy class'''
        return self._notes.replace("\n", "?=n")

    @staticmethod
    def _decode_notes(notes: str) -> str:
        '''Changes all instances of ?=n, created from presumable replacement of newline characters, to newline
        characters in the notes'''
        return notes.replace("?=n", "\n")

