# Generated by Django 5.0.3 on 2024-03-26 16:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('playlists', '0002_playlist_user'),
        ('songs', '0004_rename_id_song_song_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='playlist',
            name='songs',
            field=models.ManyToManyField(blank=True, related_name='playlist_songs', to='songs.song'),
        ),
    ]
