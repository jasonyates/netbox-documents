from django.db import migrations


# Mapping: (old_model_name, fk_field_name, content_type_app_label, content_type_model)
OLD_MODELS = [
    ('SiteDocument', 'site_id', 'dcim', 'site'),
    ('LocationDocument', 'location_id', 'dcim', 'location'),
    ('DeviceDocument', 'device_id', 'dcim', 'device'),
    ('DeviceTypeDocument', 'device_type_id', 'dcim', 'devicetype'),
    ('ModuleTypeDocument', 'module_type_id', 'dcim', 'moduletype'),
    ('CircuitDocument', 'circuit_id', 'circuits', 'circuit'),
    ('VMDocument', 'vm_id', 'virtualization', 'virtualmachine'),
    ('CircuitProviderDocument', 'provider_id', 'circuits', 'provider'),
]


def _get_object_change_model(apps):
    """ObjectChange moved from extras to core across NetBox versions."""
    for app_label in ('core', 'extras'):
        try:
            return apps.get_model(app_label, 'ObjectChange')
        except LookupError:
            continue
    return None


def migrate_forward(apps, schema_editor):
    Document = apps.get_model('netbox_documents', 'Document')
    ContentType = apps.get_model('contenttypes', 'ContentType')
    TaggedItem = apps.get_model('extras', 'TaggedItem')
    ObjectChange = _get_object_change_model(apps)

    # Use get_or_create for the Document ContentType since Django creates
    # ContentType records via post_migrate, not between migrations.
    doc_ct, _ = ContentType.objects.get_or_create(app_label='netbox_documents', model='document')

    for old_model_name, fk_field, ct_app, ct_model in OLD_MODELS:
        OldModel = apps.get_model('netbox_documents', old_model_name)
        target_ct, _ = ContentType.objects.get_or_create(app_label=ct_app, model=ct_model)
        old_ct, _ = ContentType.objects.get_or_create(app_label='netbox_documents', model=old_model_name.lower())

        for old_doc in OldModel.objects.all():
            new_doc = Document.objects.create(
                name=old_doc.name,
                document=old_doc.document.name if old_doc.document else '',
                external_url=old_doc.external_url,
                document_type=old_doc.document_type,
                comments=old_doc.comments,
                content_type=target_ct,
                object_id=getattr(old_doc, fk_field),
                custom_field_data=old_doc.custom_field_data,
            )

            # Preserve original timestamps (auto_now/auto_now_add ignore provided values in create())
            Document.objects.filter(pk=new_doc.pk).update(
                created=old_doc.created,
                last_updated=old_doc.last_updated,
            )

            # Migrate tags: re-point TaggedItem entries to the new Document
            TaggedItem.objects.filter(
                content_type=old_ct,
                object_id=old_doc.pk,
            ).update(
                content_type=doc_ct,
                object_id=new_doc.pk,
            )

            # Migrate changelog entries to reference the new Document record
            if ObjectChange is not None:
                ObjectChange.objects.filter(
                    changed_object_type=old_ct,
                    changed_object_id=old_doc.pk,
                ).update(
                    changed_object_type=doc_ct,
                    changed_object_id=new_doc.pk,
                )


def migrate_backward(apps, schema_editor):
    """Reverse migration: move data back from Document to old tables."""
    Document = apps.get_model('netbox_documents', 'Document')
    ContentType = apps.get_model('contenttypes', 'ContentType')
    TaggedItem = apps.get_model('extras', 'TaggedItem')

    doc_ct, _ = ContentType.objects.get_or_create(app_label='netbox_documents', model='document')

    for old_model_name, fk_field, ct_app, ct_model in OLD_MODELS:
        OldModel = apps.get_model('netbox_documents', old_model_name)
        target_ct, _ = ContentType.objects.get_or_create(app_label=ct_app, model=ct_model)
        old_ct, _ = ContentType.objects.get_or_create(app_label='netbox_documents', model=old_model_name.lower())

        for doc in Document.objects.filter(content_type=target_ct):
            kwargs = {
                'name': doc.name,
                'document': doc.document,
                'external_url': doc.external_url,
                'document_type': doc.document_type,
                'comments': doc.comments,
                'custom_field_data': doc.custom_field_data,
                fk_field: doc.object_id,
            }
            # LocationDocument needs site_id too
            if old_model_name == 'LocationDocument':
                Location = apps.get_model('dcim', 'Location')
                loc = Location.objects.get(pk=doc.object_id)
                # Try to get site_id from Location; may not exist in all NetBox versions
                if hasattr(loc, 'site_id') and loc.site_id:
                    kwargs['site_id'] = loc.site_id
                else:
                    # Fallback: use object_id 0 as placeholder (LocationDocument requires site_id)
                    kwargs['site_id'] = loc.pk

            old_doc = OldModel.objects.create(**kwargs)

            # Migrate tags back
            TaggedItem.objects.filter(
                content_type=doc_ct,
                object_id=doc.pk,
            ).update(
                content_type=old_ct,
                object_id=old_doc.pk,
            )

        # Delete migrated documents from unified table
        Document.objects.filter(content_type=target_ct).delete()


class Migration(migrations.Migration):

    dependencies = [
        ('netbox_documents', '0009_document'),
        ('contenttypes', '__latest__'),
        ('extras', '__latest__'),
        ('core', '__latest__'),
    ]

    operations = [
        migrations.RunPython(migrate_forward, migrate_backward),
    ]
