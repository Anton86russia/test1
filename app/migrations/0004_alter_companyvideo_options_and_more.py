# Generated by Django 5.2 on 2025-05-06 19:02

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0003_companyvideo'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='companyvideo',
            options={'ordering': ['-uploaded_at'], 'verbose_name': 'Видео компании', 'verbose_name_plural': 'Видео компании'},
        ),
        migrations.RenameField(
            model_name='companyvideo',
            old_name='created_at',
            new_name='uploaded_at',
        ),
        migrations.RemoveField(
            model_name='companyvideo',
            name='added_by',
        ),
        migrations.RemoveField(
            model_name='companyvideo',
            name='video_url',
        ),
        migrations.AddField(
            model_name='companyvideo',
            name='preview_image',
            field=models.ImageField(blank=True, help_text='Постер для видео (опционально)', upload_to='about/video_previews/'),
        ),
        migrations.AddField(
            model_name='companyvideo',
            name='video_file',
            field=models.FileField(default='', help_text='Поддерживаемые форматы: MP4, WebM, Ogg', upload_to='about/videos/', validators=[django.core.validators.FileExtensionValidator(allowed_extensions=['mp4', 'webm', 'ogg'])]),
            preserve_default=False,
        ),
    ]
