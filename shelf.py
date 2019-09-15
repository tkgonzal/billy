'''
shelf.py
-Defines the Shelf class, a container of Media_List objects and the main hub of the backlog manager
-Defines the ShelfUnderflowException and ShelfOverflowException classes to be called when atempting to add a Media_List
 to an at capacity shelf and trying to remove from an empty Shelf

Traven 'tkwtph' Gonzales 2019
'''


import entry
import media_list


class Shelf:
    '''Defines the Shelf class, a container of Media_List objects'''
    _MEDIA_LIMIT = 10


    # INITIALIZATION
    def __init__(self, name: str, prev_shelf: {str: ([entry.Entry], [entry.Entry])} = {}):
        '''Initializes a Shelf object. By default, a Shelf object starts out as an empty container but may be passed a
        dictionary of key-list of Entry tuple pairs to make a filled shelf'''
        self._name = name
        self._media = sorted(self._convert_dict_to_media_lists(prev_shelf), key=media_list.Media_List.get_type)
        if len(self._media) > Shelf._MEDIA_LIMIT:
            self._media = self._media[:Shelf._MEDIA_LIMIT]

    @staticmethod
    def _convert_dict_to_media_lists(prev_shelf: {str: ([entry.Entry], [entry.Entry])}) -> [media_list.Media_List]:
        '''Converts a dictionary of key-list of Entry tuple pairs to a list of Media_list objects'''
        result = []
        for media in prev_shelf:
            result.append(media_list.Media_List(media, prev_shelf[media][0], prev_shelf[media][1]))
        return result


    # EDITING METHODS
    def add_media(self, type: str):
        '''Will add a new empty Media_List to the list of media. If at capacity will raise a ShelfOverflowException'''
        if len(self._media) >= self._MEDIA_LIMIT:
            raise ShelfOverflowException
        else:
            self._media.insert(self._determine_index(type), media_list.Media_List(type))

    def remove_media(self, idx: int):
        '''Will remove a Media_List from the Shelf at the given index. Will raise a ShelfUnderflowException if empty'''
        if len(self._media) <= 0:
            raise ShelfUndeflowException
        else:
            self._media.pop(idx)

    def resort_media(self):
        '''Resorts the Media_List objects (Called when a Media_List object is renamed)'''
        self._media = sorted(self._media, key=media_list.Media_List.get_type)

    def _determine_index(self, type: str) -> int:
        '''Determines the proper index of a Media_List to be made based using binary search'''
        min_idx = 0
        max_idx = len(self._media) - 1

        while min_idx <= max_idx:
            mid_idx = min_idx + (max_idx - min_idx) // 2
            if type < self._media[mid_idx].get_type():
                max_idx = mid_idx - 1
            elif type > self._media[mid_idx].get_type():
                min_idx = mid_idx + 1
            else:
                return mid_idx
        return min_idx


    # GETTERS
    def get_name(self) -> str:
        '''Returns the name of the shelf'''
        return self._name

    def get_media(self) -> [media_list.Media_List]:
        '''Returns a Shelf object's list of media'''
        return self._media

    def get_media_len(self) -> int:
        '''Returns the amount of types of Media the Shelf object is currently housing'''
        return len(self._media)

    @staticmethod
    def get_media_limit() -> int:
        '''Returns the capcity of the Shelf object'''
        return Shelf._MEDIA_LIMIT


    # SETTERS
    def set_name(self, name: str):
        '''Changes the name of the current Shelf'''
        self._name = name


class ShelfOverflowException(Exception):
    '''An overflow exception meant to be called when attempting to add to an at capacity Shelf'''
    pass


class ShelfUndeflowException(Exception):
    '''An underflow exception meant to be called when attempting to remove from an empty Shelf'''
    pass

