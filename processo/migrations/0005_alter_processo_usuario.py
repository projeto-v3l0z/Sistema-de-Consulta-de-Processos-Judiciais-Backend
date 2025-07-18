# Generated by Django 5.2.1 on 2025-06-25 23:19

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('processo', '0004_alter_processo_usuario'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterField(
            model_name='processo',
            name='usuario',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='processos', to=settings.AUTH_USER_MODEL, verbose_name='Usuário Responsável'),
        ),
    ]
