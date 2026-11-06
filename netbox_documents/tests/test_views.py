from unittest.mock import patch

from django.contrib.contenttypes.models import ContentType
from django.test import TestCase

from netbox_documents.tables import DocumentTable
from netbox_documents.template_content import _make_extension
from netbox_documents.views import DocumentListView


class DocumentPanelRenderTest(TestCase):
    """Tests for _render_panel() visibility based on allowed_doc_types."""

    def setUp(self):
        self.obj = ContentType.objects.get_for_model(ContentType)
        extension_class = _make_extension('contenttypes.contenttype')
        self.extension = extension_class.__new__(extension_class)
        self.extension.context = {'object': self.obj}

    def _render(self, allowed):
        with patch('netbox_documents.template_content.get_allowed_doc_types', return_value=allowed), \
                patch.object(self.extension, 'render', return_value='panel'), \
                patch.object(self.extension, '_get_return_url', return_value='/'):
            return self.extension._render_panel()

    def test_panel_renders_when_all_types_allowed(self):
        """None (default config) means all types are allowed, so the panel should render."""
        self.assertEqual(self._render(None), 'panel')

    def test_panel_renders_when_types_configured(self):
        self.assertEqual(self._render(['diagram']), 'panel')

    def test_panel_hidden_when_no_types_allowed(self):
        """An explicitly empty list should hide the panel."""
        self.assertEqual(self._render([]), '')


class DocumentTableTest(TestCase):

    def test_non_database_columns_not_orderable(self):
        """Columns backed by a GenericForeignKey or a property can't be sorted in the database."""
        table = DocumentTable([])
        for name in ('assigned_object', 'size', 'filename'):
            self.assertFalse(table.columns[name].orderable, f"Column '{name}' should not be orderable")


class DocumentListViewTest(TestCase):

    def test_actions_are_object_action_classes(self):
        """NetBox 4.7 requires actions to be ObjectAction classes, not a dict of names."""
        from netbox.object_actions import ObjectAction
        for action in DocumentListView.actions:
            self.assertTrue(issubclass(action, ObjectAction))
