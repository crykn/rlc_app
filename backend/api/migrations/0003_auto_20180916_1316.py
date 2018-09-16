# Generated by Django 2.0.3 on 2018-09-16 13:16

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0002_auto_20180916_1259'),
    ]

    operations = [
        migrations.DeleteModel(
            name='CanViewRecord',
        ),
        migrations.RemoveField(
            model_name='client',
            name='origin_country',
        ),
        migrations.RemoveField(
            model_name='record',
            name='client',
        ),
        migrations.RemoveField(
            model_name='record',
            name='creator',
        ),
        migrations.RemoveField(
            model_name='record',
            name='from_rlc',
        ),
        migrations.RemoveField(
            model_name='record',
            name='tagged',
        ),
        migrations.RemoveField(
            model_name='record',
            name='working_on_record',
        ),
        migrations.DeleteModel(
            name='Client',
        ),
        migrations.DeleteModel(
            name='OriginCountry',
        ),
        migrations.DeleteModel(
            name='Record',
        ),
        migrations.DeleteModel(
            name='RecordTag',
        ),
    ]
