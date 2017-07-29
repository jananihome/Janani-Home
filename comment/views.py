from django.core.mail import EmailMessage
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.sites.shortcuts import get_current_site
from django.shortcuts import render,get_object_or_404 , redirect
from django.template.loader import render_to_string
from django.utils import timezone

from educational_need.models import EducationalNeed
from .forms import CommentForm
from .models import Comment


def educational_need_comment(request, pk):
    educational_need = get_object_or_404(EducationalNeed, pk=pk)
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            # Save comment
            comment = form.save(commit=False)
            comment.author = request.user
            comment.educational_need = educational_need
            comment.app_name = 'Educational Need'
            comment.save()
            # Update educational need
            educational_need.closed = True
            educational_need.save()
            # Update user profile
            educational_need.user.profile.active_educational_need = None
            educational_need.user.profile.save()
            # Send email to admin
            current_site = get_current_site(request)
            subject = 'New educational need comment on Janani Care.'
            message = render_to_string('comment/approval_email.html', {
                'domain': current_site.domain,
                'educational_need': educational_need,
                'comment': comment,
            })
            toemail = 'lorencmaciek@gmail.com'
            email = EmailMessage(subject, message, to=[toemail])
            email.send()
            return redirect('comment_submitted')
    else:
        form = CommentForm()
    return render(request, 'comment/comment_form.html', {'form': form, 'educational_need': educational_need})


def comment_submitted(request):
    return render(request, 'comment/comment_submitted.html')


def comment_list(request):
    comments = Comment.objects.all()
    return render(request, 'comment/comment_list.html' , {'comments': comments,})


@user_passes_test(lambda u: u.is_superuser)
def comment_approve(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    return render(request, 'comment/comment_approve.html' , {'comment': comment,})


@user_passes_test(lambda u: u.is_superuser)
def approve_comment(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    comment.published = True
    comment.rejected = False
    comment.save()
    return redirect('comment_list')


@user_passes_test(lambda u: u.is_superuser)
def reject_comment(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    comment.published = False
    comment.rejected = True
    comment.rejected_reason = 'Rejected by {} on {}.'.format(request.user, timezone.now())
    comment.save()
    return redirect('comment_list')
