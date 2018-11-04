from django.core.mail import EmailMessage
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.sites.shortcuts import get_current_site
from django.http import Http404
from django.shortcuts import render,get_object_or_404 , redirect
from django.template.loader import render_to_string
from django.utils import timezone
from django.views.generic.list import ListView

from educational_need.models import EducationalNeed
from .forms import CommentForm
from .models import Comment

class CommentListView(ListView):
    model = Comment
    template_name = 'comment/comment_list.html'
    paginate_by = 4

    def get_queryset(self):
        return Comment.objects.filter(published=True).order_by('-pk')


@login_required
def educational_need_comment(request, pk):
    educational_need = get_object_or_404(EducationalNeed, pk=pk)
    if educational_need.closed:
        raise Http404("This need has been closed!")
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
            educational_need.is_active = False
            educational_need.save()
            # Send email to admin
            current_site = get_current_site(request)
            subject = 'New educational need comment on Janani Care.'
            message = render_to_string('comment/approval_email.html', {
                'domain': current_site.domain,
                'educational_need': educational_need,
                'comment': comment,
            })
            toemails = [obj.email for obj in User.objects.filter(is_staff=True)]
            email = EmailMessage(subject, message, to=toemails)
            email.send()
            return redirect('comment_submitted')
    else:
        form = CommentForm()
    template = 'comment/comment_form.html'
    context = {'form': form, 'educational_need': educational_need}
    return render(request, template, context)


@login_required
def comment_submitted(request):
    template = 'comment/comment_submitted.html'
    return render(request, template)


@user_passes_test(lambda u: u.is_superuser)
def comment_approval(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    template = 'comment/comment_approval.html'
    context = {'comment': comment}
    return render(request, template, context)


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
