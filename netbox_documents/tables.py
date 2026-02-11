import django_tables2 as tables
from netbox.tables import NetBoxTable, columns
from .models import Document

DOCUMENT_LINK = """
{% if record.size %}
    <a href="{% url 'plugins:netbox_documents:document' pk=record.pk %}">{% firstof record.name record.filename %}</a> (<a href="{{record.document.url}}" target="_blank">View Document</a>)
{% else %}
    <a href="{% url 'plugins:netbox_documents:document' pk=record.pk %}">{% firstof record.name record.filename %}</a> (<a href="{{ record.external_url }}" target="_blank">View External Document</a>)
{% endif %}
"""


class DocumentTable(NetBoxTable):
    name = tables.TemplateColumn(template_code=DOCUMENT_LINK)
    document_type = columns.ChoiceFieldColumn()
    assigned_object = tables.Column(
        linkify=True,
        verbose_name='Assigned Object',
    )
    content_type = columns.ContentTypeColumn(
        verbose_name='Object Type',
    )

    tags = columns.TagColumn(
        url_name='plugins:netbox_documents:document_list'
    )

    class Meta(NetBoxTable.Meta):
        model = Document
        fields = (
            'pk', 'id', 'name', 'document_type', 'size', 'filename',
            'content_type', 'assigned_object', 'comments', 'actions',
            'created', 'last_updated', 'tags',
        )
        default_columns = ('name', 'document_type', 'content_type', 'assigned_object', 'tags')
