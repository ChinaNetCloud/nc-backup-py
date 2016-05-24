import unittest
import sys


from collections import OrderedDict


#add path to home of the whole project.
import config_test
from configs.load_json_configs import LoadJsonConfig


class configsJsonTestCase (unittest.TestCase):
    """JSON Load test case"""
    # check if it can find json file.
    def test_load_json_good_to_dictionary(self):
        """This test loads a GOOD json config file 'data/json/conf_ok.json'"""
        self.assertIsInstance(LoadJsonConfig.read_config_file(LoadJsonConfig(),'data/json/conf_ok.json'),OrderedDict)

    # Empty file path
    def test_epty_file_path_to_json(self):
        self.assertIsInstance(LoadJsonConfig.read_config_file(LoadJsonConfig(), ''), OrderedDict)

    # what happens if the file is not existing
    def test_readable_error_if_file_not_found(self):
        """Test file not found message"""
        fake_path = 'this/path/is/not/real'
        self.assertEqual(LoadJsonConfig.read_config_file(LoadJsonConfig(), fake_path), 'File not found at ' + fake_path)

    # Test if it loads a dictionary or not.
    def test_load_json_to_dic(self):
        self.assertEqual(type(LoadJsonConfig.read_config_file(LoadJsonConfig(), 'data/json/conf_ok.json')), OrderedDict)



