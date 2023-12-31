from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0007_delete_contact_rename_categotry_item_category'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item',
            name='published_date',
            field=models.DateTimeField(null=True, blank=True),
        ),
    ]
