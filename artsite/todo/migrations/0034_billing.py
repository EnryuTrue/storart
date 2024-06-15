# Generated by Django 4.2.3 on 2024-05-25 20:25

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('todo', '0033_cart_cartitem'),
    ]

    operations = [
        migrations.CreateModel(
            name='Billing',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30)),
                ('street_address', models.CharField(max_length=50)),
                ('city', models.CharField(max_length=60)),
                ('state', models.CharField(max_length=30)),
                ('zipcode', models.CharField(max_length=5)),
                ('country', models.CharField(max_length=50)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
