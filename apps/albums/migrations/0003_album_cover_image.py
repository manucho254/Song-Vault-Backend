# Generated by Django 5.0.3 on 2024-03-23 18:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('albums', '0002_rename_artist_album_album_artist'),
    ]

    operations = [
        migrations.AddField(
            model_name='album',
            name='cover_image',
            field=models.ImageField(default=True, upload_to='album_covers'),
            preserve_default=False,
        ),
    ]