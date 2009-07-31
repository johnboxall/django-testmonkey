from unittest import TestCase, TestResult
from django.utils import simplejson
from testmonkey.helpers import Test

class TestJSONEncoder(simplejson.JSONEncoder):
    def default(self, o):
        if issubclass(o.__class__, TestResult):
            return o.failures + o.errors
        if issubclass(o.__class__, TestCase):
            return Test(o).label
        else:
            return super(TestJSONEncoder, self).default(o)