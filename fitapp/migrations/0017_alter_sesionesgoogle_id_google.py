# Generated by Django 3.2.6 on 2021-10-13 18:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fitapp', '0016_auto_20211013_1302'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sesionesgoogle',
            name='id_google',
            field=models.CharField(max_length=200),
        ),
    ]
