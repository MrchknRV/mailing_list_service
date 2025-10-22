from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

from . import views

app_name = "users"

urlpatterns = [
    path("register/", views.RegisterView.as_view(), name="register"),
    path("login/", views.UserLoginView.as_view(), name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("profile/", views.ProfileView.as_view(), name="profile"),
    path("verify-email/<int:pk>/<str:token>/", views.verify_email, name="verify_email"),
    path("password_reset/", views.CustomPasswordResetView.as_view(), name="password_reset"),
    path(
        "password_reset_confirm/<uidb64>/<token>/",
        views.CustomPasswordResetConfirmView.as_view(),
        name="password_reset_confirm",
    ),
    path("profile/edit/", views.profile_edit_comprehensive, name="profile_edit"),
    path("profile/update/", views.ProfileUpdateView.as_view(), name="profile_update"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
