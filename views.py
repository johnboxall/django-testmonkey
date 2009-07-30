import simplejson

from django.db.models import get_apps
from django.http import HttpResponse
from django.shortcuts import render_to_response

from testmonkey.helpers import run_tests, AppTests


def test_app(request, app_label):
    result = run_tests(test_labels=[app_label], verbosity=0, interactive=False)
    # @@@ if result.wasSuccessful
    serializable = [(unicode(func), trace) for func, trace in result.failures]
    json = simplejson.dumps(serializable)
    return HttpResponse(json)

def test_list(request, template="testmonkey/test_list.html", ctx=None):
    app_tests = [AppTests(app_module) for app_module in get_apps()]
    ctx = {
        "app_tests": app_tests
    }
    return render_to_response(template, ctx) #request, ctx)




        




