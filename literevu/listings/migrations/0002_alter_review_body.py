# Generated by Django 3.2.4 on 2025-03-17 18:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('listings', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='review',
            name='body',
            field=models.TextField(blank=True, help_text='Le contenu de la critique', max_length=8192),
        ),
    ]
