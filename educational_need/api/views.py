from educational_need.models import EducationalNeed
from rest_framework import viewsets

from .serializers import EducationalNeedSerializer

class EducationalNeedViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows educational needs to be viewed or edited.
    """
    queryset = EducationalNeed.objects.all().order_by('-pub_date')
    serializer_class = EducationalNeedSerializer
