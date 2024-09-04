import unittest

"""SLP, DLP, HEA and IEA applicable"""
class BaseCase(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.parameters = {
            'Raw current': None,
            'Bias': None,
        }
        self.parameters_set = None

    def setUp(self):
        if not self.parameters_set:
            raise ValueError("Test parameters must be set before running tests.")
            
    def set_parameters(self, raw_current, bias):
        """Function to set parameters for the test case"""
        if not self.parameters_set:
            self.parameters['Raw current'] = raw_current
            self.parameters['Bias'] = bias
            self.parameters_set = True
    
        