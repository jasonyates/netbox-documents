from django.contrib.contenttypes.models import ContentType
from netbox.plugins import PluginTemplateExtension
from django.conf import settings
from .models import Document

plugin_settings = settings.PLUGINS_CONFIG.get('netbox_documents', {})

# Models that get the documents panel on their detail pages
DOCUMENT_MODELS = [
    'dcim.site',
    'dcim.location',
    'dcim.device',
    'dcim.devicetype',
    'dcim.moduletype',
    'circuits.circuit',
    'virtualization.virtualmachine',
    'circuits.provider',
]


def _make_extension(model_label):
    """Factory function to create a PluginTemplateExtension class for a given model."""

    class DynamicDocumentList(PluginTemplateExtension):
        models = [model_label]

        def _get_documents(self):
            obj = self.context['object']
            ct = ContentType.objects.get_for_model(obj)
            return Document.objects.filter(content_type=ct, object_id=obj.pk)

        def _get_return_url(self):
            return self.context['object'].get_absolute_url()

        def _render_panel(self):
            obj = self.context['object']
            ct = ContentType.objects.get_for_model(obj)
            return self.render('netbox_documents/document_include.html', extra_context={
                'documents': self._get_documents(),
                'content_type_id': ct.pk,
                'return_url': self._get_return_url(),
            })

        def left_page(self):
            if plugin_settings.get('documents_location', 'left') == 'left':
                return self._render_panel()
            return ""

        def right_page(self):
            if plugin_settings.get('documents_location', 'left') == 'right':
                return self._render_panel()
            return ""

    DynamicDocumentList.__name__ = f'DocumentList_{model_label.replace(".", "_")}'
    DynamicDocumentList.__qualname__ = DynamicDocumentList.__name__
    return DynamicDocumentList


template_extensions = [
    _make_extension(model_label)
    for model_label in DOCUMENT_MODELS
]
