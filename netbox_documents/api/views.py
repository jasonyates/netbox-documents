from netbox.api.viewsets import NetBoxModelViewSet

from .. import models
from .serializers import SiteDocumentSerializer, DeviceDocumentSerializer, CircuitDocumentSerializer

class SiteDocumentViewSet(NetBoxModelViewSet):
    queryset = models.SiteDocument.objects.prefetch_related('tags')
    serializer_class = SiteDocumentSerializer

class DeviceDocumentViewSet(NetBoxModelViewSet):
    queryset = models.DeviceDocument.objects.prefetch_related('tags')
    serializer_class = DeviceDocumentSerializer

class CircuitDocumentViewSet(NetBoxModelViewSet):
    queryset = models.CircuitDocument.objects.prefetch_related('tags')
    serializer_class = CircuitDocumentSerializer