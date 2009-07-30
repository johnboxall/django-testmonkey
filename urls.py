from django.conf.urls.defaults import *
from django.conf import settings


urlpatterns = patterns("testmonkey.views",
    (r"^$", "test_list"),
    url(r"(?P<app_label>\w+)/$", "test_app", name="testmonkey_test_app"),
)
