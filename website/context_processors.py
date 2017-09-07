from website.forms import ContactForm
from django.core.urlresolvers import reverse


def contact_us_context_processor(request):
    return {
        'contact_form': ContactForm(),
        'contact_form_url': reverse("website:contact_us", args=(request.path))
    }