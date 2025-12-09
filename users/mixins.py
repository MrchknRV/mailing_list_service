from django.contrib.auth.mixins import UserPassesTestMixin
from django.core.exceptions import PermissionDenied
from django.shortcuts import redirect

from .models import User


class RoleRequiredMixin(UserPassesTestMixin):
    allowed_role = []

    def test_func(self):
        if not self.request.user.is_authenticated:
            return False

        return self.request.user.role in self.allowed_role

    def handle_no_permission(self):
        if self.request.user.is_authenticated:
            raise PermissionDenied("Не достаточно прав для доступа к этой странице")
        return redirect("users:login")

class ManagerRequiredMixin(RoleRequiredMixin):
    allowed_role = [User.ROLE_MANAGER]


class AdminRequiredMixin(RoleRequiredMixin):
    allowed_role = [User.ROLE_ADMIN]


class OwnerOrManagerRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        if not self.request.user.is_authenticated:
            return False

        if self.request.user.is_manager or self.request.user.is_admin:
            return True

        obj = self.get_object()
        return hasattr(obj, "owner") and obj.owner == self.request.user

    def handle_no_permission(self):
        if self.request.user.is_authenticated:
            raise PermissionDenied("У вас нет доступа к этому объекту.")
        return redirect("users:login")


class UserNotBlockedMixin(UserPassesTestMixin):
    def test_func(self):
        if not self.request.user.is_authenticated:
            return False

        return not self.request.user.is_blocked

    def handle_no_permission(self):
        if self.request.user.is_authenticated and self.request.user.is_blocked:
            from django.contrib import messages

            messages.error(self.request, "Ваш аккаунт заблокирован.")
            from django.contrib.auth import logout

            logout(self.request)
        return redirect("users:login")
