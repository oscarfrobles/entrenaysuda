# Generated by Django 3.2.6 on 2021-10-07 22:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fitapp', '0009_auto_20211007_2216'),
    ]

    operations = [
        migrations.AddField(
            model_name='sesionesgoogle',
            name='activity',
            field=models.SmallIntegerField(default=1),
        ),
    ]
