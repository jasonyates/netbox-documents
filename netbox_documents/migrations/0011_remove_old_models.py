from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('netbox_documents', '0010_migrate_data'),
    ]

    operations = [
        migrations.DeleteModel(name='SiteDocument'),
        migrations.DeleteModel(name='LocationDocument'),
        migrations.DeleteModel(name='DeviceDocument'),
        migrations.DeleteModel(name='DeviceTypeDocument'),
        migrations.DeleteModel(name='ModuleTypeDocument'),
        migrations.DeleteModel(name='CircuitDocument'),
        migrations.DeleteModel(name='VMDocument'),
        migrations.DeleteModel(name='CircuitProviderDocument'),
    ]
