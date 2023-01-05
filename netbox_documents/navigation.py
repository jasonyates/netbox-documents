from extras.plugins import PluginMenuItem, PluginMenu, PluginMenuButton
from utilities.choices import ButtonColorChoices
from django.conf import settings

plugin_settings = settings.PLUGINS_CONFIG.get('netbox_documents', {})

if plugin_settings.get('enable_navigation_menu'):

    menu = []

    # Add a menu item for Site Documents if enabled
    if plugin_settings.get('enable_site_documents'):
        menu.append(
            PluginMenuItem(
                link='plugins:netbox_documents:sitedocument_list',
                link_text='Site Documents',
                buttons=[PluginMenuButton(
                    link='plugins:netbox_documents:sitedocument_add',
                    title='Add',
                    icon_class='mdi mdi-plus-thick',
                    color=ButtonColorChoices.GREEN
                )]
            )
        )

    # Add a menu item for Device Documents if enabled
    if plugin_settings.get('enable_device_documents'):
        menu.append(
            PluginMenuItem(
                link='plugins:netbox_documents:devicedocument_list',
                link_text='Device Documents',
                buttons=[PluginMenuButton(
                    link='plugins:netbox_documents:devicedocument_add',
                    title='Add',
                    icon_class='mdi mdi-plus-thick',
                    color=ButtonColorChoices.GREEN
                )]
            )
        )
    
    # Add a menu item for Device Documents if enabled
    if plugin_settings.get('enable_device_type_documents'):
        menu.append(
            PluginMenuItem(
                link='plugins:netbox_documents:devicetypedocument_list',
                link_text='Device Type Documents',
                buttons=[PluginMenuButton(
                    link='plugins:netbox_documents:devicetypedocument_add',
                    title='Add',
                    icon_class='mdi mdi-plus-thick',
                    color=ButtonColorChoices.GREEN
                )]
            )
        )

    # Add a menu item for Circuit Documents if enabled
    if plugin_settings.get('enable_circuit_documents'):
        menu.append(
            PluginMenuItem(
                link='plugins:netbox_documents:circuitdocument_list',
                link_text='Circuit Documents',
                buttons=[PluginMenuButton(
                    link='plugins:netbox_documents:circuitdocument_add',
                    title='Add',
                    icon_class='mdi mdi-plus-thick',
                    color=ButtonColorChoices.GREEN
                )]
            )
        )

    menu = PluginMenu(
        label='Documents',
        groups=(
            ('Document Storage', menu),
        ),
        icon_class='mdi mdi-file-document-multiple'
    )
