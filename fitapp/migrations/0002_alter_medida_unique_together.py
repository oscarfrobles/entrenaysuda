# Generated by Django 3.2.6 on 2021-09-15 21:56

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('fitapp', '0001_initial'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='medida',
            unique_together={('mes', 'anyo')},
        ),
    ]
