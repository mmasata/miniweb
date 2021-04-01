from miniwebTest.uunittest import TestCase
from miniweb.core.miniweb import app
from miniweb.entity.controller import Controller
import ure


def get_miniweb_test():
    """
    Create or get singleton of miniweb instance for test purposes.
    :return: Miniweb instance
    """
    #test params, we dont want to additional logging
    params = {
        "port": 8000,
        "log": 9999,
        "host": "localhost"
    }
    return app(params)



class RouteTestCase(TestCase):
    """
    Class for Route unit tests.
    """


    def test_add_get_route(self):
        """
        Test of adding get route to miniweb instance.
        Check route array length changes.
        :return: Test result
        """
        app = get_miniweb_test()
        len_before = len(app.routes)

        #create simple get router
        @app.get("/addtest/get")
        def test():
            pass
        #after adding route routes len should be +1
        len_after = len(app.routes)
        self.assertEqual(len_before+1, len_after)


    def test_add_post_route(self):
        """
        Test of adding post route to miniweb instance.
        Check route array length changes.
        :return: Test result
        """
        app = get_miniweb_test()
        len_before = len(app.routes)

        # create simple post router
        @app.post("/addtest/post")
        def test():
            pass
        #after adding route routes len should be +1
        len_after = len(app.routes)
        self.assertEqual(len_before+1, len_after)


    def test_add_put_route(self):
        """
        Test of adding put route to miniweb instance.
        Check route array length changes.
        :return: Test result
        """
        app = get_miniweb_test()
        len_before = len(app.routes)

        # create simple put router
        @app.put("/addtest/put")
        def test():
            pass

        # after adding route routes len should be +1
        len_after = len(app.routes)
        self.assertEqual(len_before + 1, len_after)


    def test_add_delete_route(self):
        """
        Test of adding delete route to miniweb instance.
        Check route array length changes.
        :return: Test result
        """
        app = get_miniweb_test()
        len_before = len(app.routes)

        # create simple delete router
        @app.delete("/addtest/delete")
        def test():
            pass

        # after adding route routes len should be +1
        len_after = len(app.routes)
        self.assertEqual(len_before + 1, len_after)


    def test_add__route(self):
        """
        Test of adding route to miniweb instance.
        Check route array length changes.
        :return: Test result
        """
        app = get_miniweb_test()
        len_before = len(app.routes)

        # create simple router
        @app.route("/addtest/route", ["GET", "POST"])
        def test():
            pass

        # after adding route routes len should be +1
        len_after = len(app.routes)
        self.assertEqual(len_before + 1, len_after)


    def test_add_static_route(self):
        """
        Test of adding static route to miniweb instance.
        Check route array length changes.
        :return: Test result
        """
        app = get_miniweb_test()
        len_before = len(app.routes)
        # create simple static router
        app.static_router(root="/home/test", path="/test/")
        # after adding route routes len should be +1
        len_after = len(app.routes)
        self.assertEqual(len_before+1, len_after)


    def test_controller_prefix_path(self):
        """
        Test of join controller path to router.
        :return: Test result
        """
        app = get_miniweb_test()
        #at this moment path should not be inside of routes
        is_not_route_before = False
        for route in app.routes:
            if route.path == "/testcontroller/routeincontroller":
                is_not_route_before = True
                self.fail()
                break

        #now we add this path to routes
        test_controller = Controller("/testcontroller/")
        @app.get("routeincontroller", controller=test_controller)
        def test():
            pass

        #now this path should be stored in routes
        is_route_after = False
        for route in app.routes:
            if route.path == "/testcontroller/routeincontroller":
                is_route_after = True
                break
        self.assertFalse(is_not_route_before, is_route_after)


    def test_route_none_method(self):
        """
        Test of adding route without method.
        Route should not be registered.
        :return: Test result
        """
        app = get_miniweb_test()

        #create route with None method
        @app.route("/routewithnonetmethod", None)
        def test():
            pass

        #result should not be changed, because route was not registered
        result = False
        for route in app.routes:
            if route.path == "/routewithnonetmethod":
                result = True
                break

        self.assertFalse(result)


    def test_route_without_path(self):
        """
        Test of adding route without path.
        Route should not be registered, without exception.
        :return: Test result
        """
        app = get_miniweb_test()

        #create route with None path
        @app.get(None)
        def test():
            pass

        #if not exception then pass
        self.assertTrue(True)


    def test_match_path_success(self):
        """
        Test of register route with dynamic path parameters.
        Matching method should recognize pattern.
        :return: Test result
        """
        app = get_miniweb_test()
        path = "/complexpath/{user}/test/{test}/anothertext/{anotherParam}"

        #create route with dynamic path
        @app.get(path)
        def test():
            pass

        #this path should match with defined dynamic path
        match_param = "/complexpath/John/test/MyTestParam/anothertext/AnotherParamTest"
        match = False
        for route in app.routes:
            if route.path is path:
                match, params = route.match_with_vars(match_param)
                break
        self.assertTrue(match)


    def test_match_path_fail(self):
        """
        Test of register route with dynamic path parameters.
        Matching method should not recognize pattern in wrong path.
        :return: Test result
        """
        app = get_miniweb_test()
        path = "/complexpathtofail/{user}/subparam/{anotherUser}/{lastParam}"

        #create route with dynamic path
        @app.put(path)
        def test():
            pass

        # this path should not match with defined dynamic path
        match_param = "/complexpathtofailDIFERENT/SomeCoolName/subparam/VeryLongName/LastParamOnTheEnd"
        match = False
        for route in app.routes:
            if route.path is path:
                match, params = route.match_with_vars(match_param)
                break
        self.assertFalse(match)


    def test_path_variables(self):
        """
        Test of path parameters and their access via injected parameter.
        Dynamic parameters should be paired to key-value format.
        :return: Test result
        """
        app = get_miniweb_test()
        path = "/pathparamtest/key/{key}/value/{value}/fullname/{firstname}/{lastname}"

        @app.put(path)
        def test():
            pass

        #will check if params are correct
        match_param = "/pathparamtest/key/MINIWEB1/value/123456789/fullname/John/Smith"
        params_check = {
            "key": "MINIWEB1",
            "value": "123456789",
            "firstname": "John",
            "lastname": "Smith"
        }
        params = None
        for route in app.routes:
            if route.path is path:
                match, params = route.match_with_vars(match_param)
                break

        is_equal = params_check == params
        self.assertTrue(is_equal)
