"""
URL configuration for conf project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path
from django.conf.urls.static import static
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)
from django.views.decorators.cache import cache_page

from django.conf import settings
from cooking.views import register, user_login, user_logout, add_comment, profile
from cooking.views import (
    Index,
    CategoryList,
    PostDetail,
    AddPost,
    PostUpdate,
    PostDelete,
    SearchResults,
    UserChangePassword,
)
from cooking.views import (
    CookingApi,
    CookingAPIDetail,
    CookingCategoryAPI,
    CookingCategoryAPIDetail,
)
from cooking.yasg import urlpatterns as api_doc_urls

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", Index.as_view(), name="index"),
    # path('', cache_page(60 * 15)(Index.as_view()), name='index'), # Кэщирование на основе файловой системы
    path("category/<int:pk>/", CategoryList.as_view(), name="category_list"),
    path("post/<int:pk>/", PostDetail.as_view(), name="post_detail"),
    path("add_article/", AddPost.as_view(), name="add"),
    path("post/<int:pk>/update/", PostUpdate.as_view(), name="post_update"),
    path("post/<int:pk>/delete", PostDelete.as_view(), name="post_delete"),
    path("search/", SearchResults.as_view(), name="search"),
    path("password/", UserChangePassword.as_view(), name="change_password"),
    path("login/", user_login, name="login"),
    path("logout/", user_logout, name="logout"),
    path("register/", register, name="register"),
    path("add_comment/<int:post_id>/", add_comment, name="add_comment"),
    path("profile/<int:user_id>/", profile, name="profile"),
    # API
    path("post/api", CookingApi.as_view(), name="CookingAPI"),
    path("post/api/<int:pk>", CookingAPIDetail.as_view(), name="CookingAPIDeatil"),
    path("categoies/api/", CookingCategoryAPI.as_view(), name="CookingCategoryAPI"),
    path(
        "categoies/api/<int:pk>",
        CookingCategoryAPIDetail.as_view(),
        name="CookingCategoryAPIDetail",
    ),
    path("api/token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("api/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("api/token/verify", TokenVerifyView.as_view(), name="token_verify"),
] + api_doc_urls


if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
