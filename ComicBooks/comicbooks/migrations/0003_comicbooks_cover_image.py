# Generated by Django 5.0 on 2025-05-07 17:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('comicbooks', '0002_alter_comicbooks_grade'),
    ]

    operations = [
        migrations.AddField(
            model_name='comicbooks',
            name='cover_image',
            field=models.ImageField(blank=True, null=True, upload_to='comic_covers/'),
        ),
    ]
