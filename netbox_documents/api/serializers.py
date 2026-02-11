from rest_framework import serializers
from django.contrib.contenttypes.models import ContentType

from netbox.api.serializers import NetBoxModelSerializer, WritableNestedSerializer
from netbox.api.fields import ContentTypeField
from ..models import Document
from .fields import UploadableBase64FileField


class DocumentSerializer(NetBoxModelSerializer):

    url = serializers.HyperlinkedIdentityField(
        view_name='plugins-api:netbox_documents-api:document-detail'
    )

    content_type = ContentTypeField(queryset=ContentType.objects.all())
    document = UploadableBase64FileField(required=False)

    class Meta:
        model = Document
        fields = (
            'id', 'url', 'display', 'name', 'document', 'external_url',
            'document_type', 'filename', 'content_type', 'object_id',
            'comments', 'tags', 'custom_fields',
            'created', 'last_updated',
        )


class NestedDocumentSerializer(WritableNestedSerializer):

    url = serializers.HyperlinkedIdentityField(
        view_name='plugins-api:netbox_documents-api:document-detail'
    )

    class Meta:
        model = Document
        fields = (
            'id', 'url', 'display', 'name', 'document', 'external_url',
            'document_type', 'filename',
        )
