from miniwebTest.uunittest import TestCase
import miniweb.entity.middleware as mw
from miniweb.message.response import Response
from miniweb.message.request import Request
from miniweb.entity.controller import Controller
from miniweb.core.miniweb import app as get_miniweb


def clear_global_filters():
    mw.global_filter = []


def clear_controller_filters(c):
    c.filter = []


class MiddlewareTestCase(TestCase):


    def test_add_global_filter(self):
        len_before = len(mw.global_filter)

        @mw.filter()
        def filter_fc(req, res):
            return True

        len_after = len(mw.global_filter)
        clear_global_filters()
        self.assertEqual(len_before+1, len_after)


    def test_controller_filter_wont_add_to_global(self):
        middleware_controller = Controller("/middlewaretest1/")
        len_before_global = len(mw.global_filter)

        @mw.filter(middleware_controller)
        def filter_fc(req, res):
            return True

        len_after_global = len(mw.global_filter)
        clear_controller_filters(middleware_controller)
        self.assertEqual(len_before_global, len_after_global)


    def test_add_controller_filter(self):
        middleware_controller = Controller("/middlewaretest2/")
        len_before = len(middleware_controller.filters)

        @mw.filter(middleware_controller)
        def filter_fc(req, res):
            return True

        len_after = len(middleware_controller.filters)
        clear_controller_filters(middleware_controller)
        self.assertEqual(len_before+1, len_after)


    def test_middleware_is_called(self):
        app = get_miniweb()

        @mw.filter()
        def test(req, res):
            res.test = "FILTER_CALLED"
            return True

        @app.get("/middleware10/test1")
        def some_fc(req, res):
            pass

        res_obj = Response()
        some_fc(None, res_obj)
        clear_global_filters()
        self.assertEqual(res_obj.test, "FILTER_CALLED")


    def test_middleware_success(self):
        app = get_miniweb()

        @mw.filter()
        def test(req, res):
            return True

        @app.get("/middleware11/test1")
        def some_fc(req, res):
            res.test = "DECORATED_FUNCTION_CALLED"
            pass

        res_obj = Response()
        some_fc(None, res_obj)
        clear_global_filters()
        self.assertEqual(res_obj.test, "DECORATED_FUNCTION_CALLED")


    def test_middleware_fail(self):
        app = get_miniweb()

        @mw.filter()
        def test(req, res):
            return False

        @app.get("/middleware12/test1")
        def some_fc(req, res):
            print("CALLED")
            res.test = "DECORATED_FUNCTION_CALLED"
            pass


        res_obj = Response()
        res_obj.test = "NOT_CALLED"
        some_fc(None, res_obj)
        clear_global_filters()
        self.assertNotEqual(res_obj.test, "DECORATED_FUNCTION_CALLED")


    def test_consumes_success(self):
        app = get_miniweb()

        @app.get("/middleware13/test1", consumes=["application/json"])
        def some_fc(req, res):
            res.test = "DECORATED_FUNCTION_CALLED"
            pass

        req_obj = Request()
        req_obj.headers["Content-Type"] = "application/json"
        res_obj = Response()
        some_fc(req_obj, res_obj)
        self.assertEqual(res_obj.test, "DECORATED_FUNCTION_CALLED")


    def test_consumes_fail(self):
        app = get_miniweb()

        @app.get("/middleware14/test1", consumes=["application/json"])
        def some_fc(req, res):
            res.test = "DECORATED_FUNCTION_CALLED"
            pass

        req_obj = Request()
        req_obj.headers["Content-Type"] = "multipart/form-data"
        res_obj = Response()
        res_obj.test = "NOT_CALLED"
        some_fc(req_obj, res_obj)
        self.assertNotEqual(res_obj.test, "DECORATED_FUNCTION_CALLED")