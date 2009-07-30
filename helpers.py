import unittest

from django.conf import settings
from django.db.models import get_app, get_apps
from django.test.simple import build_suite, reorder_suite
from django.test.testcases import TestCase
from django.test.utils import setup_test_environment, teardown_test_environment
from django.utils.encoding import StrAndUnicode


class AppTests(StrAndUnicode):
    def __init__(self, app_module):
        self.module = app_module
        
    def __unicode__(self):
        return self.module.__name__.rsplit(".", 2)[-2]
        
    def get_tests(self):
        # @@@ Doctests? - `runTest`
        if not hasattr(self, "_tests"):
            self._suite = unittest.TestSuite()
            self._suite.addTest(build_suite(self.module))
            self._suite = reorder_suite(self._suite, (TestCase,))
            self._tests = [Test(test) for test in self._suite._tests]
        return self._tests
            
    def __iter__(self):
        return iter(self.get_tests())
    

class Test(StrAndUnicode):
    """Wrapper around a TestCase to let us access properties in template."""
    def __init__(self, test):
        self.name = test._testMethodName
        self.doc = test._testMethodDoc or ""
    
    def __unicode__(self):
        return self.name
        
        
def run_tests(test_labels, verbosity=1, interactive=True, extra_tests=[]):
    # Same as django.test.simple.run_tests but return the result object.
    # http://code.djangoproject.com/browser/django/trunk/django/test/simple.py#L149
    setup_test_environment()

    settings.DEBUG = False
    suite = unittest.TestSuite()

    if test_labels:
        for label in test_labels:
            if '.' in label:
                suite.addTest(build_test(label))
            else:
                app = get_app(label)
                suite.addTest(build_suite(app))
    else:
        for app in get_apps():
            suite.addTest(build_suite(app))

    for test in extra_tests:
        suite.addTest(test)

    suite = reorder_suite(suite, (TestCase,))

    old_name = settings.DATABASE_NAME
    from django.db import connection
    connection.creation.create_test_db(verbosity, autoclobber=not interactive)
    result = unittest.TextTestRunner(verbosity=verbosity).run(suite)
    connection.creation.destroy_test_db(old_name, verbosity)

    teardown_test_environment()

    return result