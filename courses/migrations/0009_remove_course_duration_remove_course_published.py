# Generated by Django 5.0.3 on 2024-03-11 06:30

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0008_course_duration_course_published_usercourse'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='course',
            name='duration',
        ),
        migrations.RemoveField(
            model_name='course',
            name='published',
        ),
    ]