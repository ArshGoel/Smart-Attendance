# Generated by Django 4.2.14 on 2025-03-29 05:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("Accounts", "0002_alter_student_profile_picture"),
    ]

    operations = [
        migrations.AlterField(
            model_name="student",
            name="profile_picture",
            field=models.ImageField(blank=True, null=True, upload_to="profile_images/"),
        ),
    ]
