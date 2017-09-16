from django.conf.urls import url
from django.contrib import admin

from app.views import calendar, boarding_feed, BoardingView

admin.autodiscover()

urlpatterns = [
    # url(r'^$', calendar, name='cal'),
    url(r'^(?P<pk>\d+)/$', BoardingView.as_view(), name='boarding-detail'),
    url(r'^$', calendar, name='boarding-list'),
    url(r'^feed/', boarding_feed, name='boarding-feed'),

]
