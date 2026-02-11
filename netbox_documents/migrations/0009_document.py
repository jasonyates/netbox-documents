import django.db.models.deletion
import netbox_documents.utils
import taggit.managers
import utilities.json
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '__latest__'),
        ('extras', '__latest__'),
        ('netbox_documents', '0008_moduletypedocument'),
    ]

    operations = [
        migrations.CreateModel(
            name='Document',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False)),
                ('created', models.DateTimeField(auto_now_add=True, null=True)),
                ('last_updated', models.DateTimeField(auto_now=True, null=True)),
                ('custom_field_data', models.JSONField(blank=True, default=dict, encoder=utilities.json.CustomFieldJSONEncoder)),
                ('name', models.CharField(blank=True, max_length=100)),
                ('document', models.FileField(blank=True, upload_to=netbox_documents.utils.file_upload)),
                ('external_url', models.URLField(blank=True, max_length=255)),
                ('document_type', models.CharField(max_length=30)),
                ('comments', models.TextField(blank=True)),
                ('content_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='contenttypes.contenttype')),
                ('object_id', models.PositiveBigIntegerField()),
                ('tags', taggit.managers.TaggableManager(through='extras.TaggedItem', to='extras.Tag')),
            ],
            options={
                'verbose_name': 'Document',
                'verbose_name_plural': 'Documents',
                'ordering': ('name',),
                'indexes': [
                    models.Index(fields=['content_type', 'object_id'], name='netbox_docu_content_b53857_idx'),
                ],
            },
        ),
    ]
