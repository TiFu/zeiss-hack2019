from django.contrib.auth.models import User
from rest_framework import serializers

from displacement_detector_api.image_processing.position_change import calculate_position_change
from displacement_detector_api.models import EvaluationResult, AnalysisImage


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('url', 'username', 'email', 'groups')


class EvaluationResultSerializer(serializers.ModelSerializer):
    class Meta:
        model = EvaluationResult
        fields = ('all_positions',)




class AnalysisImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = AnalysisImage
        exclude = []


