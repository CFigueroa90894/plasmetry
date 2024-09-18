import unittest

"""Applicable for all probes."""
class BaseCase(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def setUp(self):
        if not self.parameters:
            raise ValueError("Test parameters must be set before running tests.")