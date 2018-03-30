from django.shortcuts import render
from accounts.models import Profile


def volunteer_list(request):
    volunteers = Profile.objects.filter(approved_volunteer=True).order_by('-pk')
    return render(
        request,
        'volunteers/volunteer_list.html',
        {'volunteers': volunteers}
    )
