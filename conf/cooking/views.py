from django.shortcuts import render, redirect
from django.db.models import F
from django.contrib.auth import login, logout

from .models import Post
from .forms import PostAddForm, LoginForm, RegistrationForm

# Create your views here.


def index(request):
    """Главная страница"""
    posts = Post.objects.all()
    context = {
        "title": "Главная страница",
        "posts": posts,
    }

    return render(request, "cooking/index.html", context)


def category_list(request, pk):
    """Реакция на кнопки категорий"""
    posts = Post.objects.filter(category_id=pk)
    context = {
        "title": posts[0].category,
        "posts": posts,
    }
    return render(request, "cooking/index.html", context)


def post_detail(request, pk):
    article = Post.objects.get(pk=pk)
    Post.objects.filter(pk=pk).update(watched=F("watched") + 1)
    ext_post = Post.objects.all().order_by("-watched")[:5]
    context = {"title": article, "post": article, "ext_post": ext_post}

    return render(request, "cooking/article_detail.html", context)


def add_post(request):
    """Добавление статьи от пользователя"""
    if request.method == "POST":
        form = PostAddForm(request.POST, request.FILES)
        if form.is_valid():
            post = Post.objects.create(**form.cleaned_data)
            post.save()

            return redirect("post_detail", post.pk)
    else:
        form = PostAddForm()

    context = {"form": form, "title": "Добавить статью"}

    return render(request, "cooking/article_add_form.html", context)


def user_login(request):
    """Аутентификация пользователя"""
    if request.method == "POST":
        form = LoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)

            return redirect("index")
    else:
        form = LoginForm()

    context = {"title": "Авторизация пользователя", "form": form}

    return render(request, "cooking/login_form.html", context)


def user_logout(request):
    """Выход пользователя"""
    logout(request)
    return redirect("index")


def register(request):
    """Регистрация пользователя"""
    if request.method == "POST":
        form = RegistrationForm(data=request.POST)
        if form.is_valid():
            form.save()

            return redirect("login")
    else:
        form = RegistrationForm()

    context = {"title": "Регистрация пользователя", "form": form}

    return render(request, "cooking/register.html", context)
