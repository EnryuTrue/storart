# Generated by Django 4.2.3 on 2024-05-17 10:42

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('todo', '0018_artpost_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='artpost',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL),
        ),
    ]
