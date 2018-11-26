# Generated by Django 2.1.2 on 2018-11-22 16:56

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('recordmanagement', '0005_recorddocument_tagged'),
    ]

    operations = [
        migrations.CreateModel(
            name='RecordMessage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('message', models.CharField(max_length=4096)),
                ('record', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='record_messages', to='recordmanagement.Record')),
                ('sender', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='record_messages_sent', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
