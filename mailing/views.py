from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, DetailView, ListView, TemplateView, UpdateView

from .forms import ClientForm, MailingForm, MessageForm
from .mixins import OwnerQuerysetMixin, OwnerRequiredMixin
from .models import Client, Mailing, MailingAttempt, Message, Status
from .services import EmailService


class IndexView(TemplateView):
    template_name = "mailing/index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["total_mailings"] = Mailing.objects.count()
        context["active_mailings"] = Mailing.objects.filter(status=Status.STARTED).count()
        context["unique_clients"] = Client.objects.distinct().count()
        return context


class ClientListView(OwnerQuerysetMixin, LoginRequiredMixin, ListView):
    model = Client
    context_object_name = "clients"
    template_name = "mailing/client_list.html"


class ClientCreateView(LoginRequiredMixin, CreateView, SuccessMessageMixin):
    model = Client
    form_class = ClientForm
    template_name = "mailing/client_form.html"
    success_url = reverse_lazy("mailing:client_list")
    success_message = "Клиент успешно создан!"

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)


class ClientUpdateView(LoginRequiredMixin, UpdateView, SuccessMessageMixin, OwnerRequiredMixin):
    model = Client
    form_class = ClientForm
    template_name = "mailing/client_form.html"
    success_url = reverse_lazy("mailing:client_list")
    success_message = "Клиент успешно обновлен!"


class ClientDeleteView(LoginRequiredMixin, DeleteView, OwnerRequiredMixin):
    model = Client
    template_name = "mailing/client_delete_confirm.html"
    success_url = reverse_lazy("mailing:client_list")


class ClientDetailView(LoginRequiredMixin, DetailView, OwnerRequiredMixin):
    model = Client
    template_name = "mailing/client_detail.html"
    context_object_name = "client"
    login_url = reverse_lazy("mailing:login")


class MessageListView(LoginRequiredMixin, ListView, OwnerQuerysetMixin):
    model = Message
    context_object_name = "messages"
    template_name = "mailing/message_list.html"


class MessageCreateView(LoginRequiredMixin, CreateView, SuccessMessageMixin):
    model = Message
    form_class = MessageForm
    tempalte_name = "mailing/message_form.html"
    success_url = reverse_lazy("mailing:message_list")
    success_message = "Сообщение успешно создано"

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)


class MessageUpdateView(LoginRequiredMixin, UpdateView, SuccessMessageMixin, OwnerRequiredMixin):
    model = Message
    form_class = MessageForm
    template_name = "mailing/message_form.html"
    success_url = reverse_lazy("mailing:message_list")
    success_message = "Сообщение успешно обновлено!"


class MessageDeleteView(LoginRequiredMixin, DeleteView, OwnerRequiredMixin):
    model = Message
    template_name = "mailing/message_delete_confirm.html"
    success_url = reverse_lazy("mailing:message_list")


class MessageDetailView(LoginRequiredMixin, DetailView, OwnerRequiredMixin):
    model = Message
    template_name = "mailing/message_detail.html"
    context_object_name = "message"
    login_url = reverse_lazy("mailing:login")


class MailingListView(LoginRequiredMixin, ListView, OwnerQuerysetMixin):
    model = Mailing
    context_object_name = "mailings"
    template_name = "mailing/mailing_list.html"


class MailingCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Mailing
    form_class = MailingForm
    template_name = "mailing/mailing_form.html"
    success_url = reverse_lazy("mailing:mailing_list")
    success_message = "Рассылка успешно создана!"

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["user"] = self.request.user
        return kwargs

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["available_messages_count"] = Message.objects.filter(owner=self.request.user).count()
        context["available_clients_count"] = Client.objects.filter(owner=self.request.user).count()
        return context


class MailingUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView, OwnerRequiredMixin):
    model = Mailing
    form_class = MailingForm
    template_name = "mailing/mailing_form.html"
    success_url = reverse_lazy("mailing:mailing_list")
    success_message = "Рассылка успешно обновлена!"

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["user"] = self.request.user
        return kwargs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["available_messages_count"] = Message.objects.filter(owner=self.request.user).count()
        context["available_clients_count"] = Client.objects.filter(owner=self.request.user).count()
        return context


class MailingDeleteView(LoginRequiredMixin, DeleteView, OwnerRequiredMixin):
    model = Mailing
    template_name = "mailing/mailing_confirm_delete.html"
    success_url = reverse_lazy("mailing:mailing_list")


class MailingDetailView(LoginRequiredMixin, DetailView, OwnerRequiredMixin):
    model = Mailing
    template_name = "mailing/mailing_detail.html"
    context_object_name = "mailing"
    login_url = reverse_lazy("mailing:login")


class MailingSendView(LoginRequiredMixin, TemplateView):

    def post(self, request, pk):
        mailing = get_object_or_404(Mailing, pk=pk, owner=request.user)

        if mailing.status == Status.COMPLETED:
            messages.error(request, "Нельзя отправить завершенную рассылку.")
            return redirect("mailing:mailing_detail", pk=pk)

        if not mailing.clients.exists():
            messages.error(request, "Нельзя отправить рассылку без клиентов.")
            return redirect("mailing:mailing_detail", pk=pk)

        success_send, failed_send = EmailService.send_mass_mailing(mailing)

        if success_send > 0:
            messages.success(request, f"Рассылка отправлена! Успешно: {success_send}, Неудачно: {failed_send}")
        else:
            messages.error(request, f"Не удалось отправить рассылку. Неудачных отправок: {failed_send}")

        return redirect("mailing:mailing_detail", pk=pk)


class MailingSendOneView(LoginRequiredMixin, TemplateView): ...
