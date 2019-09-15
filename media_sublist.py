'''
media_sublist.py
-Defines the Media_Sublist parent class, which the Current_Backlog and Completed_List classes inherit from. Generically
 defines a container of Entry objects. The class is abstract, as only instances of its subclasses will be needed for
 the backlog
-Also Defines the MSUndeflow and MSOverflow Exceptions (MS refering to Media_Sublist). Though their names are self
 explanatory, their docstrings go more in depth into when they are to be raised

Traven 'tkwtph' Gonzales 2019
'''


import datetime
import entry
from sys import maxsize


class Media_Sublist:
    '''Defines a container of Entry objects'''
    # The ITEMS_LIMIT constant denotes the capacity of a Media_Sublist's list of Entry objects. Since the Media_Sublist
    # class is abstract, it is set to maxsize.
    _ITEMS_LIMIT = maxsize


    # METHODS FOR SETTING UP Media_Sublist
    def __init__(self, items: [entry.Entry] = []):
        '''Initializes a Media_Sublist object to be a container of Entry objects with a key for sorting its list of
        Entry objects, may start out as either empty or be initialized with a pre-existing list of Entry objects'''
        # The key_dict stores all key methods used for sorting with associated key words describing how they order
        self._key_dict = {"default": self._default_key, "name": self._name_key, "author": self._author_key,
                          "genre": self._genre_key, "price": self._price_key, "release": self._release_year_key,
                          "date": self._date_added_key}
        # The edit_dict stores all setter methods for Entry objects, each with associated key words
        self._edit_dict = {"name": entry.Entry.set_name, "author": entry.Entry.set_author,
                           "genre": entry.Entry.set_genre, "price": entry.Entry.set_price,
                           "release": entry.Entry.set_release_year, "priority": entry.Entry.set_priority,
                           "notes": entry.Entry.set_notes}
        self._current_key = self._default_key
        self._items = sorted(items, key=self._current_key)


    # METHODS FOR ALTERING A Media_Sublist's Order
    def change_sort(self, order: str):
        '''Changes the pattern for sorting a Media_Sublist's items given the keyword for a key method'''
        self._sort_by_key(self._key_dict[order])

    def _sort_by_key(self, key_method: callable):
        '''Changes the current key and resorts a Media_Sublist's items to match'''
        self._current_key = key_method
        self._items.sort(key=self._current_key)


    # METHODS FOR EDITING A Media_Sublist AND ITS ENTRIES
    def insert_item(self, item: entry.Entry):
        '''Inserts item into list by binary insertion'''
        i = self._determine_index(item)
        self._items.insert(i, item)

    def remove_item(self, idx: int) -> entry.Entry:
        '''Removes and returns the item from the Media_Sublist's items, assuming provided index is valid. Will throw an
        UnderflowException when called on an empty Media_Sublist'''
        if len(self._items) > 0:
            return self._items.pop(idx)
        else:
            raise MSUnderflowException

    def edit_item(self, idx: int, edit_key: str or [str], new_info: str or float or int or [str] or [float] or [int]):
        '''Edits an entry and reorders it accordingly, assuming provided index and calls are always valid. May either
        take a key referring to a member to edit or a list of keys and info referring to a set of memebers to edit'''
        if type(edit_key) == str:
            self._edit_dict[edit_key](self._items[idx], new_info)
        else:
            for key, new in zip(edit_key, new_info):
                self._edit_dict[key](self._items[idx], new)
        item = self._items.pop(idx)
        Media_Sublist.insert_item(self, item)

    def _determine_index(self, item: entry.Entry) -> int:
        '''Determines the proper index of an Entry to be inserted into the sublist using binary search'''
        min_idx = 0
        max_idx = len(self._items) - 1

        while min_idx <= max_idx:
            mid = min_idx + (max_idx - min_idx) // 2
            if self._current_key(item) < self._current_key(self._items[mid]):
                max_idx = mid - 1
            elif self._current_key(item) > self._current_key(self._items[mid]):
                min_idx = mid + 1
            else:
                return mid
        return min_idx


    # GETTERS
    def get_items(self) -> [entry.Entry]:
        '''Returns the Media_Sublist's current items'''
        return self._items

    def get_items_limit(self) -> int:
        '''Returns the Media_Sublist's limit for the length of its items list'''
        return self._ITEMS_LIMIT


    # KEY METHODS FOR SORTING
    '''All key methods will sort by name alphabetically when their respectivve values are equal'''
    @staticmethod
    def _default_key(item: entry.Entry):
        '''Abstract method used as key for sorting a Media_Sublist's items'''
        pass

    @staticmethod
    def _name_key(item: entry.Entry) -> str:
        '''Returns the name of an Entry object for sorting'''
        return item.get_name().lower()

    @staticmethod
    def _author_key(item: entry.Entry) -> (str, str):
        '''Returns the author of the Entry object for sorting'''
        return (item.get_author().lower(), item.get_name().lower())

    @staticmethod
    def _genre_key(item: entry.Entry) -> (str, str):
        '''Returns the genre of the Entry object for sorting'''
        return (item.get_genre().lower(), item.get_name().lower())

    @staticmethod
    def _price_key(item: entry.Entry) -> (float, str):
        '''Returns the price of the Entry object for sorting'''
        return (item.get_price(), item.get_name().lower())

    @staticmethod
    def _release_year_key(item: entry.Entry) ->  (int, str):
        '''Returns the release year of the Entry object for sorting'''
        return (item.get_release_year(), item.get_name().lower())

    @staticmethod
    def _date_added_key(item: entry.Entry) -> (datetime.datetime, str):
        '''Returns the datetime of the Entry object being added to the list for sorting'''
        return (item.get_datetime_added(), item.get_name().lower())


    # SHELF-SAV CONVERSION
    def convert_items_to_str(self) -> str:
        '''Converts a Media_Sublist object's items to a str used for saving the information of a Shelf object from the
        Billy class'''
        result = ""

        for item in self._items:
            result += f"{item.convert_members_to_str()}=+/"

        return result[:-3]

    @staticmethod
    def make_items_from_str(items_str: str) -> "Media_Sublist":
        '''Converts a string representing the items of a Media_Sublist into items to be used as a Media_Sublist's
        argument'''
        result = []
        item_strings = items_str[:-1].split("=+/") if len(items_str) > 20 else []

        for item_str in item_strings:
            result.append(entry.Entry.make_entry_from_str(item_str))

        return result


class MSUnderflowException(Exception):
    '''An underflow exception for the Media_Sublist classes, meant to be raised whenever removal is performed on 'empty'
    Media_Sublists'''
    pass


class MSOverflowException(Exception):
    '''An overflow exception for the Media_Sublist classes, meant to be raised whenever removal is performed on 'full'
    Media_Sublists (i.e. their item counts have reached their respective limits)'''
    pass

