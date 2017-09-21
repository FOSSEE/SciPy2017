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
    url(r'^', include('social.apps.django_app.urls', namespace='social')),
    url(r'^', include('django.contrib.auth.urls', namespace='auth')),

    url(r'^forgotpassword/$', password_reset, {'template_name': 'register/password_reset_form.html'}, name="password_reset"),
    url(r'^password_reset/(?P<uidb64>[0-9A-Za-z]+)-(?P<token>.+)/$',
        password_reset_confirm, {'template_name': 'register/password_reset_confirm.html'}, name='password_reset_confirm'),
    url(r'^password_reset/mail_sent/$', password_reset_done, {'template_name': 'register/password_reset_done.html'},
        name='password_reset_done'),
    url(r'^password_reset/complete/$', password_reset_complete, {'template_name': 'register/password_reset_complete.html'},
        name='password_reset_complete'),
    url(r'^changepassword/$', password_change, {'template_name': 'register/password_change_form.html'},
        name='password_change'),
    url(r'^password_change/done/$', password_change_done, {'template_name': 'register/password_change_done.html'},
        name='password_change_done'),
)
