from extras.plugins import PluginMenuItem
from django.conf import settings

plugin_settings = settings.PLUGINS_CONFIG.get('netbox_documents', {})

if plugin_settings.get('enable_navigation_menu'):

    menu_items = []

    # Add a menu item for Site Documents if enabled
    if plugin_settings.get('enable_site_documents'):
        menu_items.append(PluginMenuItem(
            link='plugins:netbox_documents:sitedocument_list',
            link_text='Site Documents'
        ))

    # Add a menu item for Device Documents if enabled
    if plugin_settings.get('enable_device_documents'):
        menu_items.append(
            PluginMenuItem(
                link='plugins:netbox_documents:devicedocument_list',
                link_text='Device Documents'
            )
        )

    # Add a menu item for Circuit Documents if enabled
    if plugin_settings.get('enable_circuit_documents'):
        menu_items.append(
            PluginMenuItem(
                link='plugins:netbox_documents:circuitdocument_list',
                link_text='Circuit Documents'
            )
        )