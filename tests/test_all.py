import unittest

#import sys
#sys.path.insert(0,'..')
from run import *

class TestMisc(unittest.TestCase):

    def test_wind_direction(self):
        assert wind_direction(0) == "N"

if __name__ == '__main__':
    unittest.main()
