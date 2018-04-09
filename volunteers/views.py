from django.shortcuts import render
from django.views.generic.list import ListView

from accounts.models import Profile


class VolunteerList(ListView):
    model = Profile
    template_name = 'volunteers/volunteer_list.html'
    paginate_by = 4

    def get_queryset(self):
        return Profile.objects.filter(approved_volunteer=True).order_by('-pk')
