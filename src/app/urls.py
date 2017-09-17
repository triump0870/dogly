from django.conf.urls import url
from django.contrib import admin

from app.views import calendar_view, boarding_feed, BoardingView, in_the_house_view

admin.autodiscover()

urlpatterns = [
    # url(r'^$', calendar, name='cal'),
    url(r'^(?P<pk>\d+)/$', BoardingView.as_view(), name='boarding-detail'),
    url(r'^', calendar_view, name='boarding-list'),
    url(r'^feed/', boarding_feed, name='boarding-feed'),
    url(r'^in-the-house/', in_the_house_view, name='in-the-house'),
]
