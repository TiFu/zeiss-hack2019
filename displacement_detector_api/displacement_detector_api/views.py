from django.contrib.auth.models import User
from rest_framework import viewsets

from displacement_detector_api.models import EvaluationResult, AnalysisImage
from displacement_detector_api.serializers import UserSerializer, EvaluationResultSerializer, AnalysisImageSerializer


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class EvaluationResultViewSet(viewsets.ModelViewSet):
    queryset = EvaluationResult.objects.all()
    serializer_class = EvaluationResultSerializer

class AnalysisImageViewSet(viewsets.ModelViewSet):
    queryset = AnalysisImage.objects.all()
    serializer_class = AnalysisImageSerializer
