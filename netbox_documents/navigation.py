from netbox.plugins import PluginMenuItem, PluginMenu, PluginMenuButton
from netbox.choices import ButtonColorChoices
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
                permissions=["netbox_documents.view_document"],
                buttons=[PluginMenuButton(
                    link='plugins:netbox_documents:sitedocument_add',
                    permissions=["netbox_documents.add_document"],
                    title='Add',
                    icon_class='mdi mdi-plus-thick',
                    color=ButtonColorChoices.GREEN
                )]
            )
        )

    # Add a menu item for Location Documents if enabled
    if plugin_settings.get('enable_location_documents'):
        menuitem.append(
            PluginMenuItem(
                link='plugins:netbox_documents:locationdocument_list',
                link_text='Location Documents',
                permissions=["netbox_documents.view_document"],
                buttons=[PluginMenuButton(
                    link='plugins:netbox_documents:locationdocument_add',
                    permissions=["netbox_documents.add_document"],
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
                permissions=["netbox_documents.view_document"],
                buttons=[PluginMenuButton(
                    link='plugins:netbox_documents:devicedocument_add',
                    permissions=["netbox_documents.add_document"],
                    title='Add',
                    icon_class='mdi mdi-plus-thick',
                    color=ButtonColorChoices.GREEN
                )]
            )
        )
    
    # Add a menu item for Device Type Documents if enabled
    if plugin_settings.get('enable_device_type_documents'):
        menuitem.append(
            PluginMenuItem(
                link='plugins:netbox_documents:devicetypedocument_list',
                link_text='Device Type Documents',
                permissions=["netbox_documents.view_document"],
                buttons=[PluginMenuButton(
                    link='plugins:netbox_documents:devicetypedocument_add',
                    permissions=["netbox_documents.add_document"],
                    title='Add',
                    icon_class='mdi mdi-plus-thick',
                    color=ButtonColorChoices.GREEN
                )]
            )
        )

    # Add a menu item for Module Type Documents if enabled
    if plugin_settings.get('enable_module_type_documents'):
        menuitem.append(
            PluginMenuItem(
                link='plugins:netbox_documents:moduletypedocument_list',
                link_text='Module Type Documents',
                permissions=["netbox_documents.view_document"],
                buttons=[PluginMenuButton(
                    link='plugins:netbox_documents:moduletypedocument_add',
                    permissions=["netbox_documents.add_document"],
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
                permissions=["netbox_documents.view_document"],
                buttons=[PluginMenuButton(
                    link='plugins:netbox_documents:circuitdocument_add',
                    permissions=["netbox_documents.add_document"],
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

    # Add a menu item for VM Documents if enabled
    if plugin_settings.get('enable_vm_documents'):
        menuitem.append(
            PluginMenuItem(
                link='plugins:netbox_documents:vmdocument_list',
                link_text='Virtual Machine Documents',
                permissions=["netbox_documents.view_document"],
                buttons=[PluginMenuButton(
                    link='plugins:netbox_documents:vmdocument_add',
                    permissions=["netbox_documents.add_document"],
                    title='Add',
                    icon_class='mdi mdi-plus-thick',
                    color=ButtonColorChoices.GREEN
                )]
            )
        )

    # Add a menu item for Circuit Provider Documents if enabled
    if plugin_settings.get('enable_circuit_provider_documents'):
        menuitem.append(
            PluginMenuItem(
                link='plugins:netbox_documents:circuitproviderdocument_list',
                link_text='Circuit Provider Documents',
                permissions=["netbox_documents.view_document"],
                buttons=[PluginMenuButton(
                    link='plugins:netbox_documents:circuitproviderdocument_add',
                    permissions=["netbox_documents.add_document"],
                    title='Add',
                    icon_class='mdi mdi-plus-thick',
                    color=ButtonColorChoices.GREEN
                )]
            )
        )

    else:

        # Fall back to pre 3.4 navigation option
        menu_items = menuitem
