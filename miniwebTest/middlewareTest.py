from miniwebTest.uunittest import TestCase
from miniweb.entity.middleware import *
from miniweb.message.response import Response
from miniweb.entity.controller import Controller
from miniweb.core.miniweb import app as get_miniweb


class MiddlewareTestCase(TestCase):


    def test_add_global_filter(self):
        len_before = len(global_filter)

        @filter()
        def filter_fc(req, res):
            return True

        len_after = len(global_filter)
        self.assertEqual(len_before+1, len_after)


    def test_controller_filter_wont_add_to_global(self):
        middleware_controller = Controller("/middlewaretest1/")
        len_before_global = len(global_filter)

        @filter(middleware_controller)
        def filter_fc(req, res):
            return True

        len_after_global = len(global_filter)
        self.assertEqual(len_before_global, len_after_global)


    def test_add_controller_filter(self):
        middleware_controller = Controller("/middlewaretest2/")
        len_before = len(middleware_controller.filters)

        @filter(middleware_controller)
        def filter_fc(req, res):
            return True

        len_after = len(middleware_controller.filters)
        self.assertEqual(len_before+1, len_after)


    def test_middleware_is_called(self):
        app = get_miniweb()

        @filter()
        def test(req, res):
            res.test = "FILTER_CALLED"
            return True

        @app.get("/middleware10/test1")
        def some_fc(req, res):
            pass

        res_obj = Response()
        some_fc(None, res_obj)
        self.assertEqual(res_obj.test, "FILTER_CALLED")


    def test_middleware_success(self):
        app = get_miniweb()

        @filter()
        def test(req, res):
            return True

        @app.get("/middleware11/test1")
        def some_fc(req, res):
            res.test = "DECORATED_FUNCTION_CALLED"
            pass

        res_obj = Response()
        some_fc(None, res_obj)
        self.assertEqual(res_obj.test, "DECORATED_FUNCTION_CALLED")


    def test_middleware_fail(self):
        app = get_miniweb()

        @filter()
        def test(req, res):
            return False

        @app.get("/middleware12/test1")
        def some_fc(req, res):
            res.test = "DECORATED_FUNCTION_CALLED"
            pass

        res_obj = Response()
        result_fc = some_fc(None, res_obj)
        self.assertNotEqual(res_obj.test, "DECORATED_FUNCTION_CALLED")
