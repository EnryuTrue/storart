# Generated by Django 4.2.3 on 2024-05-15 16:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('todo', '0014_conversation_alter_user_username_message_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='artpost',
            name='price',
            field=models.IntegerField(default=150),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='artpost',
            name='title',
            field=models.CharField(default='gege akutami', max_length=20),
            preserve_default=False,
        ),
    ]
