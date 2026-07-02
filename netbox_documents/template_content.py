from django.apps import apps
from django.contrib.contenttypes.models import ContentType
from netbox.plugins import PluginTemplateExtension
from django.conf import settings
from .models import Document, get_allowed_doc_types

plugin_settings = settings.PLUGINS_CONFIG.get('netbox_documents', {})


def _get_registered_models():
    """
    Discover all models that have a detail view (get_absolute_url).
    This allows documents to be attached to any NetBox model automatically.
    """
    model_labels = []
    for model in apps.get_models():
        if hasattr(model, 'get_absolute_url'):
            label = f'{model._meta.app_label}.{model._meta.model_name}'
            model_labels.append(label)
    return model_labels


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

            if not get_allowed_doc_types(ct.pk):
                return ''

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
    _make_extension(label)
    for label in _get_registered_models()
]
