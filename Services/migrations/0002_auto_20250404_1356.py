# Generated by Django 3.1.12 on 2025-04-04 08:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Services', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='attendance',
            name='id',
            field=models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
    ]
