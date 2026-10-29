from unittest.mock import patch

from django.test import TestCase

from dcim.models import Site
from netbox_documents.template_content import _make_extension


class DocumentPanelRenderTest(TestCase):
    """Tests for whether the documents panel renders based on allowed_doc_types."""

    @classmethod
    def setUpTestData(cls):
        cls.site = Site.objects.create(name='Test Site', slug='test-site')

    def _render(self, allowed_doc_types):
        config = {'netbox_documents': {'allowed_doc_types': allowed_doc_types}}
        extension = _make_extension('dcim.site')({'object': self.site})
        with self.settings(PLUGINS_CONFIG=config), \
                patch.object(extension, 'render', return_value='rendered') as mock_render:
            return extension._render_panel(), mock_render

    def test_renders_with_default_config(self):
        """Panel should render when allowed_doc_types is unset (all types allowed)."""
        result, mock_render = self._render({})
        self.assertEqual(result, 'rendered')
        mock_render.assert_called_once()

    def test_renders_when_model_has_allowed_types(self):
        """Panel should render when the model has at least one allowed type."""
        result, _ = self._render({'dcim.site': ['diagram']})
        self.assertEqual(result, 'rendered')

    def test_renders_when_model_unmapped_and_no_all_key(self):
        """Panel should render when the model isn't mapped and there is no __all__ fallback."""
        result, _ = self._render({'dcim.device': ['diagram']})
        self.assertEqual(result, 'rendered')

    def test_hidden_when_model_has_no_allowed_types(self):
        """Panel should be hidden when the model is explicitly configured with no types."""
        result, mock_render = self._render({'dcim.site': []})
        self.assertEqual(result, '')
        mock_render.assert_not_called()

    def test_hidden_when_all_key_is_empty(self):
        """Panel should be hidden when __all__ is an empty list and the model isn't mapped."""
        result, _ = self._render({'__all__': []})
        self.assertEqual(result, '')
