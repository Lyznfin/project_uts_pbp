# Generated by Django 5.0.3 on 2024-03-18 14:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0015_alter_course_title_completedusersection'),
    ]

    operations = [
        migrations.AlterField(
            model_name='coursesection',
            name='section',
            field=models.CharField(max_length=100),
        ),
    ]
