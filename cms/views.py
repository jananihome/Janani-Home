from django.views import generic

from .models import Page


class PageView(generic.DetailView):
    model = Page
    template_name = 'cms/page.html'
