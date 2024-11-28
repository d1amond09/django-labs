from django.db import models
from django.contrib.auth.models import User

class Genre(models.Model):
    name = models.CharField('Название жанра', max_length=100)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'

class Author(models.Model):
    name = models.CharField('Имя автора',max_length=100)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Автор'
        verbose_name_plural = 'Авторы'

class Album(models.Model):
    title = models.CharField('Название', max_length=255)
    release_date = models.DateField('Дата выхода')
    author = models.ForeignKey(Author, on_delete=models.CASCADE, related_name='authors')
    genres = models.ManyToManyField(Genre, related_name='albums', verbose_name='Жанры')
    users = models.ManyToManyField(User, related_name='purchased_albums', verbose_name='Пользователи')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Альбом'
        verbose_name_plural = 'Альбомы'