# Generated by Django 5.2 on 2025-05-10 04:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0007_tag_alter_task_options_remove_task_created_task_tags'),
    ]

    operations = [
        migrations.AddField(
            model_name='task',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='task_images/', verbose_name='Изображение'),
        ),
    ]
