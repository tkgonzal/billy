'''
billy.py
-Defines the Billy class, which is meant to create, load, and save Shelf objects by writing a Shelf object's data to a
 shelf file.
-The Billy class gets its name from a common media shelf used by collectors, the Billy.
-Shelf files contain data in the following manner:
    -The first line contains N many types of media a shelf file contains
    -What follows is N groups of three lines:
        -The first of these lines is the name of the the type of Media_List a Shelf housed
        -The second line contains the contents of that Media_List's Current_Backlog
        -The third line contains the contents of that Media_List;s Completed_List
    -The Entry information of each Media_Sublist's entry items is separated by the special set of characters "=+/"
    -Each Entry string of information has its parameters separated by the special set of characters "/*/"

Traven "tkgonzal" Gonzales 2019
'''


import shelf
import media_sublist
from pathlib import Path


class Billy:
    '''The Billy class defines an object meant to house a Shelf object, from which users can create the Shelf object
    and edits its contents. The Billy Class is also in charge of saving its Shelf object's information by writing the
    information to a shelf file, from which it can then load a Shelf object.'''


    # INITIALIZATION
    def __init__(self):
        '''Initializes a Billy object to be essentially a blank Shelf object editor, starting off with an empty Shelf
        object which users can edit as they please'''
        self._shelf = shelf.Shelf("untitled")


    # SHELF MANAGEMENT
    def make_new(self, name: str = "untitled"):
        '''Makes a new Shelf object for editing by the user'''
        self._shelf = shelf.Shelf(name)

    def save(self):
        '''"Saves" a Shelf object by writing its contents to a shelf file in a SAV folder. If the SAV folder does not
        exist yet, it is created.'''
        if not Path("SAV").exists():
            Path("SAV").mkdir(parents=True)
        shelf_sav = Path("SAV") / f"{self._shelf.get_name()}.shelf"
        media = self._shelf.get_media()

        try:
            sav = shelf_sav.open("w")
            sav.truncate(0)
            sav.write(f"{self._shelf.get_media_len()}\n")
            for i in range(self._shelf.get_media_len()):
                sav.write(f"{media[i].get_type()}\n")
                sav.write(f"{media[i].backlog.convert_items_to_str()}\n")
                sav.write(f"{media[i].completed.convert_items_to_str()}\n")
        finally:
            sav.close()

    def load(self, name: str):
        '''"Loads" a Shelf object by recreating the contents which has info stored in a shelf file'''
        shelf_sav = Path("SAV") / f"{name}.shelf"

        if not shelf_sav.exists():
            raise FileNotFoundError

        try:
            sav = shelf_sav.open("r")
            sav_info = sav.readlines()
        finally:
            sav.close()

        media_len = int(sav_info[0])
        sav_i = 1
        shelf_contents = {}

        for i in range(media_len):
            media_type = sav_info[sav_i][:-1]
            sav_i += 1
            backlog = media_sublist.Media_Sublist.make_items_from_str(sav_info[sav_i])
            sav_i += 1
            completed = media_sublist.Media_Sublist.make_items_from_str(sav_info[sav_i])
            shelf_contents[media_type] = (backlog, completed)
            sav_i += 1

        loaded_shelf = shelf.Shelf(name, shelf_contents)
        self._shelf = loaded_shelf


    # GETTERS
    def get_shelf(self) -> shelf.Shelf:
        '''Returns the Shelf object Billy is currently working on'''
        return self._shelf

