import unittest
from unittest import TestResult# as DefaultTestResult
from django.core.cache import cache

"""
Build a progress report by storing test state in memcache.

"""
class TestProgress(object):
    running_key = "test:is_running"
    progress_key = "test:progress"

    def is_running(test_label):
        return bool(cache.get(running_key))
    
    def start(test_label):
        cache.set(running_key, test_label)
        
    def stop(test_label):
        cache.delete(running_key)
        
    def get_progress(): #test_label):
        return cache.get(progress_key)
        
    def set_progress(test_result):
        return cache.set(test_result, progress_key)


progress = TestProgress()



old_startTest = unittest.TestResult.startTest
old_addError = unittest.TestResult.addError
old_addFailure = unittest.TestResult.addFailure
old_addSuccess = unittest.TestResult.addSuccess

# class TestProgressResult(DefaultTestResult):
def startTest(self, test):
    print 'startTest: %s' % test
    old_startTest(self, test)
    # super(TestProgressResult, self).startTest(test)

def addError(self, test, err):
    print 'addError: %s' % test
    old_addError(self, test, err)
    # super(TestProgressResult, self).addError(test, err)
    
def addFailure(self, test, err):
    print 'addFailure: %s' % test
    old_addFailure(self, test, err)
    # super(TestProgressResult, self).addFailure(test, err)
    
def addSuccess(self, test):
    print 'addFailure: %s' % test
    old_addSuccess(self, test)
    # super(TestProgressResult, self).addSuccess(test, err)

# unittest.TestResult = TestProgressResult
unittest.TestResult.startTest = startTest
unittest.TestResult.addError = addError
unittest.TestResult.addFailure = addFailure
unittest.TestResult.addSuccess = addSuccess