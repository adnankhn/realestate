# Generated by Django 5.1.4 on 2025-01-14 07:42

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('property', '0002_propertyimage'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Shortlist',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('properties', models.ManyToManyField(related_name='shortlisted_by', to='property.property')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='shortlist', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
