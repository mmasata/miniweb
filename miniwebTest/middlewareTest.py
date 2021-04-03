from miniwebTest.uunittest import TestCase
import miniweb.entity.middleware as mw
from miniweb.message.response import Response
from miniweb.message.request import Request
from miniweb.entity.controller import Controller
from miniweb.core.miniweb import app as get_miniweb


def clear_global_filters():
    """
    Clear global filter array.
    Method for test purposes.
    :return: None
    """
    mw.global_filter = []


def clear_controller_filters(c):
    """
    Clear controller filter array.
    Method for test purposes.
    :param c: Controller instance
    :return: None
    """
    c.filter = []


class MiddlewareTestCase(TestCase):
    """
    Class for Middleware unit tests.
    """


    def test_add_global_filter(self):
        """
        Test of creating global filter function.
        Array size of filters should be bigger after register new filter.
        :return: Test result
        """
        len_before = len(mw.global_filter)

        #create new global filter
        @mw.filter()
        def filter_fc(req, res):
            return True

        #comparing array length before and after
        len_after = len(mw.global_filter)
        clear_global_filters()
        self.assertEqual(len_before+1, len_after)


    def test_controller_filter_not_global(self):
        """
        Test of creating controller filter function.
        Function should not be add to global filter array test.
        :return: Test result
        """

        #define controller
        middleware_controller = Controller("/middlewaretest1/")
        len_before_global = len(mw.global_filter)

        #create new controller filter
        @mw.filter(middleware_controller)
        def filter_fc(req, res):
            return True

        # comparing array length before and after
        len_after_global = len(mw.global_filter)
        clear_controller_filters(middleware_controller)
        self.assertEqual(len_before_global, len_after_global)


    def test_add_controller_filter(self):
        """
        Test of creating controller filter function.
        Array size of controller filters should be bigger after register new filter.
        :return: Test result
        """

        #define controller
        middleware_controller = Controller("/middlewaretest2/")
        len_before = len(middleware_controller.filters)

        # create new controller filter
        @mw.filter(middleware_controller)
        def filter_fc(req, res):
            return True

        # comparing array length before and after
        len_after = len(middleware_controller.filters)
        clear_controller_filters(middleware_controller)
        self.assertEqual(len_before+1, len_after)


    def test_middleware_is_called(self):
        """
        Test of calling middleware functions before route function execution.
        Middleware function passed, so route function should be called.
        Update response object from middleware function.
        :return: Test result
        """
        app = get_miniweb()

        #create new global filter
        @mw.filter()
        def test(req, res):
            #filter passed and update response instance
            res.test = "FILTER_CALLED"
            return True

        #create get route
        @app.get("/middleware10/test1")
        def some_fc(req, res):
            pass

        #response should be updated from middleware function
        res_obj = Response()
        some_fc(None, res_obj)
        clear_global_filters()
        self.assertEqual(res_obj.test, "FILTER_CALLED")


    def test_middleware_success(self):
        """
        Test of middleware function pass.
        Route function should be called test.
        Update response object from route function.
        :return: Test result
        """
        app = get_miniweb()

        #create new global filter
        @mw.filter()
        def test(req, res):
            return True

        #create get route
        @app.get("/middleware11/test1")
        def some_fc(req, res):
            #route function update response instance
            res.test = "DECORATED_FUNCTION_CALLED"
            pass

        # response should be updated from route function
        res_obj = Response()
        some_fc(None, res_obj)
        clear_global_filters()
        self.assertEqual(res_obj.test, "DECORATED_FUNCTION_CALLED")


    def test_middleware_fail(self):
        """
        Test of middleware function fail.
        Route function should not be called.
        Route function will not update response object.
        :return: Test result
        """
        app = get_miniweb()

        #create new global filter
        @mw.filter()
        def test(req, res):
            return False

        #create get route
        @app.get("/middleware12/test1")
        def some_fc(req, res):
            #response object will not be edited, because this function will not be called
            res.test = "DECORATED_FUNCTION_CALLED"
            pass


        res_obj = Response()
        res_obj.test = "NOT_CALLED"
        some_fc(None, res_obj)
        clear_global_filters()
        self.assertNotEqual(res_obj.test, "DECORATED_FUNCTION_CALLED")


    def test_consumes_success(self):
        """
        Test of special middleware function - consumes.
        Will check content type from request and will call route function.
        :return: Test result
        """
        app = get_miniweb()

        #create get route with consume filter
        @app.get("/middleware13/test1", consumes=["application/json"])
        def some_fc(req, res):
            res.test = "DECORATED_FUNCTION_CALLED"
            pass

        #request object with correct content type
        req_obj = Request()
        req_obj.headers["Content-Type"] = "application/json"
        res_obj = Response()
        some_fc(req_obj, res_obj)
        self.assertEqual(res_obj.test, "DECORATED_FUNCTION_CALLED")


    def test_consumes_fail(self):
        """
        Test of special middleware function - consumes.
        Will check content type from request.
        This test should fail and route function will not be called.
        :return: Test result
        """
        app = get_miniweb()

        #create get route with consume filter
        @app.get("/middleware14/test1", consumes=["application/json"])
        def some_fc(req, res):
            res.test = "DECORATED_FUNCTION_CALLED"
            pass

        #request object with wrong content type
        req_obj = Request()
        req_obj.headers["Content-Type"] = "multipart/form-data"
        res_obj = Response()
        res_obj.test = "NOT_CALLED"
        some_fc(req_obj, res_obj)
        self.assertNotEqual(res_obj.test, "DECORATED_FUNCTION_CALLED")
