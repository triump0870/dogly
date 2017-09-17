from django.views.generic import TemplateView
from django.conf.urls import include, url

from django.contrib import admin
from django.conf import settings


admin.autodiscover()

urlpatterns = [
    url(r'^', include('app.urls', namespace='app')),
    # Uncomment the admin/doc line below and add 'django.contrib.admindocs'
    # to INSTALLED_APPS to enable admin documentation:
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
]

if settings.DEBUG:
    import debug_toolbar
    urlpatterns += [
        url(r'^__debug__/', include(debug_toolbar.urls)),
    ]
