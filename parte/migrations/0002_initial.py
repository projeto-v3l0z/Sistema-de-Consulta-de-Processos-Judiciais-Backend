# Generated by Django 5.2.1 on 2025-05-30 17:42

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('parte', '0001_initial'),
        ('processo', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='parte',
            name='processo',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='partes', to='processo.processo', verbose_name='Processo'),
        ),
    ]
