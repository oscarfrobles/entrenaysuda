# Generated by Django 3.2.6 on 2021-10-07 22:16

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('fitapp', '0008_alter_calendario_weight'),
    ]

    operations = [
        migrations.CreateModel(
            name='SesionesGoogle',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('id_google', models.CharField(max_length=200, unique=True)),
                ('name', models.CharField(blank=True, max_length=200)),
                ('description', models.CharField(blank=True, max_length=200)),
                ('startTimeMillis', models.IntegerField()),
                ('endTimeMillis', models.IntegerField()),
                ('application', models.CharField(blank=True, max_length=200)),
                ('user_google', models.CharField(blank=True, max_length=200)),
            ],
        ),
        migrations.AddField(
            model_name='calendario',
            name='session_google',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='fitapp.sesionesgoogle'),
        ),
    ]
