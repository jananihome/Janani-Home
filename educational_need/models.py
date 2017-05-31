from django.db import models


class EducationalNeed(models.Model):
    user = models.ForeignKey('auth.User')  # Need to replace with our custom user
    title = models.CharField(max_length=200)
    permanent_address = models.TextField()
    current_address = models.TextField()
    college_school_address = models.TextField(blank=True, null=True)
    college_school_contact_details = models.TextField(blank=True, null=True)
    view_count = models.IntegerField(default=0)
    status = models.CharField(max_length=200)
    amount_required = models.IntegerField(default=0)
    documents = models.TextField()
    requirement_description = models.TextField()
    communication_mode = models.CharField(max_length=200)

    def _str_(self):
        return self.title
