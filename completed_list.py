'''
completed_list.py
-Defines the Completed_List class which stores Entry objects marked as completed, representing pieces of media that were
 previously on the users' backlog. A Completed_List is a child of Media_Sublist that is meant to hold a small amount of
 Entries to show the user what they have most recently completed.

Traven 'tkwtph' Gonzales
'''


import datetime
import entry
import media_sublist


class Completed_List(media_sublist.Media_Sublist):
    '''A type of Media_Sublist meant to be a container of Entry objects marked as completed'''
    _ITEMS_LIMIT = 5


    # INITIALIZATION
    def __init__(self, items: [entry.Entry] = []):
        '''Initializes a Completed_List to be a Media_Sublist meant to hold a small amount of Entry objects the user has
        once had on thei backlog but has now finished consuming. May be initialized as either empty by default or with
        an list of Entry objects as an argument that will be truncated if needed'''
        i_arg = items if len(items) < Completed_List._ITEMS_LIMIT else items[:Completed_List._ITEMS_LIMIT]
        media_sublist.Media_Sublist.__init__(self, i_arg)


    # EDITING METHODS
    def insert_item(self, item: entry.Entry):
        '''To be called after an object is marked as completed, will insert a given Entry object into the
        Completed_List's item list. If the Completed_List is at capacity, the oldest Entry marked as completed will be
        removed and the new Entry will be added'''
        if len(self._items) >= Completed_List._ITEMS_LIMIT:
            if self._current_key != self._default_key:
                self.change_sort("default")
            self.remove_item(0)
        media_sublist.Media_Sublist.insert_item(self, item)


    # KEY METHODS FOR SORTING
    @staticmethod
    def _default_key(item: entry.Entry) -> (datetime.datetime, str):
        '''Returns an Entry instant's datetime marked as completed and name for sorting'''
        return (item.get_datetime_completed(), item.get_name())

