from django.core.exceptions import ObjectDoesNotExist
from rest_framework import serializers

from django.contrib.contenttypes.models import ContentType

from netbox.api.serializers import NetBoxModelSerializer
from netbox.api.fields import ContentTypeField
from netbox.api.gfk_fields import GFKSerializerField
from ..models import Document
from .fields import UploadableBase64FileField


class DocumentSerializer(NetBoxModelSerializer):

    url = serializers.HyperlinkedIdentityField(
        view_name='plugins-api:netbox_documents-api:document-detail'
    )

    content_type = ContentTypeField(queryset=ContentType.objects.all(), write_only=True)
    object_id = serializers.IntegerField(write_only=True)
    assigned_object = GFKSerializerField(read_only=True)
    document = UploadableBase64FileField(required=False)

    class Meta:
        model = Document
        fields = (
            'id', 'url', 'display', 'name', 'document', 'external_url',
            'document_type', 'filename', 'content_type', 'object_id',
            'assigned_object', 'comments', 'tags', 'custom_fields',
            'created', 'last_updated',
        )
        brief_fields = (
            'id', 'url', 'display', 'name', 'document_type', 'filename',
        )

    def validate(self, data):
        # Validate that the assigned object exists
        if data.get('content_type') and data.get('object_id'):
            try:
                data['content_type'].get_object_for_this_type(id=data['object_id'])
            except ObjectDoesNotExist:
                raise serializers.ValidationError(
                    "Invalid assigned object: {} ID {}".format(data['content_type'], data['object_id'])
                )

        super().validate(data)
        return data
