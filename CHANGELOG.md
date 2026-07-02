# Changelog

## 0.8.3 (2026-07-02)

* Fix InconsistentMigrationHistory errors when upgrading NetBox by removing `__latest__` migration dependencies - PR #102 (Thanks @tacerus) (Fixes #98, #103)
* Fix exception on Add Document when `allowed_doc_types` is configured - PR #96 (Thanks @shumbashi) (Fixes #92)
* Skip rendering the documents panel when a model has no allowed document types - PR #99 (Thanks @tacerus)
* Restore the Add button in the sidebar and in the main Documents page - PR #97 (Thanks @a084ed22)
* Fix contributing/test instructions - PR #100 (Thanks @tacerus)

## 0.8.2 (2026-02-13)

* Fix stale ContentType entries from old per-model document tables causing ProtectedError during NetBox upgrades
* Migrate changelog (ObjectChange) entries to reference the unified Document model during data migration

## 0.8.1 (2026-02-13)

* Documents can now be attached to any NetBox model, not just the original 8 hardcoded models
* Add API root view name

## 0.7.4 (2025-07-11)

* Fix permissions to allow plugin to be visible for non-superadmin users

## 0.7.3 (2025-05-06)

* Support for NetBox 4.3

## 0.7.2 (2025-04-8)

* Adds support for Module Type's - PR #73 (Thanks @BartZimmo)
* Adds additional doc types
* Rename Wireless doc type to remove reference to Ekahau
* Add navigation permissions to prevent users not logged in from seeing document navigation (Fixes #66)

## 0.7.1 (2024-06-19)

* Adds support for Netbox 4.2 - PR #71 (Thanks @a084ed22)

## 0.7.0 (2024-06-19)

* Adds support for Netbox 4.0

## 0.6.4 (2024-04-17)

* Add documents for Virtual Machines - PR 54 (Thanks @felbinger)
* Add documents for Circuit Providers

## 0.6.3 (2023-11-21)

* Fix requirements include on install
  
## 0.6.2 (2023-11-20)

* Improve Location Model adding "site" field to the model - PR 44
* Adding base64 document handling to API serializer - PR 40
* Extended max URL size to 255 chars
* Added template tags for plugin helpers

## 0.6.1 (2023-11-08)

* Add Location Model

## 0.6.0 (2023-04-28)

* Fixes support for Netbox 3.5

## 0.5.0 (2023-01-24)

* Fix API Filtersets
* Add support for storing links to external URL's
* Documentation updates

## 0.4.6 (2023-01-23)

* Added nested serializer.

## 0.4.5 (2023-01-03)

* Updated navigation for NetBox 3.4
* Added support for plugin search indexing

## 0.4.4 (2023-01-02)

* Added Device Type support
* Fix files not being deleted from disk

## 0.3.1 (2022-04-06)

* Adds help text to add/edit forms
* Updating table view to link to the document object view
* Adds button to document widget to link to the document object view
* Adds a link to the associated parent objet from the document object view
* Adds a link to uploaded document from the document object view
* Updates document_type to render as a badge on document object view and document widget

## 0.3.0 (2022-04-04)

* Initial Release
