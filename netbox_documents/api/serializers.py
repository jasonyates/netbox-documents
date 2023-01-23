from rest_framework import serializers

from netbox.api.serializers import NetBoxModelSerializer, WritableNestedSerializer
from ..models import SiteDocument, DeviceDocument, DeviceTypeDocument, CircuitDocument 
from dcim.api.nested_serializers import NestedSiteSerializer, NestedDeviceSerializer, NestedDeviceTypeSerializer 
from circuits.api.nested_serializers import NestedCircuitSerializer

# Site Document Serializer
class SiteDocumentSerializer(NetBoxModelSerializer):

    url = serializers.HyperlinkedIdentityField(
        view_name='plugins-api:netbox_documents-api:sitedocument-detail'
    )

    site = NestedSiteSerializer()

    class Meta:
        model = SiteDocument
        fields = (
            'id', 'url', 'display', 'name', 'document', 'external_url', 'document_type', 'filename', 'site', 'comments', 'tags', 'custom_fields', 'created',
            'last_updated',
        )

class NestedSiteDocumentSerializer(WritableNestedSerializer):

    url = serializers.HyperlinkedIdentityField(
        view_name='plugins-api:netbox_documents-api:sitedocument-detail'
    )

    class Meta:
        model = SiteDocument
        fields = (
            'id', 'url', 'display', 'name', 'document', 'external_url', 'document_type', 'filename',
        )


# Device Document Serializer
class DeviceDocumentSerializer(NetBoxModelSerializer):

    url = serializers.HyperlinkedIdentityField(
        view_name='plugins-api:netbox_documents-api:devicedocument-detail'
    )

    device = NestedDeviceSerializer()

    class Meta:
        model = DeviceDocument
        fields = (
            'id', 'url', 'display', 'name', 'document', 'external_url', 'document_type', 'filename', 'device', 'comments', 'tags', 'custom_fields', 'created',
            'last_updated',
        )

class NestedDeviceDocumentSerializer(WritableNestedSerializer):

    url = serializers.HyperlinkedIdentityField(
        view_name='plugins-api:netbox_documents-api:devicedocument-detail'
    )

    class Meta:
        model = DeviceDocument
        fields = (
            'id', 'url', 'display', 'name', 'document', 'external_url', 'document_type', 'filename',
        )


class DeviceTypeDocumentSerializer(NetBoxModelSerializer):

    url = serializers.HyperlinkedIdentityField(
        view_name='plugins-api:netbox_documents-api:devicetypedocument-detail'
    )

    device_type = NestedDeviceTypeSerializer()

    class Meta:
        model = DeviceTypeDocument
        fields = (
            'id', 'url', 'display', 'name', 'document', 'external_url', 'document_type', 'filename', 'device_type', 'comments', 'tags', 'custom_fields', 'created',
            'last_updated',
        )

# Circuit Document Serializer
class CircuitDocumentSerializer(NetBoxModelSerializer):

    url = serializers.HyperlinkedIdentityField(
        view_name='plugins-api:netbox_documents-api:circuitdocument-detail'
    )

    circuit = NestedCircuitSerializer()

    class Meta:
        model = CircuitDocument
        fields = (
            'id', 'url', 'display', 'name', 'document', 'external_url', 'document_type', 'filename', 'circuit', 'comments', 'tags', 'custom_fields', 'created',
            'last_updated',
        )

class NestedCircuitDocumentSerializer(WritableNestedSerializer):

    url = serializers.HyperlinkedIdentityField(
        view_name='plugins-api:netbox_documents-api:circuitdocument-detail'
    )

    class Meta:
        model = CircuitDocument
        fields = (
            'id', 'url', 'display', 'name', 'document', 'external_url', 'document_type', 'filename',
        )
