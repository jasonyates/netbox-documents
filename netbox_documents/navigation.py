from extras.plugins import PluginMenuItem, PluginMenu, PluginMenuButton
from utilities.choices import ButtonColorChoices
from django.conf import settings

plugin_settings = settings.PLUGINS_CONFIG.get('netbox_documents', {})

if plugin_settings.get('enable_navigation_menu'):

    menuitem = []

    # Add a menu item for Site Documents if enabled
    if plugin_settings.get('enable_site_documents'):
        menuitem.append(
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
        menuitem.append(
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
        menuitem.append(
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
        menuitem.append(
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

    # If we are using NB 3.4.0+ display the new top level navigation option
    if settings.VERSION >= '3.4.0':

        menu = PluginMenu(
            label='Documents',
            groups=(
                ('Document Storage', menuitem),
            ),
            icon_class='mdi mdi-file-document-multiple'
        )

    else:

        # Fall back to pre 3.4 navigation option
        menu_items = menuitem
