from django.conf.urls import url
from django.contrib import admin

from app.views import boarding_list, in_the_house_view, load_sample_data_view

admin.autodiscover()

urlpatterns = [
    url(r'^$', boarding_list, name='boarding-list'),
    url(r'^in-the-house/$', in_the_house_view, name='in-the-house'),
    url(r'^load/load_sample_data/$', load_sample_data_view, name='load_sample_data_view'),
]
