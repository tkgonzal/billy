'''
test_media_list.py
-Unittests for the Media_List class.

Traven 'tkwtph' Gonzales 2019
'''


import unittest
import time
import entry
import media_list
import media_sublist


# FUNCTION FOR MAKING WAIT TIME
def wait_time(): # ZA WARUDO
    '''Creates a wait time of .125 seconds. Used in testing for differentiating datetimes'''
    start = time.time()
    while time.time() - start < .125:
        continue


class MediaListTest(unittest.TestCase):
    '''Tests the functionality of the Media_List class's methods'''


    # SET UP
    def setUp(self):
        '''Sets up the variables used for unittesting'''
        # Entry OBJECTS FOR TESTING
        # Entry OBJECTS FOR Media_Sublist'S BACKLOG
        self._b_item1 = entry.Entry("SATURATION", "BROCKHAMPTON", "Hip-Hop", 9.99, 2017, 5,
                                    "best boy band in the world")
        wait_time()
        self._b_item2 = entry.Entry("A Fever You Can't Sweat Out", "Panic! at the Disco", "Pop Punk", 9.99, 2005, 4,
                                    "I miss the old p!atd")
        wait_time()
        self._b_item3 = entry.Entry("In the Aeroplane Over the Sea", "Neutral Milk Hotel", "Indie Rock", 9.99, 1998, 4,
                                    "WHAT A BEAUTIFUL PLACE I HAVE FOUND IN THIS PLACE")
        wait_time()
        self._b_item4 = entry.Entry("My Beautiful Dark Twisted Fantasy", "Kanye West", "Hip-Hop", 13.99, 2010, 5, "")
        wait_time()
        self._b_item5 = entry.Entry("Whatever People Say I am That's What I'm Not", "Arctic Monkeys", "Indie Rock",
                                    7.99, 2006, 2, "the only good arctic monkeys album")
        wait_time()
        self._b_items = [self._b_item1, self._b_item2, self._b_item3, self._b_item4, self._b_item5]

        # Entry OBJECTS FOR Media_Sublist'S COMPLETED SECTION
        self._c_item1 = entry.Entry("The Money Store", "Death Grips", "Experimental Hip-Hop", 11.99, 2012, 3,
                                    "strong 10")
        self._c_item2 = entry.Entry("In the Court of the Crimson King", "King Crimson", "Progressive Rock", 15.99, 1969,
                                    5, "It just works.")
        self._c_item3 = entry.Entry("Happy Bivouac", "the pillows", "Indie Rock", 13.99, 1999, 1,
                                    "i had a fever dream studio trigger produced two mediocre FLCL OVA spin offs")
        self._c_item4 = entry.Entry("Beneath the Toxic Jungle", "Rav", "Abstract Hip-Hop", 0.00, 2015, 4, "ant urine")
        self._c_item5 = entry.Entry("Nonagon Infinity", "King Gizzard and the Lizard Wizard", "Psychadelic Rock", 20.99,
                                    2016, 2, "NONAGON INFINITY OPENS THE DOOR")
        self._c_item6 = entry.Entry("IGOR", "Tyler, the Creator", "Neo-Soul", 9.99, 2019, 3, "sad boy hours")
        self._c_item7 = entry.Entry("Chloe Burbank vol. 1", "Joji", "lo-fi", 0, 2016, 5, "peak joji")
        self._c_item8 = entry.Entry("Odorenai nara, Gesu ni Natte Shimae", "Gesu no Kiwami Otome", "Indie Rock", 15.99,
                                    2013, 4, "lowkey math rock")
        self._c_items = [self._c_item1, self._c_item2, self._c_item3, self._c_item4, self._c_item5, self._c_item6,
                         self._c_item7, self._c_item8]
        # For and while loop used to mark each item as completed with a .125 difference between each item
        for i in range(7, -1, -1):
            wait_time()
            self._c_items[i].set_completed()


        # Media_Lists FOR TESTING
        self._mlist1 = media_list.Media_List("Music")
        self._mlist2 = media_list.Media_List("Music", self._b_items, self._c_items)


    # INITIALIZATION
    def test_if_a_media_list_can_be_initialized_as_empty_by_default(self):
        '''Tests if a Media_List constructed without arguments creates a Media_List whose sublists are empty'''
        self.assertEqual(len(self._mlist1.get_backlog()), 0)
        self.assertEqual(len(self._mlist1.get_completed()), 0)

    def test_if_a_media_list_can_be_initialized_with_item_arguments(self):
        '''Tests if a Media_List can be constructed without arguments creating a Media_List with proper sublists'''
        self.assertEqual(len(self._mlist2.get_backlog()), len(self._b_items))
        self.assertEqual(self._mlist2.get_backlog(), [self._b_item1, self._b_item4, self._b_item2, self._b_item3,
                                                      self._b_item5])
        self.assertEqual(len(self._mlist2.completed.get_items()), self._mlist2.get_completed_limit())

    # MARKING AS COMPLETED
    def test_if_marking_an_item_as_completed_in_a_one_item_backlog_adds_properly_to_an_empty_completed_list(self):
        '''Tests if marking an item completed in a one item backlog will make a Media_List's one item backlog empty
        and its empty completed list one Entry long'''
        self._mlist1.backlog.insert_item(self._b_item1)
        self._mlist1.mark_complete(0)

        self.assertEqual(len(self._mlist1.get_backlog()), 0)
        self.assertEqual(len(self._mlist1.get_completed()), 1)
        self.assertEqual(self._mlist1.get_completed(), [self._b_item1])

    def test_if_marking_an_item_complete_when_completed_is_at_capacity_discards_oldest_entry_in_completed(self):
        '''Tests if marking an Entry as completed in the backlog properly removes the Entry from the backlog and places
        it in the completed list, with the completed list being at capacity causing it to remove its oldest entry in
        order to add the newly marked Entry into the completed section'''
        wait_time()
        self._mlist2.mark_complete(0)

        self.assertEqual(len(self._mlist2.get_backlog()), 4)
        self.assertEqual(len(self._mlist2.get_completed()), self._mlist2.get_completed_limit())

    # MARKING AS INCOMPLETE
    def test_if_marking_an_item_as_incomplete_would_move_it_from_the_complete_list_back_to_the_backlog(self):
        '''Tests if marking an Entry in the completed section as incomplete would remove it from the completed section
        and place it the backlog when the backlog has room'''
        wait_time()
        self._mlist2.mark_incomplete(0)

        self.assertEqual(len(self._mlist2.get_completed()), self._mlist2.get_completed_limit() - 1)
        self.assertEqual(len(self._mlist2.get_backlog()), 6)

    def test_if_marking_an_item_as_incomplete_when_the_backlog_is_at_capacity_raises_an_exception(self):
        '''Tests if marking an item as incomplete when the backlog is at capacity would fail, causing the Entry to be
        remarked as complete, reinserted back into the completed list'''
        for i in range(self._mlist2.get_backlog_limit() - 5):
            self._mlist2.backlog.insert_item(entry.Entry(f"{i}", f"{i}", f"{i}", i, i, 1, ""))

        with self.assertRaises(media_sublist.MSOverflowException):
            self._mlist2.mark_incomplete(0)
            self.assertEqual(len(self._mlist2.get_backlog()), self._mlist2.get_backlog_limit())
            self.assertEqual(len(self._mlist2.get_completed()), self._mlist2.get_completed_limit())




if __name__ == '__main__':
    unittest.main()
