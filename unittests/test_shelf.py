'''
test_shelf.py
-Tests the functionality of the Shelf class

Traven 'tkgonzal' Gonzales 2019
'''


import unittest
import entry
import shelf


class ShelfTest(unittest.TestCase):
    '''Unittests for the Shelf class'''


    # SET UP
    def setUp(self):
        '''Sets up the variables needed for testing'''
        # Entry LIST VARIABLES
        self._backlog1 = []
        self._backlog2 = [entry.Entry("", "", "", i, 0, 1, "") for i in range(5)]
        self._completed = [entry.Entry("", "", "", i, 0, 1, "") for i in range(5)]
        for e in self._completed:
            e.set_completed()


        # Shelf VARIABLES
        self._shelf1 = shelf.Shelf("Empty")
        self._shelf2 = shelf.Shelf("With-Items",
                                   {"3": ([], []), "1": (self._backlog2, []), "2": (self._backlog2, self._completed)})


    # INITIALIZATION
    def test_if_initializing_a_shelf_without_a_prev_shelf_argument_makes_an_empty_shelf(self):
        '''Tests if calling the Shelf constructor without an argument for its prev_shelf parameter would create a Shelf
        with the correct name and a media variable that is an empty list, signifying that the shelf is empty'''
        self.assertEqual(self._shelf1.get_name(), "Empty")
        self.assertEqual(len(self._shelf1.get_media()), 0)

    def test_if_initializing_with_a_dict_properly_recreates_the_previous_shelf__s_data(self):
        '''Tests that a Shelf constructed with a string-list of Entry tuple dictionary will properly construct a
        Shelf whose List of Media_List follows the info in the provided dict argument and are sorted'''
        self.assertEqual(len(self._shelf2.get_media()), 3)
        for i in range(3):
            self.assertEqual(self._shelf2.get_media()[i].get_type(), f"{i + 1}")
        self.assertEqual(len(self._shelf2.get_media()[0].get_backlog()), 5)
        self.assertEqual(len(self._shelf2.get_media()[0].get_completed()), 0)
        self.assertEqual(len(self._shelf2.get_media()[1].get_backlog()), 5)
        self.assertEqual(len(self._shelf2.get_media()[1].get_completed()), 5)
        self.assertEqual(len(self._shelf2.get_media()[2].get_backlog()), 0)
        self.assertEqual(len(self._shelf2.get_media()[2].get_completed()), 0)

    def test_if_initializing_with_a_dict_whose_length_is_beyond_the_limits_of_the_shelf_makes_a_shortened_shelf(self):
        '''Tests if providing a dict whose length is larger than the capacity of a shelf properly recreates the shelf
        to have only the first items of the dict, after sorting, to fill up the capacity'''
        test = shelf.Shelf("test", {f"{i}": ([], []) for i in range(shelf.Shelf.get_media_limit(), -1, -1)})

        self.assertEqual(len(test.get_media()), shelf.Shelf.get_media_limit())


    # ADDING A Media_List
    def test_if_adding_to_an_empty_shelf_makes_the_shelf_one_media_list_long(self):
        '''Tests if adding to an empty Shelf results in it having one empty Media_List'''
        self._shelf1.add_media("Music")

        self.assertEqual(len(self._shelf1.get_media()), 1)
        self.assertEqual(len(self._shelf1.get_media()[0].get_backlog()), 0)
        self.assertEqual(len(self._shelf1.get_media()[0].get_completed()), 0)

    def test_if_adding_to_a_shelf_with_media_will_properly_add_the_specified_media(self):
        '''Tests if adding to a Shelf with media results in it having a one item longer than before Shelf and the media
        being placed in the correct position'''
        prev_len = len(self._shelf2.get_media())
        self._shelf2.add_media("11")

        self.assertEqual(self._shelf2.get_media()[1].get_type(), "11")
        self.assertEqual(len(self._shelf2.get_media()), prev_len + 1)

    def test_if_adding_to_a_shelf_at_capacity_raises_an_overrflow_exception(self):
        '''Tests if attempting to add to an at capacity shelf causes it to raise a ShelfOverflowException'''
        test = shelf.Shelf("test", {f"{i}": ([], []) for i in range(shelf.Shelf.get_media_limit() - 1, -1, -1)})

        with self.assertRaises(shelf.ShelfOverflowException):
            test.add_media("Movies")


    # REMOVING A Media_List
    def test_if_removing_from_a_shelf_with_items_makes_it_one_item_shorter_and_missing_the_removed_item(self):
        '''Tests if the remove_media method works as intended shortening the Shelf by 1 and removing the Media_List at
        the provided index from the list'''
        prev_len = len(self._shelf2.get_media())
        self._shelf2.remove_media(2)

        self.assertEqual(len(self._shelf2.get_media()), prev_len - 1)
        for i in range(len(self._shelf2.get_media())):
            self.assertTrue(self._shelf2.get_media()[i].get_type() != "3")

    def test_if_attempting_to_remove_from_an_empty_shelf_results_in_the_shelf_raising_an_undeflow_error(self):
        '''Tests if calling remove_media on an empty Shelf raises the ShelfUnderflowError'''
        with self.assertRaises(shelf.ShelfUndeflowException):
            self._shelf1.remove_media(420)


if __name__ == '__main__':
    unittest.main()
