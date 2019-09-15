'''
test_completed_list.py
-Tests the Completed_List class's functionality, though only the unique behaviour it exhibits compared to its parent
 class and the Current_Backlog class. Separated from the test_media_sublist unittests due to its setting of time of its
 items.

Traven 'tkwtph' Gonzales 2019
'''


import unittest
import time
import entry
import completed_list


class CompletedListTest(unittest.TestCase):
    '''Tests the functionality and behaviour of the Completed_List class'''


    # SET UP
    def setUp(self):
        '''Sets up variables used for unit testing'''
        # TEST ENTRIES
        self._item1 = entry.Entry("The Money Store", "Death Grips", "Experimental Hip-Hop", 11.99, 2012, 3, "strong 10")
        self._item2 = entry.Entry("In the Court of the Crimson King", "King Crimson", "Progressive Rock", 15.99, 1969,
                                  5, "It just works.")
        self._item3 = entry.Entry("Happy Bivouac", "the pillows", "Indie Rock", 13.99, 1999, 1,
                                  "i had a fever dream studio trigger produced two mediocre FLCL OVA spin offs")
        self._item4 = entry.Entry("Beneath the Toxic Jungle", "Rav", "Abstract Hip-Hop", 0.00, 2015, 4, "ant urine")
        self._item5 = entry.Entry("Nonagon Infinity", "King Gizzard and the Lizard Wizard", "Psychadelic Rock", 20.99,
                                  2016, 2, "NONAGON INFINITY OPENS THE DOOR")
        self._item6 = entry.Entry("IGOR", "Tyler, the Creator", "Neo-Soul", 9.99, 2019, 3, "sad boy hours")
        self._item7 = entry.Entry("Chloe Burbank vol. 1", "Joji", "lo-fi", 0, 2016, 5, "peak joji")
        self._item8 = entry.Entry("Odorenai nara, Gesu ni Natte Shimae", "Gesu no Kiwami Otome", "Indie Rock", 15.99,
                                  2013, 4, "lowkey math rock")
        self._items = [self._item1, self._item2, self._item3, self._item4, self._item5, self._item6, self._item7,
                       self._item8]
        # For and while loop used to mark each item as completed with a second difference between each item
        for i in range(7, -1, -1):
            start = time.time()
            while time.time() - start < .125:
                continue
            self._items[i].set_completed()

        # TEST COMPLETED LISTS
        self._clist1 = completed_list.Completed_List()
        self._clist2 = completed_list.Completed_List(self._items[:5])


    # INITIALIZATION
    def test_if_default_initialization_creates_an_empty_completed_list(self):
        '''Tests if initializing a Completed_List without passing it an items argument makes an empty Completed_List'''
        self.assertEqual(len(self._clist1.get_items()), 0)

    def test_if_initializing_with_an_items_arguments_creates_a_completed_list_with_a_sorted_list_of_items(self):
        '''Tests if initializing a Completed_List with an items arguments makes a Completed_List with a correct items
        argument'''
        self.assertEqual(len(self._clist2.get_items()), completed_list.Completed_List._ITEMS_LIMIT)
        self.assertListEqual(self._clist2.get_items(), [self._item5, self._item4, self._item3, self._item2,
                                                        self._item1])

    def test_if_initializing_with_an_items_arg_that_exceeds_the_item_limit_is_handled_properly(self):
        '''Testing if initializing with an items arg whose length is more than the items limit of the Completed_Lists
        results in the Completed_List's item list being a truncated version of the first few items of the argument'''
        test = completed_list.Completed_List(self._items)

        self.assertEqual(len(test.get_items()), completed_list.Completed_List._ITEMS_LIMIT)
        self.assertListEqual(test.get_items(), [self._item5, self._item4, self._item3, self._item2, self._item1])


    # INSERTION
    def test_if_inserting_into_an_empty_completed_list_acts_normally(self):
        '''Tests if inserting an item into an empty Completed_List adds the item to its contents'''
        self._clist1.insert_item(self._item4)

        self.assertEqual(len(self._clist1.get_items()), 1)
        self.assertListEqual(self._clist1.get_items(), [self._item4,])

    def test_if_inserting_into_an_at_capacity_completed_list_gets_rid_of_the_oldest_entry_when_on_default_key(self):
        '''Tests if inserting into an at capacity Completed_List removes the oldest entry in the list and properly adds
        the next item when the Completed_List's current key is the default key'''
        test = completed_list.Completed_List(self._items[1:6])
        test.insert_item(self._item1)

        self.assertEqual(len(test.get_items()), completed_list.Completed_List._ITEMS_LIMIT)
        self.assertListEqual(test.get_items(), [self._item5, self._item4, self._item3, self._item2, self._item1])

    def test_if_inserting_into_an_at_capcity_completed_list_works_as_intended_on_a_non_default_key(self):
        '''Test if inserting into an at capacity completed list works as intended when the current key is not on the
        default key: changing the current key back into the default key, getting rid of the oldest entry then properly
        adding the newest entry'''
        self._clist1.change_sort("price")
        for i in range(7, 2, -1):
            self._clist1.insert_item(self._items[i])
        self._clist1.insert_item(self._item3)

        self.assertEqual(len(self._clist1.get_items()), completed_list.Completed_List._ITEMS_LIMIT)
        self.assertListEqual(self._clist1.get_items(), [self._item7, self._item6, self._item5, self._item4,
                                                        self._item3])


if __name__ == '__main__':
    unittest.main()
