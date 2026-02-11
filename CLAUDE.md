# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What This Is

A NetBox plugin (`netbox-documents`) that attaches documents and external URLs to any NetBox object. It uses a single `Document` model with Django's ContentType framework (GenericForeignKey) to relate documents to any model. Requires NetBox 4.3+.

## Development Environment

This plugin runs inside a NetBox installation. You need a working NetBox dev environment to run migrations or tests. The plugin is installed into NetBox's virtualenv:

```bash
source /opt/netbox/venv/bin/activate
pip install -e /path/to/netbox-documents
python manage.py migrate netbox_documents
python manage.py runserver
```

## Testing

Tests use Django's TestCase framework. Run from the NetBox project directory:

```bash
python manage.py test netbox_documents
python manage.py test netbox_documents.tests.test_models          # single module
python manage.py test netbox_documents.tests.test_models.DocumentModelTest  # single class
python manage.py test netbox_documents.tests.test_models.DocumentModelTest.test_create_document_with_file  # single test
```

## Building for PyPI

```bash
pip install build twine
python -m build
twine upload dist/*
```

## Architecture

The plugin follows NetBox's plugin conventions. All code lives in `netbox_documents/`.

**Core model** (`models.py`): Single `Document` model with GenericForeignKey (`content_type` + `object_id`). `DocTypeChoices` is built dynamically at import time from built-in types + user-configured `custom_doc_types`. The `get_allowed_doc_types()` helper resolves per-model type filtering from plugin settings.

**How documents appear on object pages** (`template_content.py`): A factory function creates a `PluginTemplateExtension` class for each supported model (Site, Device, Circuit, etc.). Each extension renders `document_include.html` on the object's detail page. The panel placement (left/right) is controlled by the `documents_location` setting.

**How documents are created**: Documents are always added from an object's detail page, never from a standalone form. The "Add Document" link passes `?content_type=X&object_id=Y` as URL params. The view's `alter_object()` method reads these params and sets them on the instance before the form renders. The form itself (`forms.py`) only contains document-specific fields (name, file/URL, type, comments, tags) -- not the object association.

**API** (`api/`): Single `DocumentViewSet` at `/api/plugins/netbox-documents/documents/`. Uses `ContentTypeField` for the `content_type` field and accepts `object_id` as an integer.

**Configuration** (`__init__.py`): Plugin settings include `documents_location` (left/right panel), `custom_doc_types` (user-defined types as `(value, label, color)` tuples), and `allowed_doc_types` (per-model type filtering with `__all__` fallback key).

## Key Patterns

- Views extend NetBox's generic views (`ObjectView`, `ObjectListView`, `ObjectEditView`, `ObjectDeleteView`, `BulkDeleteView`) which handle permissions automatically.
- Template buttons in `document_include.html` are gated with `{% if perms.netbox_documents.* %}` checks.
- The `file_upload()` utility in `utils.py` generates upload paths using `object_id` as a prefix.
- Navigation menu (`navigation.py`) is conditionally created based on the `enable_navigation_menu` setting.
- Search index (`search.py`) registers `Document` for NetBox's global search.

## Dependencies

Runtime: `drf_extra_fields>=3.7.0` (provides `Base64FileField` for API file uploads)
