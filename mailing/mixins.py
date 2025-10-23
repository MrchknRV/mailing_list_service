from django.contrib.auth.mixins import UserPassesTestMixin
from django.core.exceptions import PermissionDenied
from django.shortcuts import redirect


class OwnerRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        obj = self.get_object()
        return obj.owner == self.request.user

    def handle_no_permission(self):
        if self.request.user.is_authenticated:
            raise PermissionDenied("У вас нет доступа к этому объекту.")
        return redirect("users:login")


class OwnerQuerysetMixin:
    def t_queryset(self):
        queryset = super().get_queryset()

        if not self.request.user.is_authenticated:
            return queryset.none()

        if hasattr(self.request.user, 'is_manager') and self.request.user.is_manager:
            return queryset

        return queryset.filter(owner=self.request.user)
