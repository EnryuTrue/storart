# Generated by Django 4.2.3 on 2023-07-30 10:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('todo', '0002_user_phone'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='date_joined',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
    ]
