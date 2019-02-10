from django.contrib.auth.models import User
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from displacement_detector_api.image_processing.position_change import calculate_position_change
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

    def list(self, request, *args, **kwargs):
        response = super(AnalysisImageViewSet, self).list(request, *args, **kwargs)

        # redefine response.data to include original query params
        response.data = {
            'distribution': calculate_position_change(),
            'data': response.data
        }

        return response
