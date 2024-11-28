from .forms import CustomUserCreationForm
from django.contrib.auth import logout
from django.contrib import messages
from django.db.models import Count
from .models import Album, Author, Genre
from django.contrib.auth.models import User
from .forms import AlbumForm, AuthorForm, GenreForm, UserForm
from django.views.generic import UpdateView, TemplateView, View
from django.views.generic.detail import SingleObjectMixin
from django.views.generic.edit import FormMixin, ProcessFormView
from django.views.generic import ListView
from django.shortcuts import render, get_object_or_404, redirect
from .forms import GenreForm
from django.urls import reverse_lazy
from .decorators import admin_required
from .forms import LoginForm
from django.contrib.auth import authenticate, login

def album_list(request):
    if request.user.is_authenticated:
        albums = Album.objects.filter(users=request.user).order_by('title')
    else:
        albums = Album.objects.none()

    data = {
        'albums': albums,
        'title': 'Музыкальные альбомы'
    }
    return render(request, 'albums/album_list.html', data)

def author_detail(request, author_id):
    author = get_object_or_404(Author, id=author_id)
    albums = Album.objects.filter(author=author)
    return render(request, 'authors/author_detail.html', {'author': author, 'albums': albums})

@admin_required
def album_create(request):
    error = ''
    if request.method == 'POST':
        form = AlbumForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('album_list')
        else:
            error = 'Форма неверно заполнена'

    form = AlbumForm()

    data = {
        'form': form,
        'error': error
    }

    return render(request, 'albums/album_create.html', data)

@admin_required
def album_edit(request, pk):
    album = get_object_or_404(Album, pk=pk)
    if request.method == 'POST':
        form = AlbumForm(request.POST, instance=album)
        if form.is_valid():
            form.save()
            return redirect('album_list')
    else:
        form = AlbumForm(instance=album)
    return render(request, 'albums/album_edit.html', {'form': form})

@admin_required
def album_delete(request, pk):
    album = get_object_or_404(Album, pk=pk)
    if request.method == 'POST':
        album.delete()
        return redirect('album_list')
    return render(request, 'albums/album_delete.html', {'album': album})

@admin_required
def author_create(request):
    error = ''
    if request.method == 'POST':
        form = AuthorForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('author_list')
        else:
            error = 'Форма неверно заполнена'

    form = AuthorForm()

    data = {
        'form': form,
        'error': error
    }

    return render(request, 'authors/author_create.html', data)


def author_list(request):
    authors = Author.objects.all()
    data = {
        'authors': authors,
        'title': 'Авторы'
    }
    return render(request, 'authors/author_list.html', data)

@admin_required
def author_edit(request, pk):
    author = get_object_or_404(Author, pk=pk)
    if request.method == 'POST':
        form = AuthorForm(request.POST, instance=author)
        if form.is_valid():
            form.save()
            return redirect('author_list')
    else:
        form = AuthorForm(instance=author)
    return render(request, 'authors/author_edit.html', {'form': form})

@admin_required
def author_delete(request, pk):
    author = get_object_or_404(Author, pk=pk)
    if request.method == 'POST':
        author.delete()
        return redirect('author_list')
    return render(request, 'authors/author_delete.html', {'author': author})

def user_list(request):
    data = {
        'users': User.objects.all(),
        'title': 'Пользователи'
    }
    return render(request, 'users/user_list.html', data)

@admin_required
def user_create(request):
    error = ''
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('user_list')
        else:
            error = 'Форма неверно заполнена'

    form = UserForm()

    data = {
        'form': form,
        'error': error
    }

    return render(request, 'users/user_create.html', data)

@admin_required
def user_edit(request, pk):
    user = get_object_or_404(User, pk=pk)
    if request.method == 'POST':
        form = UserForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect('genre_list')
    else:
        form = UserForm(instance=user)
    return render(request, 'users/user_edit.html', {'form': form})

@admin_required
def user_delete(request, pk):
    user = get_object_or_404(User, pk=pk)
    if request.method == 'POST':
        user.delete()
        return redirect('genre_list')
    return render(request, 'users/user_delete.html', {'genre': user})


def favorite_genre(user_id):
    favorite = (Album.objects
                .filter(users__id=user_id)
                .values('genres__name')
                .annotate(count=Count('genres'))
                .order_by('-count')
                .first())

    if favorite:
        return favorite['genres__name']
    else:
        return None

def user_favorite_genre(request, user_id):
    user = User.objects.get(id=user_id)
    genre = favorite_genre(user_id)

    return render(request, 'users/user_favorite_genre.html', {'user': user, 'genre': genre})


class GenreCreateView(TemplateView, FormMixin, ProcessFormView):
    template_name = 'genres/genre_create.html'
    form_class = GenreForm
    success_url = reverse_lazy('genre_list')

    @admin_required
    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    @admin_required
    def form_valid(self, form):
        form.save()
        return super().form_valid(form)


class GenreUpdateView(UpdateView):
    model = Genre
    template_name = 'genres/genre_edit.html'
    form_class = GenreForm
    success_url = reverse_lazy('genre_list')

    @admin_required
    def get_object(self, queryset=None):
        return super().get_object(queryset)

    @admin_required
    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        return self.render_to_response({'form': form, 'object': self.object})

    @admin_required
    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            self.object = form.save(commit=False)
            self.object.save()
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        return redirect(self.success_url)

    def form_invalid(self, form):
        return self.render_to_response({'form': form, 'object': self.object})


class GenreDeleteView(SingleObjectMixin, View):
    model = Genre
    success_url = reverse_lazy('genre_list')
    template_name = 'genres/genre_delete.html'

    @admin_required
    def get(self, request, *args, **kwargs):
        genre = self.get_object()
        return render(request, self.template_name, {'object': genre})

    @admin_required
    def post(self, request, *args, **kwargs):
        genre = self.get_object()
        genre.delete()
        return redirect(self.success_url)

class GenreListView(ListView):
    model = Genre
    template_name = 'genres/genre_list.html'
    context_object_name = 'genres'

    def get_queryset(self):
        return Genre.objects.all()


def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, "Регистрация прошла успешно!")
            return redirect('login')
        else:
            print(form.errors)
    else:
        form = CustomUserCreationForm()
    return render(request, 'auth/register.html', {'form': form})

def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('album_list')
            else:
                error = 'Неверное имя пользователя или пароль'
                return render(request, 'auth/login.html', {'form': form, 'error': error})
    else:
        form = LoginForm()
    return render(request, 'auth/login.html', {'form': form})

def custom_logout(request):
    logout(request)  # Logs the user out
    messages.success(request, "Вы успешно вышли из системы.")
    return redirect('home')

def genre_list(request):
    genres = Genre.objects.all()
    return render(request, 'genres/genre_list.html', {'genres': genres})

@admin_required
def genre_create(request):
    if request.method == 'POST':
        form = GenreForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('genre_list')
    else:
        form = GenreForm()
    return render(request, 'genres/genre_create.html', {'form': form})

@admin_required
def genre_edit(request, pk):
    genre = get_object_or_404(Genre, pk=pk)
    if request.method == 'POST':
        form = GenreForm(request.POST, instance=genre)
        if form.is_valid():
            form.save()
            return redirect('genre_list')
    else:
        form = GenreForm(instance=genre)
    return render(request, 'genres/genre_edit.html', {'form': form})

@admin_required
def genre_delete(request, pk):
    genre = get_object_or_404(Genre, pk=pk)
    if request.method == 'POST':
        genre.delete()
        return redirect('genre_list')
    return render(request, 'genres/genre_delete.html', {'genre': genre})


