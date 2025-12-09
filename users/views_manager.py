from django.views.generic import ListView, UpdateView, View
from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages
from django.urls import reverse_lazy
from .mixins import ManagerRequiredMixin, UserNotBlockedMixin
from .models import User
from mailing.models import Mailing, Client, Message, Status


class UserListView(ManagerRequiredMixin, UserNotBlockedMixin, ListView):
    model = User
    template_name = "users/user_list.html"
    context_object_name = "users"

    def get_queryset(self):
        return User.objects.all().order_by("-date_joined")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['total_users'] = User.objects.count()
        context['active_users'] = User.objects.filter(is_active=True, is_blocked=False).count()
        context['blocked_users'] = User.objects.filter(is_blocked=True).count()
        context['managers_count'] = User.objects.filter(role__in=[User.ROLE_MANAGER, User.ROLE_ADMIN]).count()
        return context


class UserBlockToggleView(ManagerRequiredMixin, UserNotBlockedMixin, View):
    def post(self, request, pk):
        user = get_object_or_404(User, pk=pk)

        if user == request.user:
            messages.error(request, "Нельзя блокировать самого себя")
            return redirect("users:user_list")

        if user.is_manager and not request.user.is_admin:
            messages.error(request, "У вас нет доступа блокировать другних менеджеров")
            return redirect("users:user_list")

        user.is_blocked = not user.is_blocked
        user.save()

        action = "заблокирован" if user.is_blocked else "разблокирован"
        messages.success(request, f"Пользователь {user.username} - {action}")

        return redirect("users:user_list")


class UserRoleUpdateView(ManagerRequiredMixin, UserNotBlockedMixin, UpdateView):
    model = User
    fields = ["role"]
    template_name = "users/user_role_update.html"
    success_url = reverse_lazy("users:user_list")

    def form_valid(self, form):
        user = form.save(commit=False)

        if user == self.request.user and user.role != User.ROLE_ADMIN:
            messages.error(self.request, "Нельзя понизить себе роль")
            return redirect("users:user_list")

        user.save()
        messages.success(self.request, f"Роль пользователя {user.username} изменена на {user.get_role_display()}")
        return super().form_valid(form)


class ManagerMailingListView(ManagerRequiredMixin, UserNotBlockedMixin, ListView):
    model = Mailing
    template_name = "mailing/manager_mailing_list.html"
    context_object_name = "mailings"

    def get_queryset(self):
        return Mailing.objects.all().select_related("owner", "message").prefetch_related("clients")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["total_mailings"] = Mailing.objects.count()
        context["active_mailings"] = Mailing.objects.filter(status=Status.STARTED).count()
        context["completed_mailings"] = Mailing.objects.filter(status=Status.COMPLETED).count()

        return context


class ManagerMailingDisableView(ManagerRequiredMixin, UserNotBlockedMixin, View):

    def post(self, request, pk):
        mailing = get_object_or_404(Mailing, pk=pk)

        if mailing.status == Status.STARTED:
            mailing.status = Status.COMPLETED
            mailing.save()
            messages.success(request, f"Рассылка №{mailing.id} отключена")
        else:
            messages.success(request, f"Рассылка №{mailing.id} уже не активна")

        return redirect("mailings:manager_mailing_list")


class ManagerClientListView(ManagerRequiredMixin, UserNotBlockedMixin, ListView):
    """Просмотр всех клиентов для менеджеров"""
    model = Client
    template_name = 'mailing/manager_client_list.html'
    context_object_name = 'clients'
    paginate_by = 20

    def get_queryset(self):
        return Client.objects.all().select_related('owner')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        clients = self.get_queryset()
        context['active_owners_count'] = User.objects.filter(
            client__in=clients, is_blocked=False
        ).distinct().count()
        context['in_mailings_count'] = clients.filter(mailing__isnull=False).distinct().count()
        return context


class ManagerMessageListView(ManagerRequiredMixin, UserNotBlockedMixin, ListView):
    """Просмотр всех сообщений для менеджеров"""
    model = Message
    template_name = 'mailing/manager_message_list.html'
    context_object_name = 'messages'
    paginate_by = 20

    def get_queryset(self):
        return Message.objects.all().select_related('owner')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        messages = self.get_queryset()
        context['active_owners_count'] = User.objects.filter(
            messages__in=messages, is_blocked=False
        ).distinct().count()
        context['in_mailings_count'] = messages.filter(mailing__isnull=False).distinct().count()

        # Средняя длина сообщений
        total_length = sum(len(msg.body) for msg in messages)
        context['avg_length'] = total_length // len(messages) if messages else 0

        return context


class ManagerDashboardView(ManagerRequiredMixin, UserNotBlockedMixin, ListView):
    """Дашборд для менеджеров"""
    template_name = 'users/manager_dashboard.html'

    def get_queryset(self):
        return None

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['total_users'] = User.objects.count()
        context['active_users'] = User.objects.filter(is_active=True, is_blocked=False).count()
        context['blocked_users'] = User.objects.filter(is_blocked=True).count()
        context['managers_count'] = User.objects.filter(role__in=[User.ROLE_MANAGER, User.ROLE_ADMIN]).count()

        context['total_mailings'] = Mailing.objects.count()
        context['active_mailings'] = Mailing.objects.filter(status=Status.STARTED).count()
        context['completed_mailings'] = Mailing.objects.filter(status=Status.COMPLETED).count()

        context['total_clients'] = Client.objects.count()
        context['total_messages'] = Message.objects.count()

        context['recent_active_mailings'] = Mailing.objects.filter(
            status=Status.STARTED,
        ).select_related('owner', 'message')[:5]

        context['recent_users'] = User.objects.all().order_by('-date_joined')[:5]

        return context
