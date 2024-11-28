from django.urls import path
from django.contrib.auth.views import LogoutView
from . import views

urlpatterns = [
    path('', views.album_list, name='album_list'),
    path('album_create', views.album_create, name='album_create'),
    path('edit/<int:pk>/', views.album_edit, name='album_edit'),
    path('delete/<int:pk>/', views.album_delete, name='album_delete'),

    path('author_list', views.author_list, name='author_list'),
    path('author<int:author_id>', views.author_detail, name='author_detail'),
    path('author_create', views.author_create, name='author_create'),
    path('author_list/edit/<int:pk>/', views.author_edit, name='author_edit'),
    path('author_list/delete/<int:pk>/', views.author_delete, name='author_delete'),

    path('genre_list', views.genre_list, name='genre_list'),
    path('genre_create', views.genre_create, name='genre_create'),
    path('genre_list/edit/<int:pk>/', views.genre_edit, name='genre_edit'),
    path('genre_list/delete/<int:pk>/', views.genre_delete, name='genre_delete'),
    #path('genre_list', views.GenreListView.as_view(), name='genre_list'),
    #path('genre_create', views.GenreCreateView.as_view(), name='genre_create'),
    #path('genre_list/edit/<int:pk>/', views.GenreUpdateView.as_view(), name='genre_edit'),
    #path('genre_list/delete/<int:pk>/', views.GenreDeleteView.as_view(), name='genre_delete'),

    path('user_list', views.user_list, name='user_list'),
    path('user_create', views.user_create, name='user_create'),
    path('user_list/edit/<int:pk>/', views.user_edit, name='user_edit'),
    path('user_list/delete/<int:pk>/', views.user_delete, name='user_delete'),
    path('user_list/<int:user_id>/favorite_genre/', views.user_favorite_genre, name='user_favorite_genre'),

    path('register', views.register, name='register'),
    path('login', views.user_login, name='login'),
    path('logout/', views.custom_logout, name='logout'),
]
