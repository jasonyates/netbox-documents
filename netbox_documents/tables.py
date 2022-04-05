import django_tables2 as tables

from netbox.tables import NetBoxTable, columns
from .models import SiteDocument, DeviceDocument, CircuitDocument

SITE_DOCUMENT_LINK = """
<a href="{% url 'plugins:netbox_documents:sitedocument' pk=record.pk %}">
    {% firstof record.name record.filename %}
</a> (<a href="{{record.document.url}}" target="_blank">View Document</a>)
"""

CIRCUIT_DOCUMENT_LINK = """
<a href="{% url 'plugins:netbox_documents:circuitdocument' pk=record.pk %}">
    {% firstof record.name record.filename %}
</a> (<a href="{{record.document.url}}" target="_blank">View Document</a>)
"""

DEVICE_DOCUMENT_LINK = """
<a href="{% url 'plugins:netbox_documents:devicedocument' pk=record.pk %}">
    {% firstof record.name record.filename %}
</a> (<a href="{{record.document.url}}" target="_blank">View Document</a>)
"""

class SiteDocumentTable(NetBoxTable):
    name = tables.TemplateColumn(template_code=SITE_DOCUMENT_LINK)
    document_type = columns.ChoiceFieldColumn()
    site = tables.Column(
        linkify=True
    )

    tags = columns.TagColumn(
        url_name='plugins:netbox_documents:sitedocument_list'
    )

    class Meta(NetBoxTable.Meta):
        model = SiteDocument
        fields = ('pk', 'id', 'name', 'document_type',  'size', 'filename', 'site', 'comments', 'actions', 'created', 'last_updated', 'tags')
        default_columns = ('name', 'document_type', 'site', 'tags')

class DeviceDocumentTable(NetBoxTable):
    name = tables.TemplateColumn(template_code=DEVICE_DOCUMENT_LINK)
    document_type = columns.ChoiceFieldColumn()
    device = tables.Column(
        linkify=True
    )

    tags = columns.TagColumn(
        url_name='dcim:sitegroup_list'
    )

    class Meta(NetBoxTable.Meta):
        model = DeviceDocument
        fields = ('pk', 'id', 'name', 'document_type',  'size', 'filename', 'device', 'comments', 'actions', 'created', 'last_updated', 'tags')
        default_columns = ('name', 'document_type', 'device', 'tags')

class CircuitDocumentTable(NetBoxTable):
    name = tables.TemplateColumn(template_code=CIRCUIT_DOCUMENT_LINK)
    document_type = columns.ChoiceFieldColumn()
    circuit = tables.Column(
        linkify=True
    )

    tags = columns.TagColumn(
        url_name='dcim:sitegroup_list'
    )

    class Meta(NetBoxTable.Meta):
        model = CircuitDocument
        fields = ('pk', 'id', 'name', 'document_type',  'size', 'filename', 'circuit', 'comments', 'actions', 'created', 'last_updated', 'tags')
        default_columns = ('name', 'document_type', 'circuit', 'tags')