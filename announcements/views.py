from django.shortcuts import render

from .models import Announcement

def announcement_list(request):
    announcements = Announcement.objects.filter(published=True).order_by('-pub_date')
    return render(
        request,
        'announcements/announcement_list.html',
        {'announcements': announcements}
    )
