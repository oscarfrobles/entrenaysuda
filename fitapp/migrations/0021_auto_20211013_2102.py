# Generated by Django 3.2.6 on 2021-10-13 21:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fitapp', '0020_alter_sesionesgoogle_id_google'),
    ]

    operations = [
        migrations.AlterField(
            model_name='calendario',
            name='session_google',
            field=models.ManyToManyField(blank=True, null=True, to='fitapp.SesionesGoogle'),
        ),
        migrations.AlterField(
            model_name='sesionesgoogle',
            name='id_google',
            field=models.CharField(max_length=200, unique=True),
        ),
    ]
