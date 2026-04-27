# -- coding: utf-8 --
from rest_framework.decorators import action
from rest_framework.response import Response

from apps.alerts.common.source_adapter.base import AlertSourceAdapterFactory
from apps.alerts.filters import AlertSourceModelFilter
from apps.alerts.models.alert_source import AlertSource
from apps.alerts.serializers import AlertSourceModelSerializer
from config.drf.pagination import CustomPageNumberPagination
from config.drf.viewsets import ModelViewSet


class AlertSourceModelViewSet(ModelViewSet):
    """
    告警源
    """
    queryset = AlertSource.objects.all()
    serializer_class = AlertSourceModelSerializer
    ordering_fields = ["id"]
    ordering = ["id"]
    filterset_class = AlertSourceModelFilter
    pagination_class = CustomPageNumberPagination

    @action(detail=True, methods=["get"], url_path="integration-guide")
    def integration_guide(self, request, pk=None):
        alert_source = self.get_object()
        adapter_class = AlertSourceAdapterFactory.get_adapter(alert_source)
        adapter = adapter_class(alert_source=alert_source)
        base_url = request.build_absolute_uri("/").rstrip("/")
        return Response(adapter.get_integration_guide(base_url))
