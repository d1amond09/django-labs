from django.contrib import admin
from .models import Album, Genre, Author

admin.site.register(Genre)
admin.site.register(Album)
admin.site.register(Author)
