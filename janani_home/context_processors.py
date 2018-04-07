from django.conf import settings


def config_processor(request):
    config = {
       'GOOGLE_ANALYTICS_ID': settings.GOOGLE_ANALYTICS_ID,
       'GOOGLE_SITE_VERIFICATION': settings.GOOGLE_SITE_VERIFICATION,
       'PHONE_NUMBER': settings.PHONE_NUMBER,
    }
    return {'config': config}
