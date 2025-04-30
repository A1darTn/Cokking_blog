from django.shortcuts import render, redirect
from django.db.models import F, Q
from django.contrib.auth import login, logout
from django.contrib import messages
from django.views.generic import (
    ListView,
    DeleteView,
    DetailView,
    CreateView,
    UpdateView,
)
from django.urls import reverse_lazy
from django.contrib.auth.models import User

from .models import Post, Category, Comment
from .forms import PostAddForm, LoginForm, RegistrationForm, CommentForm

# Create your views here.


# def index(request):
#     """Главная страница"""
#     posts = Post.objects.all()
#     context = {
#         "title": "Главная страница",
#         "posts": posts,
#     }

#     return render(request, "cooking/index.html", context)


class Index(ListView):
    """Главная страница"""

    model = Post
    context_object_name = "posts"
    template_name = "cooking/index.html"
    extra_context = {"title": "Главная страница"}


# def category_list(request, pk):
#     """Реакция на кнопки категорий"""
#     posts = Post.objects.filter(category_id=pk)
#     context = {
#         "title": posts[0].category,
#         "posts": posts,
#     }
#     return render(request, "cooking/index.html", context)


class CategoryList(Index):
    def get_queryset(self):
        """Здесь можно сделать фильтры"""
        return Post.objects.filter(category_id=self.kwargs["pk"], is_published=True)

    def get_context_data(self, *, object_data=None, **kwargs):
        """Для динамических данных"""
        context = super().get_context_data()
        category = Category.objects.get(pk=self.kwargs["pk"])
        context["title"] = category
        return context


# def post_detail(request, pk):
#     article = Post.objects.get(pk=pk)
#     Post.objects.filter(pk=pk).update(watched=F("watched") + 1)
#     ext_post = Post.objects.all().exclude(pk=pk).order_by("-watched")[:5]
#     context = {"title": article, "post": article, "ext_post": ext_post}

#     return render(request, "cooking/article_detail.html", context)


class PostDetail(DeleteView):
    """Страничка статьи"""

    model = Post
    template_name = "cooking/article_detail.html"

    def get_queryset(self):
        return Post.objects.filter(pk=self.kwargs["pk"])

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        Post.objects.filter(pk=self.kwargs["pk"]).update(watched=F("watched") + 1)
        post = Post.objects.get(pk=self.kwargs["pk"])
        context["title"] = post
        ext_post = (
            Post.objects.all().exclude(pk=self.kwargs["pk"]).order_by("-watched")[:5]
        )
        context["ext_post"] = ext_post
        context["comments"] = Comment.objects.filter(post=post)
        if self.request.user.is_authenticated:
            context["comment_form"] = CommentForm
        return context


class AddPost(CreateView):
    """Добавление статьи от пользователя"""

    form_class = PostAddForm
    template_name = "cooking/article_add_form.html"
    extra_context = {"title": "Добавить статью"}

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class PostUpdate(UpdateView):
    """Изменение статьи по кнопке"""

    model = Post
    form_class = PostAddForm
    template_name = "cooking/article_add_form.html"


class PostDelete(DeleteView):
    """Удаление статьи по нопке"""

    model = Post
    success_url = reverse_lazy("index")
    context_object_name = "post"
    extra_context = {"title": "Изменение статьи"}


class SearchResults(Index):
    """Поиск слова в заголовках и в содержаниях статьей"""

    def get_queryset(self):
        """Функция для фильтрации выборок с бд"""
        word = self.request.GET.get("q")
        posts = Post.objects.filter(
            Q(title__icontains=word) | Q(content__icontains=word)
        )
        return posts


def add_comment(request, post_id):
    """Добавление комментария к статьям"""
    form = CommentForm(data=request.POST)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.user = request.user
        comment.post = Post.objects.get(pk=post_id)
        comment.save()
        messages.success(request, "Ваш комментарий успешно добавлен")

    return redirect("post_detail", post_id)


# class
# def add_post(request):
#     """Добавление статьи от пользователя"""
#     if request.method == "POST":
#         form = PostAddForm(request.POST, request.FILES)
#         if form.is_valid():
#             post = Post.objects.create(**form.cleaned_data)
#             post.save()

#             return redirect("post_detail", post.pk)
#     else:
#         form = PostAddForm()

#     context = {"form": form, "title": "Добавить статью"}

#     return render(request, "cooking/article_add_form.html", context)


def user_login(request):
    """Аутентификация пользователя"""
    if request.method == "POST":
        form = LoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            messages.success(request, "Вы успешно вошли в аккаунт")
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


def profile(request, user_id):
    """Страничка пользователя"""
    user = User.objects.get(pk=user_id)
    posts = Post.objects.filter(author=user)
    context = {
        'user': user,
        'posts': posts
    }

    return render(request, 'cooking/profile.html', context)