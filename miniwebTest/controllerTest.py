from miniwebTest.uunittest import TestCase
from miniweb.entity.controller import Controller


class ControllerTestCase(TestCase):


    def test_controller_path(self):
        path = "/unit/test1/"
        test_controller = Controller(path)
        self.assertEqual(path, test_controller.path)


    def test_add_none_fc(self):
        path = "/unit/test2/"
        test_controller = Controller(path)
        len_before = len(test_controller.filters)
        test_controller.add_filter(None)
        len_after = len(test_controller.filters)
        self.assertEqual(len_before, len_after)


    def test_add_fc(self):
        path = "/unit/test3/"
        test_controller = Controller(path)
        len_before = len(test_controller.filters)

        def some_fc():
            pass

        test_controller.add_filter(some_fc)
        len_after = len(test_controller.filters)
        self.assertEqual(len_before+1, len_after)


    def test_empty_path_default(self):
        default = "/default/"
        test_controller = Controller(None)
        self.assertEqual(default, test_controller.path)
