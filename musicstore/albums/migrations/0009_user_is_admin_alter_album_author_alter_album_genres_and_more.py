# Generated by Django 5.1.1 on 2024-11-27 07:12

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('albums', '0008_user_password'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='is_admin',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='album',
            name='author',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='authors', to='albums.author'),
        ),
        migrations.AlterField(
            model_name='album',
            name='genres',
            field=models.ManyToManyField(related_name='albums', to='albums.genre', verbose_name='Жанры'),
        ),
        migrations.AlterField(
            model_name='album',
            name='users',
            field=models.ManyToManyField(related_name='purchased_albums', to='albums.user', verbose_name='Пользователи'),
        ),
    ]
