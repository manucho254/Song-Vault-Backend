# Generated by Django 5.0.3 on 2024-03-20 20:34

import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('songs', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Playlist',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('playlist_id', models.UUIDField(default=uuid.uuid4)),
                ('name', models.CharField(max_length=255)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('songs', models.ManyToManyField(related_name='playlist_songs', to='songs.song')),
            ],
            options={
                'verbose_name_plural': 'Playlists',
                'ordering': ['-created_at'],
            },
        ),
    ]
