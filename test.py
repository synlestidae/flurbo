import unittest
import os
from postfix_conf import PostfixConf
from space_conf import SpaceConf

TEST_PATH = 'unit_test_test.cf'
TEST_PATH_SP = 'unit_test_test'

def remove_file(path):
    if os.path.exists(TEST_PATH): 
        os.unlink(TEST_PATH)


class TestPostfix(unittest.TestCase):
    def test_creates_file(self):
        with PostfixConf(TEST_PATH) as p:
            pass
        self.assertTrue(os.path.exists(TEST_PATH))

    def test_sets_property_file(self):
        with PostfixConf(TEST_PATH) as p:
            p['smtpd_use_tls'] = 'yes' 
        with open(TEST_PATH, 'r') as f:
            self.assertEqual('smtpd_use_tls = yes', f.readline())

    def test_sets_two_properties_files(self):
        with PostfixConf(TEST_PATH) as p:
            p['smtpd_use_tls'] = 'yes' 
            p['myhostname'] = 'example.com' 
        with open(TEST_PATH, 'r') as f:
            self.assertEqual('smtpd_use_tls = yes', f.readline())
            self.assertEqual('myhostname = example.com', f.readline())

    def setUp(self):
        remove_file(TEST_PATH)

    def tearDown(self):
        remove_file(TEST_PATH)

class TestSpace(unittest.TestCase):
    def test_creates_file(self):
        with SpaceConf(TEST_PATH_SP) as p:
            pass
        self.assertTrue(os.path.exists(TEST_PATH_SP))

    def test_sets_property_file(self):
        with SpaceConf(TEST_PATH) as p:
            p['mate'] = 'mate@antunovic.nz' 
        with open(TEST_PATH, 'r') as f:
            self.assertEqual("mate\tmate@antunovic.nz", f.readline().strip())

    def test_sets_dict_file(self):
        test_d = {
            'dave': 'dave@antunovic.nz',
            'dot': 'dot@antunovic.nz',
        }
        with SpaceConf(TEST_PATH_SP, **test_d) as f:
            pass
        with open(TEST_PATH_SP, 'r') as f:
            self.assertEqual("dave\tdave@antunovic.nz\ndot\tdot@antunovic.nz", f.read().strip()) 

    def setUp(self):
        remove_file(TEST_PATH_SP)

    def tearDown(self):
        remove_file(TEST_PATH_SP)

if __name__ == '__main__':
    unittest.main()
