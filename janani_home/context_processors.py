from django.conf import settings


def config_processor(request):
    config = {
       'GOOGLE_ANALYTICS_ID': settings.GOOGLE_ANALYTICS_ID,
    }
    return {'config': config}
