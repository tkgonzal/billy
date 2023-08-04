'''
media_list.py
-Defines the Media_List class, a container for the Media_Sublist classes Current_Backlog and Completed_List that holds
 specifically a pair of these classes that only contains entries that fall under a certain type of media (i.e. movies,
 books, video games, etc. The Media_List class is meant to be a container of only the two aforementioned Media_Sublists
 and is used to facilitate data interactions between the two, namely for marking Entry objects in each sublist as
 complete/incomplete.

Traven 'tkgonzal' Gonzales
'''


import entry
import media_sublist
import current_backlog
import completed_list


class Media_List:
    '''A container of a pair of a Current_Backlog and Completed_List whose entries fall under a certain type of media,
    specified by Media_List'''


    # INITIALIZATION
    def __init__(self, media_type: str, backlog: [entry.Entry] = [], completed: [entry.Entry] = []):
        '''Initializes the Media_List by naming the type of media its sublists contains along with creating its
        sublists, which are a Current_Backlog and a Completed_List. By default, these sublists are initalized as empty
        but can be initialized when the constructor for the Media_List is passed list(s) of Entry objects'''
        self._type = media_type
        self.backlog = current_backlog.Current_Backlog(backlog)
        self.completed = completed_list.Completed_List(completed)


    # SUBLIST EDITING
    def mark_complete(self, idx: int):
        '''Marks an entry in the Media_List's backlog as completed and moves it to the Media_List's completed list'''
        item = self.backlog.remove_item(idx)
        item.set_completed()
        self.completed.insert_item(item)

    def mark_incomplete(self, idx: int):
        '''Marks an entry in the Media_List's completed list as incomplete moving it to the Media_List's incomplete. If
        inserting the removed item into the backlog would raise an error, the Entry removed is remarked as complete,
        inserted back into the completed list and reraises the MSOverflowException'''
        try:
            item = self.completed.remove_item(idx)
            item.set_incomplete()
            self.backlog.insert_item(item)
        except media_sublist.MSOverflowException:
            item.set_completed()
            self.completed.insert_item(item)
            raise media_sublist.MSOverflowException


    # GETTERS
    def get_type(self) -> str:
        '''Returns the type of media the Media_List stores'''
        return self._type

    def get_backlog(self) -> [entry.Entry]:
        '''Gets the items in the Media_List's current backlog'''
        return self.backlog.get_items()

    def get_backlog_limit(self) -> int:
        '''Gets the capacity for a Media_List's current backlog'''
        return self.backlog.get_items_limit()

    def get_completed(self) -> [entry.Entry]:
        '''Gets the items in the Media_List's completed section'''
        return self.completed.get_items()

    def get_completed_limit(self) -> int:
        '''gets the capacity for a Media_List's completed section'''
        return self.completed.get_items_limit()


    # SETTERS
    def set_type(self, new_type: str):
        '''Changes the name of the type that the Media_List is meant to represent'''
        self._type = new_type

