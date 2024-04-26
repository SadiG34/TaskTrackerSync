from rest_framework import serializers
from .models import *

class ResultSerializer(serializers.ModelSerializer):
    class Meta:
        model = TaskYougile
        fields = '__all__'


    # title = serializers.CharField(max_length=255, null=True)
    # timestamp = serializers.DateTimeField(null=True)
    # columnId = serializers.IntegerField(null=True)
    # description = serializers.TextField(null=True)
    # archived = serializers.BooleanField(null=True)
    # completed = serializers.BooleanField(null=True)
    # createdBy = serializers.IntegerField(null=True)
    # stickers = serializers.JSONField(null=True)
    # assigned = serializers.IntegerField(null=True)
    # stopwatch = serializers.JSONField(null=True)
    # timeTracking = serializers.JSONField(null=True)