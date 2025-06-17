from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ReportsApp', '0002_category_location_itemreport_category_old_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='itemreport',
            name='category_old',
        ),
        migrations.RemoveField(
            model_name='itemreport',
            name='location_old',
        ),
    ] 