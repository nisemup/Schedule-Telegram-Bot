from rest_framework import serializers
from . import models


class GroupSerializer(serializers.ModelSerializer):
    gid = serializers.CharField(required=False, max_length=20)
    faculty = serializers.CharField(required=False, max_length=10)
    gnum = serializers.IntegerField(required=False)

    class Meta:
        model = models.Groups
        fields = '__all__'


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Profiles
        fields = '__all__'


class ScheduleSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Schedule
        fields = '__all__'
