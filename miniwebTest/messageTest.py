from miniwebTest.uunittest import TestCase
from miniweb.message.response import Response
from miniweb.message.content import *


class ResponseTestCase(TestCase):
    """
    Class for Response unit tests.
    """


    def test_response_status_set(self):
        """
        Test of defining HTTP status to Response object.
        :return: Test result
        """

        res = Response()
        res.status(400)
        self.assertEqual(400, res.stat)


    def test_response_status_default(self):
        """
        Test of defautl value of HTTP status in Response object.
        Default value should be 500.
        :return: Test result
        """

        res = Response()
        self.assertEqual(500, res.stat)


    def test_response_type(self):
        """
        Test of defining MIME to Response object.
        :return: Test result
        """

        json = "application/json"
        res = Response()
        res.type(json)
        self.assertEqual(json, res.mime)


    def test_response_data(self):
        """
        Test of defining content data to Response object.
        :return: Test result
        """

        d = "TEST DATA"
        res = Response()
        res.entity(d)
        self.assertEqual(d, res.ent)


    def test_response_build(self):
        """
        Test of defining build parameter to Response object.
        :return: Test result
        """

        res = Response()
        res.build()
        self.assertTrue(res.can_send)



    def test_response_build_default(self):
        """
        Test of default build value.
        Value should be False.
        :return: Test result
        """

        res = Response()
        self.assertFalse(res.can_send)


class ContentTestCase(TestCase):
    """
    Class for Content unit tests.
    """


    def test_parse_content_json(self):
        """
        Test of parsing json string to dictionary.
        :return: Test result
        """

        json_str = '{"key":"value", "arr": [1,2,3,4]}'
        data_type = "application/json"
        response = get_content(json_str, data_type)
        is_correct = (response["key"] == "value" and len(response["arr"]) == 4)
        self.assertTrue(is_correct)


    def test_parse_unknown_type(self):
        """
        Test of parsing unknown data types.
        Should return original value.
        :return: Test result.
        """

        unknown_data = "Some data in unknown format!"
        data_type = "unknown/format"
        response = get_content(unknown_data, data_type)
        self.assertEqual(response, unknown_data)


    def test_form_data_single_line(self):
        """
        Test of parsing FormData single line parameter.
        Value should be accessable from class attribute named like original key.
        :return: Test result
        """

        test_data = '--BOUNDARY\r\nContent-Disposition: form-data; name="key"\r\n\r\ntestvalue\r\n--BOUNDARY'
        data_type = "multipart/form-data"
        response = get_content(test_data, data_type)
        self.assertEqual("testvalue", response.key)


    def test_form_data_multi_line(self):
        """
        Test of parsing FormData multi line parameter.
        Value should be accessable from class attribute named like original key.
        :return: Test result
        """

        test_data = '--BOUNDARY\r\nContent-Disposition: form-data; name="multikey"\r\n\r\nfirst\r\nsecond\r\n--BOUNDARY'
        data_type = "multipart/form-data"
        response = get_content(test_data, data_type)
        self.assertEqual("firstsecond", response.multikey)


    def test_form_data_file(self):
        """
        Test of parsing FormData file.
        Framework should create own File object and stored it.
        :return: Test result
        """

        test_data = '''Content-Disposition: form-data; name="file"; filename="download.html"
        \r\nContent-Type: text/html"\r\n\r\n<html>TEST</html>\r\n--BOUNDARY'''
        data_type = "multipart/form-data"
        response = get_content(test_data, data_type)
        self.assertEqual(response.file.__class__.__name__, "File")
