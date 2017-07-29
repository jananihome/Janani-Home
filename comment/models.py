from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class Comment(models.Model):
    author = models.ForeignKey('auth.User', related_name='author')
    helper = models.ForeignKey(
        User,
        limit_choices_to={'is_staff': False},
        related_name='helper',
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    app_name = models.CharField(max_length=200, blank=True)
    comment= models.TextField()
    published = models.BooleanField(default=False)
    pub_date = models.DateField(default=timezone.now)
    rejected = models.BooleanField(default=False)
    rejected_reason = models.CharField(max_length=200, blank=True, null=True)
    educational_need = models.ForeignKey(
        'educational_need.EducationalNeed',
        on_delete=models.SET_NULL,
        blank=True,
        null=True
    )

    # Define choices for rating field
    VERY_BAD = 0
    BAD = 1
    AVERAGE = 2
    GOOD = 3
    VERY_GOOD = 4
    EXCELENT = 5

    RATING_CHOICES = (
        (VERY_BAD, 'Very bad'),
        (BAD, 'Bad'),
        (AVERAGE, 'Average'),
        (GOOD, 'Good'),
        (VERY_GOOD, 'Very good'),
        (EXCELENT, 'Excelent'),
    )

    rating = models.IntegerField(
        choices=RATING_CHOICES,
        default=3,
    )

    def __str__(self):
        return 'Comment {} ({} on {})'.format(str(self.pk), self.author.username, str(self.pub_date))
