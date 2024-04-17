import django_tables2 as tables

from netbox.tables import NetBoxTable, columns
from .models import SiteDocument, LocationDocument, DeviceDocument, DeviceTypeDocument, CircuitDocument, VMDocument

SITE_DOCUMENT_LINK = """
{% if record.size %}
    <a href="{% url 'plugins:netbox_documents:sitedocument' pk=record.pk %}">{% firstof record.name record.filename %}</a> (<a href="{{record.document.url}}" target="_blank">View Document</a>)
{% else %}
    <a href="{% url 'plugins:netbox_documents:sitedocument' pk=record.pk %}">{% firstof record.name record.filename %}</a> (<a href="{{ record.external_url }}" target="_blank">View External Document</a>)
{% endif %}
"""

LOCATION_DOCUMENT_LINK = """
{% if record.size %}
    <a href="{% url 'plugins:netbox_documents:locationdocument' pk=record.pk %}">{% firstof record.name record.filename %}</a> (<a href="{{record.document.url}}" target="_blank">View Document</a>)
{% else %}
    <a href="{% url 'plugins:netbox_documents:locationdocument' pk=record.pk %}">{% firstof record.name record.filename %}</a> (<a href="{{ record.external_url }}" target="_blank">View External Document</a>)
{% endif %}
"""

CIRCUIT_DOCUMENT_LINK = """
{% if record.size %}
    <a href="{% url 'plugins:netbox_documents:circuitdocument' pk=record.pk %}">{% firstof record.name record.filename %}</a> (<a href="{{record.document.url}}" target="_blank">View Document</a>)
{% else %}
    <a href="{% url 'plugins:netbox_documents:circuitdocument' pk=record.pk %}">{% firstof record.name record.filename %}</a> (<a href="{{ record.external_url }}" target="_blank">View External Document</a>)
{% endif %}
"""

DEVICE_DOCUMENT_LINK = """
{% if record.size %}
    <a href="{% url 'plugins:netbox_documents:devicedocument' pk=record.pk %}">{% firstof record.name record.filename %}</a> (<a href="{{record.document.url}}" target="_blank">View Document</a>)
{% else %}
    <a href="{% url 'plugins:netbox_documents:devicedocument' pk=record.pk %}">{% firstof record.name record.filename %}</a> (<a href="{{ record.external_url }}" target="_blank">View External Document</a>)
{% endif %}
"""

DEVICE_TYPE_DOCUMENT_LINK = """
{% if record.size %}
    <a href="{% url 'plugins:netbox_documents:devicetypedocument' pk=record.pk %}">{% firstof record.name record.filename %}</a> (<a href="{{record.document.url}}" target="_blank">View Document</a>)
{% else %}
    <a href="{% url 'plugins:netbox_documents:devicetypedocument' pk=record.pk %}">{% firstof record.name record.filename %}</a> (<a href="{{ record.external_url }}" target="_blank">View External Document</a>)
{% endif %}
"""

VM_DOCUMENT_LINK = """
{% if record.size %}
    <a href="{% url 'plugins:netbox_documents:vmdocument' pk=record.pk %}">{% firstof record.name record.filename %}</a> (<a href="{{record.document.url}}" target="_blank">View Document</a>)
{% else %}
    <a href="{% url 'plugins:netbox_documents:vmdocument' pk=record.pk %}">{% firstof record.name record.filename %}</a> (<a href="{{ record.external_url }}" target="_blank">View External Document</a>)
{% endif %}
"""

CIRCUIT_PROVIDER_DOCUMENT_LINK = """
{% if record.size %}
    <a href="{% url 'plugins:netbox_documents:circuitproviderdocument' pk=record.pk %}">{% firstof record.name record.filename %}</a> (<a href="{{record.document.url}}" target="_blank">View Document</a>)
{% else %}
    <a href="{% url 'plugins:netbox_documents:circuitproviderdocument' pk=record.pk %}">{% firstof record.name record.filename %}</a> (<a href="{{ record.external_url }}" target="_blank">View External Document</a>)
{% endif %}
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

class LocationDocumentTable(NetBoxTable):
    name = tables.TemplateColumn(template_code=LOCATION_DOCUMENT_LINK)
    document_type = columns.ChoiceFieldColumn()
    site = tables.Column(
        linkify=True
    )
    location = tables.Column(
        linkify=True
    )

    tags = columns.TagColumn(
        url_name='plugins:netbox_documents:locationdocument_list'
    )

    class Meta(NetBoxTable.Meta):
        model = LocationDocument
        fields = ('pk', 'id', 'name', 'document_type',  'size', 'filename', 'site', 'location', 'comments', 'actions', 'created', 'last_updated', 'tags')
        default_columns = ('name', 'document_type', 'site', 'location', 'tags')

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


class DeviceTypeDocumentTable(NetBoxTable):
    name = tables.TemplateColumn(template_code=DEVICE_TYPE_DOCUMENT_LINK)
    document_type = columns.ChoiceFieldColumn()
    device_type = tables.Column(
        linkify=True
    )

    tags = columns.TagColumn(
        url_name='dcim:sitegroup_list'
    )

    class Meta(NetBoxTable.Meta):
        model = DeviceTypeDocument
        fields = ('pk', 'id', 'name', 'document_type',  'size', 'filename', 'device_type', 'comments', 'actions', 'created', 'last_updated', 'tags')
        default_columns = ('name', 'document_type', 'device_type', 'tags')

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

class VMDocumentTable(NetBoxTable):
    name = tables.TemplateColumn(template_code=VM_DOCUMENT_LINK)
    document_type = columns.ChoiceFieldColumn()
    vm = tables.Column(
        linkify=True
    )

    tags = columns.TagColumn(
        url_name='dcim:sitegroup_list'
    )

    class Meta(NetBoxTable.Meta):
        model = VMDocument
        fields = ('pk', 'id', 'name', 'document_type',  'size', 'filename', 'vm', 'comments', 'actions', 'created', 'last_updated', 'tags')
        default_columns = ('name', 'document_type', 'vm', 'tags')

class CircuitProviderDocumentTable(NetBoxTable):
    name = tables.TemplateColumn(template_code=CIRCUIT_DOCUMENT_LINK)
    document_type = columns.ChoiceFieldColumn()
    provider = tables.Column(
        linkify=True
    )

    tags = columns.TagColumn(
        url_name='dcim:sitegroup_list'
    )

    class Meta(NetBoxTable.Meta):
        model = CircuitDocument
        fields = ('pk', 'id', 'name', 'document_type',  'size', 'filename', 'provider', 'comments', 'actions', 'created', 'last_updated', 'tags')
        default_columns = ('name', 'document_type', 'provider', 'tags')