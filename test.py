import unittest
import os
from postfix_conf import PostfixConf
from space_conf import SpaceConf

TEST_PATH = 'unit_test_test'

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
            self.assertEqual('smtpd_use_tls = yes', f.readline().strip())

    def test_sets_two_properties_files(self):
        with PostfixConf(TEST_PATH) as p:
            p['smtpd_use_tls'] = 'yes' 
            p['myhostname'] = 'example.com' 
        with open(TEST_PATH, 'r') as f:
            self.assertEqual('smtpd_use_tls = yes', f.readline().strip())
            self.assertEqual('myhostname = example.com', f.readline().strip())

    def test_sets_properties_existing_file(self):
        with open(TEST_PATH, 'w') as f:
            f.write("test_val = hello\n")

        with PostfixConf(TEST_PATH) as p:
            p['smtpd_use_tls'] = 'yes' 
            p['myhostname'] = 'example.com' 
            self.assertEqual('hello', p['test_val'])

        with open(TEST_PATH, 'r') as f:
            self.assertEqual('test_val = hello', f.readline().strip())
            self.assertEqual('smtpd_use_tls = yes', f.readline().strip())
            self.assertEqual('myhostname = example.com', f.readline().strip())

    def setUp(self):
        remove_file(TEST_PATH)

    def tearDown(self):
        remove_file(TEST_PATH)

class TestSpace(unittest.TestCase):
    def test_creates_file(self):
        with SpaceConf(TEST_PATH) as p:
            pass
        self.assertTrue(os.path.exists(TEST_PATH))

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
        with SpaceConf(TEST_PATH, **test_d) as f:
            pass
        with open(TEST_PATH, 'r') as f:
            self.assertEqual("dave\tdave@antunovic.nz\ndot\tdot@antunovic.nz", f.read().strip()) 

    def setUp(self):
        remove_file(TEST_PATH)

    def tearDown(self):
        remove_file(TEST_PATH)

if __name__ == '__main__':
    unittest.main()
