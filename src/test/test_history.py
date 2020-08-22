#!
import unittest

class TestLineHistoryDunderMethods(unittest.TestCase):
    def setUp(self):
        self.buf = LineHistory()

    def test_index(self):
        # Does get_history_item say, index starts at 1?
        # FFS this passed
        with self.assertRaises(IndexError):
            self.buf.get_history_item(0)

    def test_adding_a_ReadLineTextBuffer_to_the_history(self):
        # like we jump through some acrobatic hoops for seemingly no reason
        self.buf.add_history("a simple str")
        # NOPE! This actually doesn't pass as the str and the list are both
        # modified to our fucked ReadLineTextBuffer
        self.assertEqual(self.buf.history, ["a simple str"])
        self.assertEqual(self.buf.get_history_item(0), "a simple str")

    def test_getitem(self):
        self.buf = LineHistory()
        self.buf.add_history("a simple str")
        self.assertEqual(self.buf[0], "a simple str")

    def test_add(self):
        self.adding_buffer = LineHistory()
        self.adding_buffer + "Cross your fingers"
        self.assertEqual(self.buf[0], "Cross your fingers")

    def test_len(self):
        self.buf2 = LineHistory()
        self.buf2.add_history("Anything")
        self.assertEqual(len(self.buf2), 1)
        del self.buf2.history[0]

    def test_a_new_one(self):
        self.new_buffer = LineHistory()
        self.assertLess(len(self.new_buffer), 1)


if __name__ == "__main__":
    unittest.main()
