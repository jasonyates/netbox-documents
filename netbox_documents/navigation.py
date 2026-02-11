from netbox.plugins import PluginMenuItem, PluginMenu, PluginMenuButton
from netbox.choices import ButtonColorChoices
from django.conf import settings

plugin_settings = settings.PLUGINS_CONFIG.get('netbox_documents', {})

if plugin_settings.get('enable_navigation_menu'):

    menuitem = [
        PluginMenuItem(
            link='plugins:netbox_documents:document_list',
            link_text='Documents',
            permissions=["netbox_documents.view_document"],
        )
    ]

    menu = PluginMenu(
        label='Documents',
        groups=(
            ('Document Storage', menuitem),
        ),
        icon_class='mdi mdi-file-document-multiple'
    )
