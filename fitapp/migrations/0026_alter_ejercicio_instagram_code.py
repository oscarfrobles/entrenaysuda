# Generated by Django 3.2.6 on 2021-10-29 19:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fitapp', '0025_alter_ejercicio_instagram_code'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ejercicio',
            name='instagram_code',
            field=models.TextField(blank=True, default='', help_text='Código Instagram', verbose_name='Vídeo'),
        ),
    ]
