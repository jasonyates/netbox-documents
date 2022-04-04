from extras.plugins import PluginTemplateExtension
from django.conf import settings
from .models import SiteDocument, DeviceDocument, CircuitDocument

plugin_settings = settings.PLUGINS_CONFIG.get('netbox_documents', {})

class SiteDocumentList(PluginTemplateExtension):
    model = 'dcim.site'

    def left_page(self):

        if plugin_settings.get('enable_site_documents') and plugin_settings.get('site_documents_location') == 'left':

            return self.render('netbox_documents/sitedocument_include.html', extra_context={
                'site_documents': SiteDocument.objects.filter(site=self.context['object']),
            })

        else:
            return ""

    def right_page(self):

        if plugin_settings.get('enable_site_documents') and plugin_settings.get('site_documents_location') == 'right':

            return self.render('netbox_documents/sitedocument_include.html', extra_context={
                'site_documents': SiteDocument.objects.filter(site=self.context['object']),
            })

        else:
            return ""


class DeviceDocumentList(PluginTemplateExtension):
    model = 'dcim.device'

    def left_page(self):

        if plugin_settings.get('enable_device_documents') and plugin_settings.get('device_documents_location') == 'left':

            return self.render('netbox_documents/devicedocument_include.html', extra_context={
                'device_documents': DeviceDocument.objects.filter(device=self.context['object']),
            })

        else:
            return ""

    def right_page(self):

        if plugin_settings.get('enable_device_documents') and plugin_settings.get('device_documents_location') == 'right':

            return self.render('netbox_documents/devicedocument_include.html', extra_context={
                'device_documents': DeviceDocument.objects.filter(device=self.context['object']),
            })

        else:
            return ""


class CircuitDocumentList(PluginTemplateExtension):
    model = 'circuits.circuit'

    def left_page(self):

        if plugin_settings.get('enable_circuit_documents') and plugin_settings.get('circuit_documents_location') == 'left':

            return self.render('netbox_documents/circuitdocument_include.html', extra_context={
                'circuit_documents': CircuitDocument.objects.filter(circuit=self.context['object']),
            })

        else:
            return ""

    def right_page(self):

        if plugin_settings.get('enable_circuit_documents') and plugin_settings.get('circuit_documents_location') == 'right':

            return self.render('netbox_documents/circuitdocument_include.html', extra_context={
                'circuit_documents': CircuitDocument.objects.filter(circuit=self.context['object']),
            })

        else:
            return ""

template_extensions = [SiteDocumentList, DeviceDocumentList, CircuitDocumentList]