# Generated by Django 5.0.3 on 2024-03-20 20:38

import django.db.models.deletion
import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('artists', '0001_initial'),
        ('songs', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Album',
            fields=[
                ('album_id', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=255)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('artist_album', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, related_name='artist_album', to='artists.artist')),
                ('songs', models.ManyToManyField(related_name='songs_in_album', to='songs.song')),
            ],
            options={
                'verbose_name_plural': "Album's",
                'ordering': ['-created_at'],
            },
        ),
    ]
