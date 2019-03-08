import requests



class test_url():
    '''Class that tests url endpoints to make sure the output is what's expected'''

    def __init__(self):
        self.url = 'http://127.0.0.1:80/'
        self.bad_lat = '123'
        self.bad_lon = '456'
        self.good_lat = '34.10'
        self.good_lon = '-117.68'
        self.no_data_text = "No data available\n"
        self.comma_error_text = "Got that comma problem!"
        self.string_to_float_exception_text = "There was an exception: could not convert string to float: "
        self.good_coords_string = '{"ASSAULT": 0, "MURDER": 0, "THEFT": 0, "RAPE": 0, "GTA": 0, "ROBBERY": 0, "OTHER": 1}'

    def assert_200(self, r):
        assert(r.status_code == 200)

    def test_empty(self):
        r = requests.get(self.url)
        txt = r.text
        self.assert_200(r)
        assert(txt == self.no_data_text)

    def test_no_comma(self):
        r = requests.get(self.url + self.bad_lat)
        self.assert_200(r)
        text = r.text
        assert(text == self.comma_error_text)

    def test_one_comma_bad_coords(self):
        r = requests.get(self.url + self.bad_lat + ',')
        self.assert_200(r)
        assert(r.text == self.string_to_float_exception_text)

    def test_one_comma_good_coords(self):
        r = requests.get(self.url + self.good_lat + ',' + self.good_lon)
        self.assert_200(r)
        assert(r.text == self.good_coords_string)

    def test_two_comma(self):
        r = requests.get(self.url + self.good_lon +',' + self.good_lat + ',')
        self.assert_200(r)
        assert(r.text == self.comma_error_text)

        r = requests.get(self.url + "," + self.good_lon + ',' + self.good_lat + ',')
        self.assert_200(r)

def run_tests():
    tester = test_url()
    print("Testing empty string")
    tester.test_empty()

    print("Testing string with no commas")
    tester.test_no_comma()

    print("Testing with 1 comma bad coordinates")
    tester.test_one_comma_bad_coords()

    print("Testing valid input")
    tester.test_one_comma_good_coords()

    print("Testing if two or more commas")
    tester.test_two_comma()


run_tests()
