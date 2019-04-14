from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import render

from announcements.models import Announcement
from comment.models import Comment
from educational_need.models import EducationalNeed
from events.models import Event


def superuser_required(view_func):
    def decorator(request):
        if not request.user.is_superuser:
            template = 'superadmin/you_shall_not_pass.html'
            return render(request, template)
        return view_func(request)
    return decorator


@login_required
@superuser_required
def dashboard(request):
    template = 'superadmin/dashboard.html'

    user_count = User.objects.count()
    volunteer_count = User.objects.filter(profile__is_volunteer=True).count()
    ngo_count = User.objects.filter(profile__is_organization=True).count()
    educational_need_count = EducationalNeed.objects.count()
    comment_count = Comment.objects.count()
    event_count = Event.objects.count()
    announcement_count = Announcement.objects.count()
    context = {
        'user_count': user_count,
        'volunteer_count': volunteer_count,
        'ngo_count': ngo_count,
        'educational_need_count': educational_need_count,
        'comment_count': comment_count,
        'event_count': event_count,
        'announcement_count': announcement_count,

    }
    return render(request, template, context)


@login_required
@superuser_required
def user_list(request):
    template = 'superadmin/user_list.html'

    all_users = User.objects.select_related('profile')

    limit = request.GET.get('limit', '10')
    try:
        paginator = Paginator(all_users, limit)
    except ValueError:
        paginator = Paginator(all_users, 10)
    except AssertionError:
        paginator = Paginator(all_users, 10)

    page = request.GET.get('page', '1')
    try:
        users = paginator.page(page)
    except PageNotAnInteger:
        users = paginator.page(1)
    except EmptyPage:
        users = paginator.page(paginator.num_pages)



    context = {
        'users': users,
    }

    return render(request, template, context)