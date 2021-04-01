from miniwebTest.uunittest import TestCase
from miniweb.entity.controller import Controller


class ControllerTestCase(TestCase):
    """
    Class for Controller unit tests.
    """


    def test_controller_path(self):
        """
        Test of correct controller path.
        :return: Test result
        """
        path = "/unit/test1/"
        test_controller = Controller(path)
        self.assertEqual(path, test_controller.path)


    def test_add_none_fc(self):
        """
        Test of adding None filter function to controller.
        Should not be added, and array size of filters should be same.
        :return: Test result
        """
        path = "/unit/test2/"
        test_controller = Controller(path)
        len_before = len(test_controller.filters)
        test_controller.add_filter(None)
        len_after = len(test_controller.filters)
        self.assertEqual(len_before, len_after)


    def test_add_fc(self):
        """
        Test of adding filter function to controller.
        Array size should be biger then before adding.
        :return: Test result
        """
        path = "/unit/test3/"
        test_controller = Controller(path)
        len_before = len(test_controller.filters)

        #define some function
        def some_fc():
            pass

        #add function and compare length before and after
        test_controller.add_filter(some_fc)
        len_after = len(test_controller.filters)
        self.assertEqual(len_before+1, len_after)


    def test_empty_path_default(self):
        """
        Test of creating controller with None path.
        Will create controller with "/default/" path.
        :return: Test result
        """
        default = "/default/"
        test_controller = Controller(None)
        self.assertEqual(default, test_controller.path)
