from rest_framework import serializers

from netbox.api.serializers import NetBoxModelSerializer, WritableNestedSerializer
from ..models import SiteDocument, LocationDocument, DeviceDocument, DeviceTypeDocument, CircuitDocument, VMDocument, CircuitProviderDocument
from dcim.api.nested_serializers import NestedSiteSerializer, NestedLocationSerializer, NestedDeviceSerializer, NestedDeviceTypeSerializer 
from circuits.api.nested_serializers import NestedCircuitSerializer, NestedProviderSerializer
from virtualization.api.nested_serializers import NestedVirtualMachineSerializer
from .fields import UploadableBase64FileField

# Site Document Serializer
class SiteDocumentSerializer(NetBoxModelSerializer):

    url = serializers.HyperlinkedIdentityField(
        view_name='plugins-api:netbox_documents-api:sitedocument-detail'
    )

    site = NestedSiteSerializer()
    document = UploadableBase64FileField(required=False)

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


# Location Document Serializer
class LocationDocumentSerializer(NetBoxModelSerializer):

    url = serializers.HyperlinkedIdentityField(
        view_name='plugins-api:netbox_documents-api:locationdocument-detail'
    )

    location = NestedLocationSerializer()
    site = NestedSiteSerializer()
    document = UploadableBase64FileField(required=False)
    
    class Meta:
        model = LocationDocument
        fields = (
            'id', 'url', 'display', 'name', 'document', 'external_url', 'document_type', 'filename', 'site', 'location', 'comments', 'tags', 'custom_fields', 'created',
            'last_updated',
        )

class NestedLocationDocumentSerializer(WritableNestedSerializer):

    url = serializers.HyperlinkedIdentityField(
        view_name='plugins-api:netbox_documents-api:locationdocument-detail'
    )

    class Meta:
        model = LocationDocument
        fields = (
            'id', 'url', 'display', 'name', 'document', 'external_url', 'document_type', 'filename',
        )


# Device Document Serializer
class DeviceDocumentSerializer(NetBoxModelSerializer):

    url = serializers.HyperlinkedIdentityField(
        view_name='plugins-api:netbox_documents-api:devicedocument-detail'
    )

    device = NestedDeviceSerializer()
    document = UploadableBase64FileField(required=False)

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
    document = UploadableBase64FileField(required=False)

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
    document = UploadableBase64FileField(required=False)

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

# VM Document Serializer
class VMDocumentSerializer(NetBoxModelSerializer):

    url = serializers.HyperlinkedIdentityField(
        view_name='plugins-api:netbox_documents-api:vmdocument-detail'
    )

    vm = NestedVirtualMachineSerializer()
    document = UploadableBase64FileField(required=False)

    class Meta:
        model = VMDocument
        fields = (
            'id', 'url', 'display', 'name', 'document', 'external_url', 'document_type', 'filename', 'vm', 'comments', 'tags', 'custom_fields', 'created',
            'last_updated',
        )

class NestedVMDocumentSerializer(WritableNestedSerializer):

    url = serializers.HyperlinkedIdentityField(
        view_name='plugins-api:netbox_documents-api:vmdocument-detail'
    )

    class Meta:
        model = VMDocument
        fields = (
            'id', 'url', 'display', 'name', 'document', 'external_url', 'document_type', 'filename',
        )

# Circuit Provider Document Serializer
class CircuitProviderDocumentSerializer(NetBoxModelSerializer):

    url = serializers.HyperlinkedIdentityField(
        view_name='plugins-api:netbox_documents-api:circuitproviderdocument-detail'
    )

    provider = NestedProviderSerializer()
    document = UploadableBase64FileField(required=False)

    class Meta:
        model = CircuitProviderDocument
        fields = (
            'id', 'url', 'display', 'name', 'document', 'external_url', 'document_type', 'filename', 'provider', 'comments', 'tags', 'custom_fields', 'created',
            'last_updated',
        )

class NestedCircuitProviderDocumentSerializer(WritableNestedSerializer):

    url = serializers.HyperlinkedIdentityField(
        view_name='plugins-api:netbox_documents-api:circuitdocument-detail'
    )

    class Meta:
        model = CircuitProviderDocument
        fields = (
            'id', 'url', 'display', 'name', 'document', 'external_url', 'document_type', 'filename',
        )