# Generated by Django 4.2.3 on 2024-04-24 18:16

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('todo', '0011_artpost'),
    ]

    operations = [
        migrations.AddField(
            model_name='artpost',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='user',
            name='username',
            field=models.CharField(max_length=100, unique=True, validators=[django.core.validators.RegexValidator(code='invalid_username', message='Username must contain at least 8 characters.', regex='^.{8,}$')]),
        ),
    ]
