import unittest

from configs.load_json_configs import LoadJsonConfig

class configsJsonTestCase (unittest.TestCase):
    """JSON Load test case"""
    def test_load_json_good_to_dictionary(self):
        """This test loads a GOOD json config file 'data/json/conf_ok.json'"""
        self.assertIsInstance(LoadJsonConfig.read_config_file(LoadJsonConfig(),'data/json/conf_ok.json'),dict)

    def test_readable_error_if_file_not_found(self):
        """Test file not found message"""
        fake_path = 'this/path/is/not/real'
        self.assertEqual(LoadJsonConfig.read_config_file(LoadJsonConfig(), fake_path), 'File not found at ' + fake_path)

