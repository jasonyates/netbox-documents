from extras.plugins import PluginConfig

class NetboxDocuments(PluginConfig):
    name = 'netbox_documents'
    verbose_name = 'Document Storage'
    description = 'Manage site, location, circuit and device diagrams and documents in Netbox'
    version = '0.6.3'
    author = 'Jason Yates'
    author_email = 'me@jasonyates.co.uk'
    min_version = '3.5.0'
    base_url = 'documents'
    default_settings = {
        "enable_site_documents": True,
        "enable_location_documents": True,
        "enable_circuit_documents": True,
        "enable_device_documents": True,
        "enable_device_type_documents": True, 
        "enable_navigation_menu": True,
        "site_documents_location": "left",
        "location_documents_location": "left",
        "circuit_documents_location": "left",
        "device_documents_location": "left",
        "device_type_documents_location": "left", 
    }

config = NetboxDocuments
