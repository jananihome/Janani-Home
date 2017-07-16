from django.shortcuts import render,get_object_or_404 , redirect
from .models import Comment
from django.contrib.auth.decorators import login_required

def comment_list(request):
    comments = Comment.objects.all()
    return render(request, 'comment_list.html' , {'comments': comments,})

@login_required
def activate(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    comment.published = True
    comment.save()
    return redirect('comment_list')
