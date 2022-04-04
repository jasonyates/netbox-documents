from rest_framework import serializers

from netbox.api.serializers import NetBoxModelSerializer
from ..models import SiteDocument, DeviceDocument, CircuitDocument
from dcim.api.nested_serializers import NestedSiteSerializer, NestedDeviceSerializer
from circuits.api.nested_serializers import NestedCircuitSerializer

class SiteDocumentSerializer(NetBoxModelSerializer):

    url = serializers.HyperlinkedIdentityField(
        view_name='plugins-api:netbox_documents-api:sitedocument-detail'
    )

    site = NestedSiteSerializer()

    class Meta:
        model = SiteDocument
        fields = (
            'id', 'url', 'display', 'name', 'document', 'document_type', 'filename', 'site', 'comments', 'tags', 'custom_fields', 'created',
            'last_updated',
        )

class DeviceDocumentSerializer(NetBoxModelSerializer):

    url = serializers.HyperlinkedIdentityField(
        view_name='plugins-api:netbox_documents-api:devicedocument-detail'
    )

    device = NestedDeviceSerializer()

    class Meta:
        model = DeviceDocument
        fields = (
            'id', 'url', 'display', 'name', 'document', 'document_type', 'filename', 'device', 'comments', 'tags', 'custom_fields', 'created',
            'last_updated',
        )

class CircuitDocumentSerializer(NetBoxModelSerializer):

    url = serializers.HyperlinkedIdentityField(
        view_name='plugins-api:netbox_documents-api:circuitdocument-detail'
    )

    circuit = NestedCircuitSerializer()

    class Meta:
        model = CircuitDocument
        fields = (
            'id', 'url', 'display', 'name', 'document', 'document_type', 'filename', 'circuit', 'comments', 'tags', 'custom_fields', 'created',
            'last_updated',
        )