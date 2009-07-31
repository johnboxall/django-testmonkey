import simplejson

from django.db.models import get_apps
from django.http import HttpResponse
from django.shortcuts import render_to_response

from testmonkey.helpers import run_tests, AppTests
from testmonkey.json import TestJSONEncoder


def test_app(request, test_label):
    result = run_tests(test_labels=[test_label], verbosity=1, interactive=False)
    json = simplejson.dumps(result, cls=TestJSONEncoder)
    return HttpResponse(json, mimetype="application/json")

def test_list(request, template="testmonkey/test_list.html", ctx=None):
    app_tests = [AppTests(app_module) for app_module in get_apps()]
    ctx = {
        "app_tests": app_tests
    }
    return render_to_response(template, ctx) #request, ctx)




        
