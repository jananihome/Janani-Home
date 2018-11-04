from django.contrib.sitemaps import Sitemap
from django.urls import reverse

from accounts.models import Profile
from cms.models import Page
from educational_need.models import EducationalNeed


class StaticViewSitemap(Sitemap):
    priority = 0.5
    changefreq = 'daily'

    def items(self):
        return [
            'list_view',
            'signup',
            'login',
            'comment_list',
            'volunteer_list',
        ]

    def location(self, item):
        return reverse(item)


class CmsSitemap(Sitemap):
    changefreq = 'weekly'
    priority = 0.5

    def items(self):
        return Page.objects.filter(noindex=False)

    def lastmod(self, obj):
        return obj.pub_date


class EducationalNeedSitemap(Sitemap):
    changefreq = 'weekly'
    priority = 0.5

    def items(self):
        return EducationalNeed.objects.filter(is_active=True)

    def lastmod(self, obj):
        return obj.pub_date
