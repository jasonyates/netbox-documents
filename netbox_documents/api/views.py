from netbox.api.viewsets import NetBoxModelViewSet

from .. import models, filtersets
from .serializers import SiteDocumentSerializer, LocationDocumentSerializer, DeviceDocumentSerializer, DeviceTypeDocumentSerializer, CircuitDocumentSerializer, VMDocumentSerializer, CircuitProviderDocumentSerializer

class SiteDocumentViewSet(NetBoxModelViewSet):
    queryset = models.SiteDocument.objects.prefetch_related('tags')
    serializer_class = SiteDocumentSerializer
    filterset_class = filtersets.SiteDocumentFilterSet

class LocationDocumentViewSet(NetBoxModelViewSet):
    queryset = models.LocationDocument.objects.prefetch_related('tags')
    serializer_class = LocationDocumentSerializer
    filterset_class = filtersets.LocationDocumentFilterSet

class DeviceDocumentViewSet(NetBoxModelViewSet):
    queryset = models.DeviceDocument.objects.prefetch_related('tags')
    serializer_class = DeviceDocumentSerializer
    filterset_class = filtersets.DeviceDocumentFilterSet

class DeviceTypeDocumentViewSet(NetBoxModelViewSet):
    queryset = models.DeviceTypeDocument.objects.prefetch_related('tags')
    serializer_class = DeviceTypeDocumentSerializer
    filterset_class = filtersets.DeviceTypeDocumentFilterSet

class CircuitDocumentViewSet(NetBoxModelViewSet):
    queryset = models.CircuitDocument.objects.prefetch_related('tags')
    serializer_class = CircuitDocumentSerializer
    filterset_class = filtersets.CircuitDocumentFilterSet

class VMDocumentViewSet(NetBoxModelViewSet):
    queryset = models.VMDocument.objects.prefetch_related('tags')
    serializer_class = VMDocumentSerializer
    filterset_class = filtersets.VMDocumentFilterSet

class CircuitProviderDocumentViewSet(NetBoxModelViewSet):
    queryset = models.CircuitProviderDocument.objects.prefetch_related('tags')
    serializer_class = CircuitProviderDocumentSerializer
    filterset_class = filtersets.CircuitProviderDocumentFilterSet