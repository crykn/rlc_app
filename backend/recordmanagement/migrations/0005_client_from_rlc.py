# Generated by Django 2.2 on 2019-05-11 14:50

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0008_auto_20190411_1633'),
        ('recordmanagement', '0004_auto_20190414_1953'),
    ]

    operations = [
        migrations.AddField(
            model_name='client',
            name='from_rlc',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='client_from_rlc', to='api.Rlc'),
        ),
    ]
