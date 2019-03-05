import requests



class test_url():
    '''Class that tests url endpoints to make sure the output is what's expected'''

    def __init__(self):
        self.url = 'http://127.0.0.1:5000/'
        self.bad_lat = '123'
        self.bad_lon = '456'
        self.good_lat = '34.10'
        self.good_lon = '-117.68'

    def test_empty(self):
        r = requests.get(self.url)
        txt = r.text

        assert(txt == "No data available\n")

    def test_no_comma(self):
        r = requests.get(self.url + self.bad_lat)
        text = r.text
        assert(text == "Got that comma problem!")

    def test_one_comma_bad_coords(self):
        r = requests.get(self.url + self.bad_lat + ',')
        assert(r.text == "There was an exception: could not convert string to float: ")

    def test_one_comma_good_coords(self):
        r = requests.get(self.url + self.good_lat + ',' + self.good_lon)
        assert(r.text == '{"ASSAULT": 0, "MURDER": 0, "THEFT": 0, "RAPE": 0, "GTA": 0, "ROBBERY": 0, "OTHER": 1}')

    def test_two_comma(self):
        r = requests.get(self.url + self.good_lon +',' + self.good_lat + ',')
        assert(r.text == "Got that comma problem!")


def run_tests():
    tester = test_url()
    tester.test_empty()
    tester.test_no_comma()
    tester.test_one_comma_bad_coords()
    tester.test_one_comma_good_coords()
    tester.test_two_comma()


run_tests()