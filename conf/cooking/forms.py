from django import forms
from .models import Post, Comment
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.models import User


class PostAddForm(forms.ModelForm):
    """Форма для добавления новой статьи от пользователя"""

    class Meta:
        model = Post
        fields = ("title", "content", "photo", "category")

        widgets = {
            "title": forms.TextInput(attrs={"class": "form-control"}),
            "content": forms.Textarea(attrs={"class": "form-control"}),
            "photo": forms.FileInput(attrs={"class": "form-control"}),
            "categore": forms.Select(attrs={"class": "form-control"}),
        }


class LoginForm(AuthenticationForm):
    """Форма для аунтентификации пользователя"""

    widget_username = forms.TextInput(attrs={"class": "form-control"})

    username = forms.CharField(
        label="Имя пользователя",
        max_length=150,
        widget=widget_username,
    )

    widget_pssword = forms.PasswordInput(attrs={"class": "form-control"})

    password = forms.CharField(label="Пароль", widget=widget_pssword)


class RegistrationForm(UserCreationForm):
    """Форма для регистрации пользователя"""

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")

        # Имя пользователя

    widget_username = forms.TextInput(
        attrs={"class": "form-control", "placeholder": "Имя пользователя"}
    )

    username = forms.CharField(
        max_length=150,
        widget=widget_username,
    )

    # Электронная почта
    widget_email = forms.TextInput(
        attrs={"class": "form-control", "placeholder": "Электронная почта"}
    )

    email = forms.EmailField(widget=widget_email)

    # Пароль номер 1
    widget_password1 = forms.PasswordInput(
        attrs={"class": "form-control", "placeholder": "Пароль"}
    )

    password1 = forms.CharField(widget=widget_password1)

    # Пароль номер 2
    widget_password2 = forms.PasswordInput(
        attrs={"class": "form-control", "placeholder": "Подтвердите пароль"}
    )

    password2 = forms.CharField(widget=widget_password2)


class CommentForm(forms.ModelForm):
    """Форма для написания комментария"""

    class Meta:
        model = Comment
        fields = ("text",)

        widgets = {
            "text": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Текст вашего комментария",
                }
            )
        }
