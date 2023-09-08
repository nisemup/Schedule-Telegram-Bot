from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import permissions, viewsets

from . import models
from . import serializers


class GroupViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.GroupSerializer
    permission_classes = [permissions.IsAdminUser]

    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['faculty', 'gnum']

    def get_queryset(self):
        queryset = models.Groups.objects.all()
        distinct = self.request.query_params.get('distinct')
        if distinct:
            queryset = models.Groups.objects.order_by().values(distinct).distinct()
        return queryset


class ProfileViewSet(viewsets.ModelViewSet):
    queryset = models.Profiles.objects.all()
    serializer_class = serializers.ProfileSerializer
    permission_classes = [permissions.IsAdminUser]


class ScheduleViewSet(viewsets.ModelViewSet):
    queryset = models.Schedule.objects.all()
    serializer_class = serializers.ScheduleSerializer
    permission_classes = [permissions.IsAdminUser]
