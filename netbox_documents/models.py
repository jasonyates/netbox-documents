from django.conf import settings
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import ValidationError
from django.db import models
from django.urls import reverse

from netbox.models import NetBoxModel
from utilities.choices import ChoiceSet
from .utils import file_upload


# Built-in document type choices (always available)
_BUILTIN_CHOICES = [
    ('diagram', 'Network Diagram', 'green'),
    ('floorplan', 'Floor Plan', 'purple'),
    ('purchaseorder', 'Purchase Order', 'orange'),
    ('quote', 'Quote', 'indigo'),
    ('wirelessmodel', 'Wireless Model (Ekahau)', 'yellow'),
    ('manual', 'Manual', 'pink'),
    ('supportcontract', 'Support Contract', 'blue'),
    ('circuitcontract', 'Circuit Contract', 'red'),
    ('contract', 'Contract', 'red'),
    ('msa', 'MSA', 'green'),
    ('kmz', 'KMZ', 'blue'),
    ('other', 'Other', 'gray'),
]


def _build_all_choices():
    """Combine built-in choices with any user-defined custom types from plugin settings."""
    plugin_settings = settings.PLUGINS_CONFIG.get('netbox_documents', {})
    custom_types = plugin_settings.get('custom_doc_types', [])

    all_choices = list(_BUILTIN_CHOICES)
    seen = {c[0] for c in all_choices}

    for entry in custom_types:
        if len(entry) != 3:
            continue
        value, label, color = entry
        if value not in seen:
            all_choices.append((value, label, color))
            seen.add(value)

    return all_choices


class DocTypeChoices(ChoiceSet):
    """Document type choices -- built-in types plus any custom types from plugin config."""

    key = 'DocTypeChoices.document'

    CHOICES = _build_all_choices()


def get_allowed_doc_types(content_type_id):
    """
    Return the list of allowed document type values for the given content_type,
    or None if all types should be shown.
    """
    plugin_settings = settings.PLUGINS_CONFIG.get('netbox_documents', {})
    allowed_map = plugin_settings.get('allowed_doc_types', {})

    if not allowed_map:
        return None

    if content_type_id is None:
        return allowed_map.get('__all__')

    try:
        ct = ContentType.objects.get(pk=content_type_id)
        model_label = f'{ct.app_label}.{ct.model}'
    except ContentType.DoesNotExist:
        return allowed_map.get('__all__')

    if model_label in allowed_map:
        return allowed_map[model_label]

    return allowed_map.get('__all__')


class Document(NetBoxModel):
    name = models.CharField(
        max_length=100,
        blank=True,
        help_text='(Optional) Specify a name to display for this document. If no name is specified, the filename or URL will be used.'
    )

    document = models.FileField(
        upload_to=file_upload,
        blank=True
    )

    external_url = models.URLField(
        blank=True,
        max_length=255
    )

    document_type = models.CharField(
        max_length=30,
        choices=DocTypeChoices
    )

    comments = models.TextField(
        blank=True
    )

    # Generic relation fields
    content_type = models.ForeignKey(
        to=ContentType,
        on_delete=models.CASCADE
    )
    object_id = models.PositiveBigIntegerField()
    assigned_object = GenericForeignKey('content_type', 'object_id')

    clone_fields = (
        'content_type', 'object_id', 'document_type',
    )

    class Meta:
        ordering = ('name',)
        verbose_name = "Document"
        verbose_name_plural = "Documents"
        indexes = [
            models.Index(fields=['content_type', 'object_id']),
        ]

    def get_document_type_color(self):
        return DocTypeChoices.colors.get(self.document_type)

    @property
    def size(self):
        expected_exceptions = [OSError]
        try:
            from botocore.exceptions import ClientError
            expected_exceptions.append(ClientError)
        except ImportError:
            pass
        try:
            return self.document.size
        except:
            return None

    @property
    def filename(self):
        if self.external_url:
            return self.external_url
        elif self.document:
            filename = self.document.name.rsplit('/', 1)[-1]
            return filename.split('_', 1)[1]

    def __str__(self):
        if self.name:
            return self.name
        if self.external_url:
            return self.external_url
        if self.document:
            filename = self.document.name.rsplit('/', 1)[-1]
            return filename.split('_', 1)[1]
        return ""

    def get_absolute_url(self):
        return reverse('plugins:netbox_documents:document', args=[self.pk])

    def clean(self):
        super().clean()
        if not self.document and self.external_url == '':
            raise ValidationError("A document must contain an uploaded file or an external URL.")
        if self.document and self.external_url:
            raise ValidationError("A document cannot contain both an uploaded file and an external URL.")

    def delete(self, *args, **kwargs):
        if self.external_url == '':
            _name = self.document.name
            super().delete(*args, **kwargs)
            self.document.delete(save=False)
            self.document.name = _name
        else:
            super().delete(*args, **kwargs)
