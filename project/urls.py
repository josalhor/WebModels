from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import include, path
from django.views.generic import TemplateView
from .signup import signup
from todo.views import book_catalogue

urlpatterns = (
    [
        path("", book_catalogue, name="main"),
        path("init", book_catalogue, name="main"),
        path("home", TemplateView.as_view(template_name="home.html"), name="home"),
        path("login", auth_views.LoginView.as_view(), name="login"),
        path("logout", auth_views.LogoutView.as_view(), name="logout"),
        path("todoadmin/", admin.site.urls),
        path("todo/", include("todo.urls", namespace="todo")),
        path('signup/', signup, name='signup'),
    ]
    # Static media in DEBUG mode:
    + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
)
