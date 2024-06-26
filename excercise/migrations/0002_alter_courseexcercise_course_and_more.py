# Generated by Django 5.0.3 on 2024-04-29 09:33

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0017_remove_usercourse_completed_section'),
        ('excercise', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterField(
            model_name='courseexcercise',
            name='course',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='excercises', to='courses.course'),
        ),
        migrations.AlterField(
            model_name='excerciseresult',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_excercise', to=settings.AUTH_USER_MODEL),
        ),
    ]
