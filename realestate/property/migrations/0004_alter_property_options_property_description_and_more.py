# Generated by Django 5.1.4 on 2025-01-14 19:16

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('property', '0003_shortlist'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='property',
            options={'ordering': ['-created_at'], 'verbose_name': 'Property', 'verbose_name_plural': 'Properties'},
        ),
        migrations.AddField(
            model_name='property',
            name='description',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddIndex(
            model_name='property',
            index=models.Index(fields=['price'], name='property_pr_price_b1d594_idx'),
        ),
        migrations.AddIndex(
            model_name='property',
            index=models.Index(fields=['city'], name='property_pr_city_650e24_idx'),
        ),
        migrations.AddIndex(
            model_name='property',
            index=models.Index(fields=['status'], name='property_pr_status_b98bf4_idx'),
        ),
        migrations.AddIndex(
            model_name='property',
            index=models.Index(fields=['created_at'], name='property_pr_created_7a89fc_idx'),
        ),
        migrations.AddIndex(
            model_name='property',
            index=models.Index(fields=['city', 'status', 'price'], name='property_search_idx'),
        ),
    ]
