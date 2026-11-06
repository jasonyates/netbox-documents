from netbox.plugins import PluginConfig


class NetboxDocuments(PluginConfig):
    name = 'netbox_documents'
    verbose_name = 'Document Storage'
    description = 'Attach documents and external URLs to any NetBox object'
    version = '0.8.7'
    author = 'Jason Yates'
    author_email = 'me@jasonyates.co.uk'
    min_version = '4.6.0'
    max_version = '4.7.99'
    base_url = 'documents'
    default_settings = {
        "enable_navigation_menu": True,
        "documents_location": "left",
        "custom_doc_types": [],
        "allowed_doc_types": {},
    }


config = NetboxDocuments
