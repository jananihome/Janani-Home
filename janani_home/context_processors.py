from django.conf import settings


def config_processor(request):
    config = {
       'GOOGLE_ANALYTICS_ID': settings.GOOGLE_ANALYTICS_ID,
       'GOOGLE_SITE_VERIFICATION': settings.GOOGLE_SITE_VERIFICATION,
    }
    return {'config': config}
