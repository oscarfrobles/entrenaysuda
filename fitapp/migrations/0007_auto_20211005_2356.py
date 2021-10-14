# Generated by Django 3.2.6 on 2021-10-05 23:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fitapp', '0006_auto_20211005_2325'),
    ]

    operations = [
        migrations.RenameField(
            model_name='calendario',
            old_name='calorias',
            new_name='calories',
        ),
        migrations.RenameField(
            model_name='calendario',
            old_name='distancia',
            new_name='distance',
        ),
        migrations.RenameField(
            model_name='calendario',
            old_name='pasos',
            new_name='estimated_steps',
        ),
        migrations.AddField(
            model_name='calendario',
            name='steps',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='calendario',
            name='weight',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
