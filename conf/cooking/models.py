from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User


# Create your models here.
class Category(models.Model):
    title = models.CharField(max_length=255, verbose_name="Название категории")

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("category_list", kwargs={"pk": self.pk})

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"


class Post(models.Model):
    title = models.CharField(max_length=255, verbose_name="Заголовок статьи")
    content = models.TextField(
        default="Скоро тут будет статья...", verbose_name="Текст статьи"
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата обновления")
    photo = models.ImageField(
        upload_to="photos/", blank=True, null=True, verbose_name="Изображение"
    )
    watched = models.PositiveIntegerField(default=0, verbose_name="Просмотры")
    is_published = models.BooleanField(default=True, verbose_name="Публикация")
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, verbose_name="Категория"
    )
    author = models.ForeignKey(
        User, default=None, null=True, blank=True, on_delete=models.CASCADE
    )

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("post_detail", kwargs={"pk": self.pk})

    class Meta:
        verbose_name = "Пост"
        verbose_name_plural = "Посты"


class Comment(models.Model):
    """Комменатрии к постам"""

    post = models.ForeignKey(Post, on_delete=models.CASCADE, verbose_name="Пост")
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, verbose_name="Пользователь"
    )
    text = models.TextField(verbose_name="Комментарий")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")

    def __str__(self):
        return self.text

    class Meta:
        verbose_name = "Комментарий"
        verbose_name_plural = "Комментарии"
