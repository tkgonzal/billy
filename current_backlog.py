'''
current_backlog.py
-Defines a Current_Backlog class which is a type of Media_Sublist, a container of Entry objects, designed for a backlog
 in which each Entry object represents a piece of media the user has yet to finish consuming

Traven 'tkgonzal' Gonzales
'''


import entry
import datetime
import media_sublist


class Current_Backlog(media_sublist.Media_Sublist):
    '''Defines a container of Entry objects representing things in the user's backlog'''
    _ITEMS_LIMIT = 50


    # INITIALIZATION
    def __init__(self, items: [entry.Entry] = []):
        '''Initializes a current backlog as a container of Entry objects with a set default key for sorting. By default
        initializes as empty and may accept a list of items. If the items argument exceed a certain limit, it will be
        truncated'''
        i_arg = items if len(items) < Current_Backlog._ITEMS_LIMIT else items[:Current_Backlog._ITEMS_LIMIT]
        media_sublist.Media_Sublist.__init__(self, i_arg)


    # EDITING METHODS
    def insert_item(self, item: entry.Entry):
        '''Inserts an item into the backlog based on the current desired ordering. Raises an MSOverflow exception if
        backlog is already at capacity'''
        if (len(self._items) < Current_Backlog._ITEMS_LIMIT):
            media_sublist.Media_Sublist.insert_item(self, item)
        else:
            raise media_sublist.MSOverflowException


    # KEY METHODS FOR SORTING
    @staticmethod
    def _default_key(item: entry.Entry) -> (int, datetime.date, str):
        '''By default, sorts backlog by an Entry's priority, its datetime added to the backlog, and its name'''
        return (-item.get_priority(), item.get_datetime_added(), item.get_name())

