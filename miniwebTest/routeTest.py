from miniwebTest.uunittest import TestCase
from miniweb.core.miniweb import app
from miniweb.entity.controller import Controller
import ure


def get_miniweb_test():
    params = {
        "port": 8000,
        "log": 9999,
        "host": "localhost"
    }
    return app(params)



class RouteTestCase(TestCase):


    def test_add_get_route(self):
        app = get_miniweb_test()
        len_before = len(app.routes)
        @app.get("/addtest/get")
        def test():
            pass
        #after adding route routes len should be +1
        len_after = len(app.routes)
        self.assertEqual(len_before+1, len_after)


    def test_add_post_route(self):
        app = get_miniweb_test()
        len_before = len(app.routes)
        @app.post("/addtest/post")
        def test():
            pass
        #after adding route routes len should be +1
        len_after = len(app.routes)
        self.assertEqual(len_before+1, len_after)


    def test_add_put_route(self):
        app = get_miniweb_test()
        len_before = len(app.routes)

        @app.put("/addtest/put")
        def test():
            pass

        # after adding route routes len should be +1
        len_after = len(app.routes)
        self.assertEqual(len_before + 1, len_after)


    def test_add_delete_route(self):
        app = get_miniweb_test()
        len_before = len(app.routes)

        @app.delete("/addtest/delete")
        def test():
            pass

        # after adding route routes len should be +1
        len_after = len(app.routes)
        self.assertEqual(len_before + 1, len_after)


    def test_add__route(self):
        app = get_miniweb_test()
        len_before = len(app.routes)

        @app.route("/addtest/route", ["GET", "POST"])
        def test():
            pass

        # after adding route routes len should be +1
        len_after = len(app.routes)
        self.assertEqual(len_before + 1, len_after)


    def test_add_static_route(self):
        app = get_miniweb_test()
        len_before = len(app.routes)
        app.static_router(root="/home/test", path="/test/")
        # after adding route routes len should be +1
        len_after = len(app.routes)
        self.assertEqual(len_before+1, len_after)


    def test_controller_prefix_path(self):
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
        app = get_miniweb_test()

        @app.route("/routewithnonetmethod", None)
        def test():
            pass

        result = True
        for route in app.routes:
            if route.path == "/routewithnonetmethod":
                result = False
                break

        self.assertTrue(result)


    def test_route_without_path(self):
        app = get_miniweb_test()

        @app.get(None)
        def test():
            pass

        #if not exception then pass
        self.assertTrue(True)


    def test_match_path_success(self):
        app = get_miniweb_test()
        path = "/complexpath/{user}/test/{test}/anothertext/{anotherParam}"

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
        app = get_miniweb_test()
        path = "/complexpathtofail/{user}/subparam/{anotherUser}/{lastParam}"

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
