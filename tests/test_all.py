import unittest
import requests
import json
import mock

# import sys
# sys.path.insert(0,'..')
from run import *


class SimpleResponse:
    data = """{"coord":{"lon":-122.42,"lat":37.77},"weather":[{"id":801,"main":"Clouds","description":"few clouds","icon":"02n"}],"base":"stations","main":{"temp":58.23,"feels_like":50.65,"temp_min":55,"temp_max":61,"pressure":1016,"humidity":82},"visibility":16093,"wind":{"speed":14.99,"deg":280},"clouds":{"all":20},"dt":1592201129,"sys":{"type":1,"id":5817,"country":"US","sunrise":1592138838,"sunset":1592191980},"timezone":-25200,"id":5391959,"name":"San Francisco","cod":200}
"""

    def json(self):
        return json.dumps(self.data)


class TestMisc(unittest.TestCase):
    def test_wind_direction(self):
        assert wind_direction(0) == "N"
        assert wind_direction(11) == "N"
        assert wind_direction(350) == "N"
        assert wind_direction(33) == "NNE"
        assert wind_direction(56) == "NE"
        assert wind_direction(78) == "ENE"
        assert wind_direction(101) == "E"
        assert wind_direction(123) == "ESE"
        assert wind_direction(146) == "SE"
        assert wind_direction(168) == "SSE"
        assert wind_direction(191) == "S"
        assert wind_direction(213) == "SSW"
        assert wind_direction(236) == "SW"
        assert wind_direction(258) == "WSW"
        assert wind_direction(281) == "W"
        assert wind_direction(303) == "WNW"
        assert wind_direction(326) == "NW"
        assert wind_direction(348) == "NNW"
        self.assertRaises(Exception, wind_direction, 361)

    def test_weather_obj(self):
        w = Weather()
        w.temp_cur = 0
        w.humid_cur = 0
        w.temp_feel = 0
        w.temp_min = 0
        w.temp_max = 0
        w.wind_speed = 0
        assert (
            str(w)
            == "temp_cur=0.0 humid_cur=0.0% temp_feel=0.0 temp_min=0.0 temp_max=0.0 wind_speed=0.0 wind_dir=None city=None country=None sunrise=None sunset=None summary=None description=None"
        )

    def test_parse_data(self):
        data1 = {
            "coord": {"lon": -122.42, "lat": 37.77},
            "weather": [
                {
                    "id": 801,
                    "main": "Clouds",
                    "description": "few clouds",
                    "icon": "02d",
                }
            ],
            "base": "stations",
            "main": {
                "temp": 71.91,
                "feels_like": 57.27,
                "temp_min": 64,
                "temp_max": 75.99,
                "pressure": 1013,
                "humidity": 43,
            },
            "visibility": 16093,
            "wind": {"speed": 25.28, "deg": 290},
            "clouds": {"all": 20},
            "dt": 1590366761,
            "sys": {
                "type": 1,
                "id": 5817,
                "country": "US",
                "sunrise": 1590324788,
                "sunset": 1590376822,
            },
            "timezone": -25200,
            "id": 5391959,
            "name": "San Francisco",
            "cod": 200,
        }
        assert parse_data(data1).summary == "Clouds"
        assert parse_data(data1).description == "few clouds"
        assert parse_data(data1).temp_cur == 71.91
        assert parse_data(data1).humid_cur == 43
        assert parse_data(data1).temp_feel == 57.27
        assert parse_data(data1).temp_min == 64
        assert parse_data(data1).temp_max == 75.99
        assert parse_data(data1).wind_speed == 25.28
        assert parse_data(data1).wind_dir == "WNW"
        assert parse_data(data1).city == "San_Francisco"
        assert parse_data(data1).country == "US"
        assert parse_data(data1).sunrise == "5:53AM"
        assert parse_data(data1).sunset == "8:20PM"
        data2 = {
            "coord": {"lon": -122.42, "lat": 37.77},
            "weather": [
                {
                    "id": 801,
                    "main": "Clouds",
                    "description": "few clouds",
                    "icon": "02d",
                }
            ],
            "base": "stations",
            "main": {
                "temp": 71.91,
                "feels_like": 57.27,
                "temp_min": 64,
                "temp_max": 75.99,
                "pressure": 1013,
                "humidity": 43,
            },
            "visibility": 16093,
            "wind": {"speed": 25.28},
            "clouds": {"all": 20},
            "dt": 1590366761,
            "sys": {
                "type": 1,
                "id": 5817,
                "country": "US",
                "sunrise": 1590324788,
                "sunset": 1590376822,
            },
            "timezone": -25200,
            "id": 5391959,
            "name": "San Francisco",
            "cod": 200,
        }
        assert parse_data(data2).wind_dir == "None"

    @mock.patch("requests.get")
    def test_get_data(self, requests_get_func):
        requests_get_func.return_value = SimpleResponse()
        assert "weather" in get_data("dummy_url")

    def test_build_url(self):
        location_id = "1234"
        api_key = "abc123"
        units = "imperial"
        assert (
            build_url(location_id, api_key, units)
            == "http://api.openweathermap.org/data/2.5/weather?id=1234&APPID=abc123&units=imperial"
        )


if __name__ == "__main__":
    unittest.main()
