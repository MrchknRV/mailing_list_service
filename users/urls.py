from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

from . import views
from .views_manager import *

app_name = "users"

urlpatterns = [
    path("register/", views.RegisterView.as_view(), name="register"),
    path("login/", views.UserLoginView.as_view(), name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("profile/", views.ProfileView.as_view(), name="profile"),
    path("verify-email/<int:user_id>/<str:token>/", views.verify_email, name="verify_email"),
    path("password_reset/", views.CustomPasswordResetView.as_view(), name="password_reset"),
    path(
        "password_reset_confirm/<uidb64>/<token>/",
        views.CustomPasswordResetConfirmView.as_view(),
        name="password_reset_confirm",
    ),
    path("profile/edit/", views.profile_edit_comprehensive, name="profile_edit"),
    path("profile/update/", views.ProfileUpdateView.as_view(), name="profile_update"),

    path('manager/dashboard/', ManagerDashboardView.as_view(), name='manager_dashboard'),
    path('manager/users/', UserListView.as_view(), name='user_list'),
    path('manager/users/<int:pk>/block/', UserBlockToggleView.as_view(), name='user_block_toggle'),
    path('manager/users/<int:pk>/role/', UserRoleUpdateView.as_view(), name='user_role_update'),
    path('manager/mailings/', ManagerMailingListView.as_view(), name='manager_mailing_list'),
    path('manager/mailings/<int:pk>/disable/', ManagerMailingDisableView.as_view(), name='manager_mailing_disable'),
    path('manager/clients/', ManagerClientListView.as_view(), name='manager_client_list'),
    path('manager/messages/', ManagerMessageListView.as_view(), name='manager_message_list'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
