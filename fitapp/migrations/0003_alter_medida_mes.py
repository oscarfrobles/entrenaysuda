# Generated by Django 3.2.6 on 2021-09-16 22:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fitapp', '0002_alter_medida_unique_together'),
    ]

    operations = [
        migrations.AlterField(
            model_name='medida',
            name='mes',
            field=models.IntegerField(choices=[(1, 'Enero'), (2, 'Febrero'), (3, 'Marzo'), (4, 'Abril'), (5, 'Mayo'), (6, 'Junio'), (7, 'Julio'), (8, 'Agosto'), (9, 'Septiembre'), (10, 'Octubre'), (11, 'Noviembre'), (12, 'Diciembre')], default=9, verbose_name='Mes'),
        ),
    ]
