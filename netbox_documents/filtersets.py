from netbox.filtersets import NetBoxModelFilterSet
from .models import SiteDocument, LocationDocument, DeviceDocument, DeviceTypeDocument, CircuitDocument, VMDocument, CircuitProviderDocument
from django.db.models import Q

class SiteDocumentFilterSet(NetBoxModelFilterSet):

    class Meta:
        model = SiteDocument
        fields = ('id', 'name', 'document_type', 'site')

    def search(self, queryset, name, value):
        if not value.strip():
            return queryset
        return queryset.filter(
            Q(name__icontains=value) |
            Q(document__icontains=value)
        )

class LocationDocumentFilterSet(NetBoxModelFilterSet):

    class Meta:
        model = LocationDocument
        fields = ('id', 'name', 'document_type', 'site', 'location')

    def search(self, queryset, name, value):
        if not value.strip():
            return queryset
        return queryset.filter(
            Q(name__icontains=value) |
            Q(document__icontains=value)
        )

class DeviceDocumentFilterSet(NetBoxModelFilterSet):

    class Meta:
        model = DeviceDocument
        fields = ('id', 'name', 'document_type', 'device')

    def search(self, queryset, name, value):
        if not value.strip():
            return queryset
        return queryset.filter(
            Q(name__icontains=value) |
            Q(document__icontains=value)
        )


class DeviceTypeDocumentFilterSet(NetBoxModelFilterSet):

    class Meta:
        model = DeviceTypeDocument
        fields = ('id', 'name', 'document_type', 'device_type')

    def search(self, queryset, name, value):
        if not value.strip():
            return queryset
        return queryset.filter(
            Q(name__icontains=value) |
            Q(document__icontains=value)
        )

class CircuitDocumentFilterSet(NetBoxModelFilterSet):

    class Meta:
        model = CircuitDocument
        fields = ('id', 'name', 'document_type', 'circuit')

    def search(self, queryset, name, value):
        if not value.strip():
            return queryset
        return queryset.filter(
            Q(name__icontains=value) |
            Q(document__icontains=value)
        )

class VMDocumentFilterSet(NetBoxModelFilterSet):

    class Meta:
        model = VMDocument
        fields = ('id', 'name', 'document_type', 'vm')

    def search(self, queryset, name, value):
        if not value.strip():
            return queryset
        return queryset.filter(
            Q(name__icontains=value) |
            Q(document__icontains=value)
        )
    
class CircuitProviderDocumentFilterSet(NetBoxModelFilterSet):

    class Meta:
        model = CircuitProviderDocument
        fields = ('id', 'name', 'document_type', 'provider')

    def search(self, queryset, name, value):
        if not value.strip():
            return queryset
        return queryset.filter(
            Q(name__icontains=value) |
            Q(document__icontains=value)
        )