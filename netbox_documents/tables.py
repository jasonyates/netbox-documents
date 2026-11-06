import django_tables2 as tables
from django.template.defaultfilters import filesizeformat
from netbox.tables import NetBoxTable, columns
from .models import Document

DOCUMENT_LINK = """
<a href="{% url 'plugins:netbox_documents:document' pk=record.pk %}">{% firstof record.name record.filename %}</a>
{% if record.external_url %}
    (<a href="{{ record.external_url }}" target="_blank" rel="noopener noreferrer">View External Document</a>)
{% elif record.document %}
    (<a href="{{ record.document.url }}" target="_blank">View Document</a>)
{% endif %}
"""


class DocumentTable(NetBoxTable):
    name = tables.TemplateColumn(
        template_code=DOCUMENT_LINK,
        order_by=('name',),
    )
    document_type = columns.ChoiceFieldColumn()
    assigned_object = tables.Column(
        linkify=True,
        orderable=False,
        verbose_name='Assigned Object',
    )
    content_type = columns.ContentTypeColumn(
        verbose_name='Object Type',
    )
    size = tables.Column(
        orderable=False,
        verbose_name='Size',
    )
    filename = tables.Column(
        orderable=False,
        verbose_name='Filename',
    )
    comments = columns.MarkdownColumn()
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

    def render_size(self, value):
        return filesizeformat(value) if value else ''
