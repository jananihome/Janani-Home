from django.contrib import admin
from . models import Comment


class CommentAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'author',
        'helper',
        'app_name',
        'pub_date',
    )
admin.site.register(Comment, CommentAdmin)
