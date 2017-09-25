from django.conf.urls import url
from django.contrib import admin

from app.views import calendar, boardings, load_sample_data_view

admin.autodiscover()

urlpatterns = [
    url(r'^$', calendar, name='calendar'),
    url(r'^boardings/$', boardings, name='boardings'),
    url(r'^load-sample-data/$', load_sample_data_view, name='load-sample-data'),
]
