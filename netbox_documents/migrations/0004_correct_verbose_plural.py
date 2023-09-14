from django.db import migrations

class Migration(migrations.Migration):

    dependencies = [
        ("netbox_documents", "0003_alter_circuitdocument_options_and_more"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="circuitdocument",
            options={
                "verbose_name_plural": "Circuit Documents",
            },
        ),
        migrations.AlterModelOptions(
            name="devicedocument",
            options={
                "verbose_name_plural": "Device Documents",
            },
        ),
        migrations.AlterModelOptions(
            name="devicetypedocument",
            options={
                "verbose_name_plural": "Device Type Documents",
            },
        ),
        migrations.AlterModelOptions(
            name="sitedocument",
            options={
                "verbose_name_plural": "Site Documents",
            },
        )
    ]
