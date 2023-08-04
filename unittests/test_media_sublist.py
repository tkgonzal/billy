'''
test_media_sublist.py
-Tests the Media_Sublist's method's functionality. This is done by way testing the Current_Backlog class, as the
 Media_Sublist is abstract since it has no true default key.

Traven 'tkgonzal' Gonzales 2019
'''


import unittest
import time
import entry
import media_sublist
import current_backlog


# FUNCTION FOR MAKING WAIT TIME
def wait_time(): # ZA WARUDO
    '''Creates a wait time of .125 seconds. Used in testing for differentiating datetimes'''
    start = time.time()
    while time.time() - start < .125:
        continue


class MediaSublistTest(unittest.TestCase):
    '''Unittest for Media_Sublist through testing of the Current_Backlog class'''


    # SET UP
    def setUp(self):
        '''Sets up variables used for unit testing'''
        # TEST ENTRIES
        self._item1 = entry.Entry("SATURATION", "BROCKHAMPTON", "Hip-Hop", 9.99, 2017, 5, "best boy band in the world")
        wait_time()
        self._item2 = entry.Entry("A Fever You Can't Sweat Out", "Panic! at the Disco", "Pop Punk", 9.99, 2005, 4,
                                  "I miss the old p!atd")
        wait_time()
        self._item3 = entry.Entry("In the Aeroplane Over the Sea", "Neutral Milk Hotel", "Indie Rock", 9.99, 1998, 4,
                                  "WHAT A BEAUTIFUL PLACE I HAVE FOUND IN THIS PLACE")
        wait_time()
        self._item4 = entry.Entry("My Beautiful Dark Twisted Fantasy", "Kanye West", "Hip-Hop", 13.99, 2010, 5, "")
        wait_time()
        self._item5 = entry.Entry("Whatever People Say I am That's What I'm Not", "Arctic Monkeys", "Indie Rock", 7.99,
                                  2006, 2, "the only good arctic monkeys album")
        self._items = [self._item1, self._item2, self._item3, self._item4, self._item5]

        # TEST BACKLOGS
        self._bklog1 = current_backlog.Current_Backlog()
        self._bklog2 = current_backlog.Current_Backlog(self._items[:5])


    # BACKLOG TESTS
    # INITIALIZATION
    def test_if_current_backlog_initializes_empty(self):
        '''Tests if a new current backlog is initialized as empty when it is not given an argument for its item
        parameter'''
        self.assertEqual(len(self._bklog1.get_items()), 0)

    def test_if_a_current_backlog_can_initialize_with_an_items_argument_and_properly_sort_its_new_items(self):
        '''Tests if a Current_Backlog can initialize with a list of items and be initialized with the items as
        properly sorted'''
        self.assertEqual(len(self._bklog2.get_items()), 5)
        self.assertListEqual(self._bklog2.get_items(), [self._item1, self._item4, self._item2, self._item3,
                                                        self._item5])

    def test_if_a_current_backlog_can_initialize_with_an_overly_long_list_of_entries_and_remain_under_its_limit(self):
        '''Tests if Current_Backlog initialization with an items argument of a length over its limit will be truncated
        upon creation of the Current_Backlog's items member'''
        test = []
        for _ in range(current_backlog.Current_Backlog._ITEMS_LIMIT + 20):
            test.append(entry.Entry("", "", "", 0.69, 1985, 1, ""))
        bklog = current_backlog.Current_Backlog(test)

        self.assertEqual(len(bklog.get_items()), current_backlog.Current_Backlog._ITEMS_LIMIT)

    # INSERTION
    def test_insertion_to_empty_backlog(self):
        '''Tests if inserting into an empty backlog works as intended'''
        self._bklog1.insert_item(self._item1)

        self.assertEqual(len(self._bklog1.get_items()), 1)
        self.assertEqual(self._bklog1.get_items()[0], self._item1)

    def test_multiple_insertions_to_backlog(self):
        '''Tests if multiple insertions to a backlog inserts the items in a proper order'''
        for i in range(5):
            self._bklog1.insert_item(self._items[i])

        self.assertEqual(len(self._bklog1.get_items()), 5)
        self.assertListEqual(self._bklog1.get_items(), [self._item1, self._item4, self._item2, self._item3,
                                                        self._item5])

    def test_that_backlog_raises_an_overflow_exception_after_inserting_more_than_its_limit(self):
        '''Tests if inserting into a backlog after it reaches a certain limit raises an exception'''
        for _ in range(current_backlog.Current_Backlog._ITEMS_LIMIT):
            self._bklog1.insert_item(entry.Entry("", "", "", 0.69, 1985, 1, ""))

        with self.assertRaises(media_sublist.MSOverflowException):
            self._bklog1.insert_item(entry.Entry("", "", "", 0.69, 1985, 1, ""))

        self.assertEqual(len(self._bklog1.get_items()), current_backlog.Current_Backlog._ITEMS_LIMIT)

    def test_that_inserting_into_an_empty_backlog_with_a_non_default_key_works_properly(self):
        '''Tests if inserting into the backlog with a non-default key works properly'''
        self._bklog1.change_sort("name")
        for i in range(5):
            self._bklog1.insert_item(self._items[i])

        self.assertListEqual(self._bklog1.get_items(), [self._item2, self._item3, self._item4, self._item1,
                                                        self._item5])

    def test_that_inserting_into_a_backlog_after_changing_its_current_key_works_properly(self):
        '''Tests that a backlog with entries that changes its current key inserts properly'''
        self._bklog1.insert_item(self._item4)
        self._bklog1.insert_item(self._item5)
        self._bklog1.change_sort("author")

        self._bklog1.insert_item(self._item3)
        self.assertEqual(self._bklog1.get_items()[2], self._item3)

        for i in range(2):
            self._bklog1.insert_item(self._items[i])
        self.assertEqual(self._bklog1.get_items()[1], self._item1)
        self.assertEqual(self._bklog1.get_items()[4], self._item2)


    # SORTING
    def test_that_changing_sorting_on_an_empty_backlog_does_not_affect_the_backlog_items(self):
        '''Tests that the changing the sorting method for an empty backlog does not change its items'''
        prev_list = self._bklog1.get_items()
        self._bklog1.change_sort("genre")

        self.assertListEqual(self._bklog1.get_items(), prev_list)

    def test_that_changing_the_current_key_of_a_backlog_sorts_its_items_in_the_proper_order(self):
        '''Tests that changing the current key sorts ot the backlog to the new desired order'''
        self._bklog2.change_sort("price")

        self.assertListEqual(self._bklog2.get_items(), [self._item5, self._item2, self._item3, self._item1,
                                                        self._item4])

    # REMOVAL
    def test_that_removing_from_an_empty_backlog_raises_an_underflow_error(self):
        '''Tests if attempting to remove from an empty backlog raises an error'''
        with self.assertRaises(media_sublist.MSUnderflowException):
            self._bklog1.remove_item(1)

    def test_that_removing_from_a_one_item_backlog_ends_up_making_an_empty_backlog(self):
        '''Tests if removing the item from a one item backlog makes the backlog's item list empty'''
        self._bklog1.insert_item(self._item4)

        self.assertEqual(len(self._bklog1.get_items()), 1)

        self._bklog1.remove_item(0)
        self.assertListEqual(self._bklog1.get_items(), [])

    def test_that_removing_from_a_multiple_item_backlog_works_as_intended(self):
        '''Tests if removing an item from a multiple item backlog removes said item and maintains order of items'''
        self._bklog2.change_sort("release")
        self._bklog2.remove_item(2)

        self.assertEqual(len(self._bklog2.get_items()), 4)
        self.assertListEqual(self._bklog2.get_items(), [self._item3, self._item2, self._item4, self._item1])

    # EDITING ENTRIES
    def test_that_editing_an_entry__s_properties_changes_its_member_variables_when_it_doesn__t_change_order(self):
        '''Tests if editing a backlog's items properly changes its member variables' values (considering cases where
        the edit wouldn't change the order of the list)'''
        sequel = "SATURATION II"
        tracklist = "01. GUMMY\n02. QUEER\n03. JELLO\n04. TEETH\n05. SWAMP\n06. SCENE\n07. TOKYO\n08. JESUS\n09. "\
                    + "CHICK\n10. JUNKY\n12. FIGHT\n13. SWEET\n14. GAMBA\n15. SUNNY\n16. SUMMER"
        proper_credits = "Kanye West et. al"
        self._bklog2.edit_item(1, "name", sequel)
        self._bklog2.edit_item(1, "notes", tracklist)
        self._bklog2.edit_item(3, "author", proper_credits)

        self.assertEqual(self._bklog2.get_items()[1].get_name(), sequel)
        self.assertEqual(self._bklog2.get_items()[1].get_notes(), tracklist)
        self.assertEqual(self._bklog2.get_items()[3].get_author(), proper_credits)

    def test_that_editing_an_entry_when_its_edited_property_is_the_key_changes_its_position_in_the_backlog(self):
        '''Tests that editing a backlog's item when the edit would alter where the item should be would properly
        reposition the entry and maintain all other properties of the backlog relative to the edit'''
        self._bklog1.change_sort("author")
        for i in range(5):
            self._bklog1.insert_item(self._items[i])
        self._item5.set_author("z")
        self._bklog1.edit_item(0, "author", "z")

        self.assertNotEqual(self._bklog1.get_items()[0].get_author(), "z")
        self.assertListEqual(self._bklog1.get_items(), [self._item1, self._item4, self._item3, self._item2,
                                                        self._item5])


if __name__ == '__main__':
    unittest.main()
