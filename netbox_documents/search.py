from netbox.search import SearchIndex
from .models import SiteDocument, LocationDocument, DeviceDocument, DeviceTypeDocument, CircuitDocument, VMDocument, CircuitProviderDocument
from django.conf import settings

# If we run NB 3.4+ register search indexes 
if settings.VERSION >= '3.4.0':
    class SiteDocumentIndex(SearchIndex):
        model = SiteDocument
        fields = (
            ("name", 100),
            ("document", 500),
            ("comments", 5000),
        )

    class LocationDocumentIndex(SearchIndex):
        model = LocationDocument
        fields = (
            ("name", 100),
            ("document", 500),
            ("comments", 5000),
        )

    class CircuitDocumentIndex(SearchIndex):
        model = CircuitDocument
        fields = (
            ("name", 100),
            ("document", 500),
            ("comments", 5000),
        )

    class DeviceTypeDocumentIndex(SearchIndex):
        model = DeviceTypeDocument
        fields = (
            ("name", 100),
            ("document", 500),
            ("comments", 5000),
        )

    class DeviceDocumentIndex(SearchIndex):
        model = DeviceDocument
        fields = (
            ("name", 100),
            ("document", 500),
            ("comments", 5000),
        )

    class VMDocumentIndex(SearchIndex):
        model = VMDocument
        fields = (
            ("name", 100),
            ("document", 500),
            ("comments", 5000),
        )

    class CircuitProviderDocumentIndex(SearchIndex):
        model = CircuitProviderDocument
        fields = (
            ("name", 100),
            ("document", 500),
            ("comments", 5000),
        )

    # Register indexes
    indexes = [SiteDocumentIndex, LocationDocumentIndex, CircuitDocumentIndex, DeviceTypeDocumentIndex, DeviceDocumentIndex, VMDocumentIndex, CircuitProviderDocumentIndex]