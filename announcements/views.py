from django.shortcuts import render
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView

from .models import Announcement

def announcement_list(request):
    announcements = Announcement.objects.filter(published=True).order_by('-pub_date')
    return render(
        request,
        'announcements/announcement_list.html',
        {'announcements': announcements}
    )


class AnnouncementDetail(DetailView):
    model = Announcement
    template_name = 'announcements/announcement_detail.html'
