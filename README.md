# Netbox Documents Plugin

A plugin designed to faciliate the storage of site, circuit, device type and device specific documents within [NetBox](https://github.com/netbox-community/netbox)

## Features

* Store documents against the following NetBox models:
   - Circuits
   - Devices
   - Device Types
   - Sites
   - Locations
   - Virtual Machines
   - Circuit Providers

* Upload documents to your NetBox media/ folder or other Django supported storage method e.g. S3
* Supports a wide array of common file types (bmp, gif, jpeg, jpg, png, pdf, txt, doc, docx, xls, xlsx, xlsm)
* Store links to external URL's to save duplication of remote documents


## Compatibility

| NetBox Version | Plugin Version |
|----------------|----------------|
|     3.6+       |      0.6.4     |
|     3.5.x      |      0.6.0     |
| 3.3.x - 3.4.x  |      0.5.1     |


## Installation

A working installation of Netbox 3.3+ is required. 3.6+ is recommended. **NOTE: Netbox 3.5 introduced breaking changes for plugins, please use the correct plugin version for your netbox install.**

#### Package Installation from PyPi

Activate your virtual env and install via pip:

```
$ source /opt/netbox/venv/bin/activate
(venv) $ pip install netbox-documents
```

To ensure the Netbox Documents plugin is automatically re-installed during future upgrades, add the package to your `local_requirements.txt` :

```no-highlight
# echo netbox-documents >> local_requirements.txt
```

#### Enable the Plugin

In the Netbox `configuration.py` configuration file add or update the PLUGINS parameter, adding `netbox_documents`:

```python
PLUGINS = [
    'netbox_documents',
]
```

(Optional) Add or update a PLUGINS_CONFIG parameter in `configuration.py` to configure plugin settings. Options shown below are the configured defaults:

```python
PLUGINS_CONFIG = {
     'netbox_documents': {
         # Enable the management of site specific documents (True/False)
         'enable_site_documents': True,
         # Enable the management of location specific documents (True/False)
         'enable_location_documents': True,
         # Enable the management of circuit specific documents (True/False)
         'enable_circuit_documents': True,
         # Enable the management of device specific documents (True/False)
         'enable_device_documents': True,
         # Enable the management of device type specific documents (True/False)
         'enable_device_type_documents': True,
         # Enable the global menu options (True/False)   
         'enable_navigation_menu': True,
         # Location to inject the document widget in the site view (left/right)
         'site_documents_location': 'left',
         # Location to inject the document widget in the location view (left/right)
         'location_documents_location': 'left',
         # Location to inject the document widget in the device view (left/right
         'device_documents_location': 'left',
         # Location to inject the document type widget in the device type view (left/right
         'device_type_documents_location': 'left',
         # Location to inject the document widget in the device view (left/right
         'circuit_documents_location': 'left'
     }
}

```

(Optional) Add or replace the built-in Document Type choices via Netbox's [`FIELD_CHOICES`](https://netbox.readthedocs.io/en/feature/configuration/optional-settings/#field_choices) configuration parameter:

The colours that can be used are listed in the Netbox CSS netbox-light.css:

(https://github.com/netbox-community/netbox/blob/develop/netbox/project-static/dist/netbox-light.css)

The bg- must not be specified in the configuration.
Here are a few examples from the CSS:

* bg-indigo = #6610f2 --> 'indigo'
* bg-blue = #0d6efd --> 'blue'
* bg-purple = #6f42c1 --> 'purple'
* bg-pink = #d63384 --> 'pink'
* bg-red = #dc3545 --> 'red'
* bg-orange = #fd7e14 --> 'orange'
* bg-yellow = #ffc107 --> 'yellow'
* bg-green = #198754 --> 'green'
* bg-teal = #20c997 --> 'teal'
* bg-cyan = #0dcaf0 --> 'cyan'
* bg-gray = #adb5bd --> 'gray'
* bg-black = #000 --> 'black'
* bg-white --> 'white'

```python
FIELD_CHOICES = {
    'netbox_documents.DocTypeChoices.site+': (
        ('mydocument', 'My Custom Site Document Type', 'green'),
    ),
    'netbox_documents.DocTypeChoices.location+': (
        ('mydocument', 'My Custom Location Document Type', 'green'),
    ),
    'netbox_documents.DocTypeChoices.device+': (
        ('mydocument', 'My Custom Device Document Type', 'green'),
    ),
    'netbox_documents.DocTypeChoices.devicetype+': (
        ('mydocument', 'My Custom Device Type Document Type', 'green'),
    ),
    'netbox_documents.DocTypeChoices.circuit+': (
        ('mydocument', 'My Custom Circuit Document Type', 'green'),
    )
}
```

#### Apply Database Migrations

Apply database migrations with Netbox `manage.py`:

```
(venv) $ python manage.py migrate
```

#### Restart Netbox

Restart the Netbox service to apply changes:

```
sudo systemctl restart netbox
```

#### Re-index Netbox search index (Upgrade to 3.4 only)

If you are upgrading from Netbox 3.3 or above to Netbox 3.4, any previously inserted documents may not show up in the new search feature. To resolve this, re-index the plugin:

```
(venv) $ python manage.py reindex netbox_documents
```

### Screenshots

![Site Document View](docs/img/siteview.png)
![Add Circuit Document](docs/img/addcircuit.png)
![Site Document List](docs/img/sitedocuments.png)
![Device Document List](docs/img/devicedocuments.png)
![Device Type Document](docs/img/devicetypedocuments.png)
![Device Type Document List](docs/img/devicetypedocumentsList.png)
