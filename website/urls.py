from django.conf.urls import patterns, include, url
from django.conf.urls.static import static
from django.conf import settings



urlpatterns = patterns('',
    url(r'^$', 'website.views.home', name='home'),
    # url(r'^contact/$', 'website.views.contact_us', name='contact'),
    url(r'^cfp/$', 'website.views.cfp', name='cfp'),
    url(r'^submit-cfp/$', 'website.views.submitcfp', name='submitcfp'),
    url(r'^submit-cfw/$', 'website.views.submitcfw', name='submitcfw'),
    #url(r'^submit-cfp/$', 'website.views.cfp', name='home'),
    #url(r'^submit-cfw/$', 'website.views.home', name='home'),
    url(r'^accounts/register/$', 'website.views.userregister', name='userregister'),
    #url(r'^accounts/login/$', 'website.views.cfp', name='cfp'),
    url(r'^gallery/$', 'website.views.gallery', name='gallery'),
    # url(r'^view-abstracts/$', 'website.views.view_abstracts', name='view_abstracts'),
    url(r'^view-abstracts/$', 'website.views.view_abstracts', name='view_abstracts'),
    url(r'^abstract-details/(?P<proposal_id>\d+)$', 'website.views.abstract_details', name='abstract_details'),
    url(r'^edit-proposal/(?P<proposal_id>\d+)$', 'website.views.edit_proposal', name='edit_proposal'),
    url(r'^view-abstracts/status_change/$', 'website.views.status_change', name='status_change'),
    url(r'^comment-abstract/(?P<proposal_id>\d+)$', 'website.views.comment_abstract', name='comment_abstract'),
    url(r'^comment-abstract/status/(?P<proposal_id>\d+)$', 'website.views.status', name='status'),
    url(r'^comment-abstract/rate/(?P<proposal_id>\d+)$', 'website.views.rate_proposal', name='rate_proposal'),
    url(r'^process-contact-form/(?P<next_url>\d+)', 'website.views.contact_us', name='contact_us'),
    # url(r'^view-abstracts/download_csv/$','website.views.download_csv', name='download_csv')
    )+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

