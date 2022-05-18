# Generated Manual by LHBL2003

import django.core.serializers.json
from django.db import migrations, models
import django.db.models.deletion
import netbox_documents.utils
import taggit.managers


class Migration(migrations.Migration):

    initial = false

    dependencies = [
        ('dcim', '0153_created_datetimefield'),
        ('circuits', '0034_created_datetimefield'),
        ('extras', '0072_created_datetimefield'),
    ]

    operations = [
        migrations.CreateModel(
            name='DeviceTypeDocument',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False)),
                ('created', models.DateTimeField(auto_now_add=True, null=True)),
                ('last_updated', models.DateTimeField(auto_now=True, null=True)),
                ('custom_field_data', models.JSONField(blank=True, default=dict, encoder=django.core.serializers.json.DjangoJSONEncoder)),
                ('name', models.CharField(blank=True, max_length=100)),
                ('document', models.FileField(upload_to=netbox_documents.utils.file_upload)),
                ('document_type', models.CharField(max_length=30)),
                ('comments', models.TextField(blank=True)),
                ('device_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='documents', to='dcim.device-types')),
                ('tags', taggit.managers.TaggableManager(through='extras.TaggedItem', to='extras.Tag')),
            ],
            options={
                'ordering': ('name',),
            },
        ),
    ]
