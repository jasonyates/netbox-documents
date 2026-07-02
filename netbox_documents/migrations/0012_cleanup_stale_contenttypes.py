from django.db import migrations, models

import netbox_documents.models

# The old per-model document types removed in migration 0011.
OLD_CONTENT_TYPES = [
    'sitedocument',
    'locationdocument',
    'devicedocument',
    'devicetypedocument',
    'moduletypedocument',
    'circuitdocument',
    'vmdocument',
    'circuitproviderdocument',
]


def _get_object_change_model(apps):
    """ObjectChange moved from extras to core across NetBox versions."""
    for app_label in ('core', 'extras'):
        try:
            return apps.get_model(app_label, 'ObjectChange')
        except LookupError:
            continue
    return None


def cleanup_stale_content_types(apps, schema_editor):
    """
    Migration 0011 deleted the old per-model document tables, making their
    ContentType entries stale. However, two models still reference them via
    protected foreign keys:

      - ObjectChange.changed_object_type  (NetBox changelog)
      - core.ObjectType.contenttype_ptr   (NetBox's ContentType subclass)

    This prevents Django's remove_stale_contenttypes command from cleaning
    them up, causing a ProtectedError during NetBox upgrades.

    Fix: re-point ObjectChange records to the unified Document content type,
    remove the ObjectType entries, then delete the stale content types.
    """
    ContentType = apps.get_model('contenttypes', 'ContentType')

    old_cts = ContentType.objects.filter(
        app_label='netbox_documents',
        model__in=OLD_CONTENT_TYPES,
    )

    if not old_cts.exists():
        return

    old_ct_ids = list(old_cts.values_list('id', flat=True))

    doc_ct = ContentType.objects.filter(
        app_label='netbox_documents', model='document'
    ).first()

    # 1. Re-point ObjectChange records to the unified Document content type.
    #    The changed_object_id values won't match new Document PKs (the data
    #    migration assigned new IDs), but this is the same as any deleted-object
    #    changelog entry -- the record persists for audit purposes.
    #
    #    In NetBox 4.x, ObjectChange.changed_object_type is a FK to ObjectType
    #    (which inherits from ContentType), so we must ensure the Document's
    #    ObjectType entry exists before re-pointing.
    ObjectChange = _get_object_change_model(apps)
    if ObjectChange is not None:
        if doc_ct:
            # Ensure Document has an ObjectType entry (the FK target)
            try:
                ObjectType = apps.get_model('core', 'ObjectType')
                if not ObjectType.objects.filter(pk=doc_ct.id).exists():
                    ObjectType.objects.create(contenttype_ptr_id=doc_ct.id)
            except LookupError:
                pass

            ObjectChange.objects.filter(
                changed_object_type_id__in=old_ct_ids
            ).update(changed_object_type_id=doc_ct.id)
        else:
            # Shouldn't happen, but if Document CT is missing, remove the
            # changelog entries rather than leaving broken references.
            ObjectChange.objects.filter(
                changed_object_type_id__in=old_ct_ids
            ).delete()

    # 2. Remove ObjectType entries for the old content types.
    try:
        ObjectType = apps.get_model('core', 'ObjectType')
        ObjectType.objects.filter(pk__in=old_ct_ids).delete()
    except LookupError:
        pass

    # 3. Delete the stale content types themselves.
    old_cts.delete()


class Migration(migrations.Migration):

    dependencies = [
        ('netbox_documents', '0011_remove_old_models'),
    ]

    operations = [
        migrations.RunPython(
            cleanup_stale_content_types,
            migrations.RunPython.noop,
        ),
        migrations.AlterField(
            model_name='document',
            name='name',
            field=models.CharField(
                blank=True,
                help_text='(Optional) Specify a name to display for this document. If no name is specified, the filename or URL will be used.',
                max_length=100,
            ),
        ),
        migrations.AlterField(
            model_name='document',
            name='document_type',
            field=models.CharField(
                choices=netbox_documents.models.DocTypeChoices,
                max_length=30,
            ),
        ),
    ]
