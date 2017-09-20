from django.conf.urls import patterns, include, url

from django.contrib import admin
from django.contrib.auth.views import password_reset, password_reset_confirm,\
        password_reset_done, password_reset_complete, password_change,\
        password_change_done
admin.autodiscover()

urlpatterns = patterns('',
    
    url(r'^admin/', include(admin.site.urls)),
    url(r'^', include('website.urls', namespace='website')),
    url(r'^2017/', include('website.urls', namespace='website')),
    url(r'^2017/', include('website.urls_password_reset')),
    url(r'^', include('social.apps.django_app.urls', namespace='social')),
    url(r'^', include('django.contrib.auth.urls', namespace='auth'))
)
