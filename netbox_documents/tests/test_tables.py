from django.contrib.contenttypes.models import ContentType
from django.test import TestCase

from dcim.models import Site
from netbox_documents.models import Document
from netbox_documents.tables import DocumentTable


class DocumentTableExportTest(TestCase):
    """Tests for DocumentTable export output."""

    @classmethod
    def setUpTestData(cls):
        site = Site.objects.create(name='Test Site', slug='test-site')
        ct = ContentType.objects.get_for_model(Site)
        Document.objects.create(
            name='Rack diagram', external_url='https://example.com/a.pdf',
            document_type='diagram', content_type=ct, object_id=site.pk,
        )
        Document.objects.create(
            external_url='https://example.com/b.pdf',
            document_type='other', content_type=ct, object_id=site.pk,
        )

    def _export_names(self):
        table = DocumentTable(Document.objects.order_by('pk'))
        return [row.get_cell_value('name') for row in table.rows]

    def test_export_name_excludes_link_text(self):
        """Exported name should be the document name, not the rendered link text."""
        self.assertEqual(self._export_names()[0], 'Rack diagram')

    def test_export_name_falls_back_to_url(self):
        """Exported name should fall back to the external URL when no name is set."""
        self.assertEqual(self._export_names()[1], 'https://example.com/b.pdf')
