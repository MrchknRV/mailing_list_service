from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.views import LogoutView
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.views.generic import FormView, TemplateView, UpdateView

from mailing.models import Status
from mailing.services import EmailService

from .forms import (CustomPasswordResetForm, CustomSetPasswordForm, UserLoginForm, UserPasswordChangeForm,
                    UserProfileForm, UserRegisterForm, UserUpdateForm)
from .models import User, UserProfile


class RegisterView(FormView):
    template_name = "users/register.html"
    form_class = UserRegisterForm
    success_url = reverse_lazy("mailing:index")

    def form_valid(self, form):
        user = form.save(commit=False)

        user.email = form.cleaned_data["email"]
        user.save()

        token = user.generate_verification_token()

        verification_url = self.request.build_absolute_uri(f"/users/verify-email/{user.id}/{token}/")

        EmailService.send_verification_email(user, verification_url)
        messages.success(self.request, "Регистрация успешна! На Ваш email отправлено письмо подтверждения")

        return super().form_valid(form)


class UserLoginView(FormView):
    template_name = "users/login.html"
    form_class = UserLoginForm

    def form_valid(self, form):
        user = form.cleaned_data["user"]
        login(self.request, user)
        messages.success(self.request, f"Добро пожаловать, {user.username}!")
        return redirect("mailing:index")


def logout_view(request):
    logout(request)
    messages.success(request, "Вы успешно вышли из системы.")
    return redirect("mailing:index")


class ProfileView(LoginRequiredMixin, TemplateView):
    template_name = "users/profile.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["user_mailings_count"] = self.request.user.mailing_set.count()
        context["active_mailings_count"] = self.request.user.mailing_set.filter(status=Status.STARTED).count()
        # context['user_clients_count'] = self.request.user.client_set.count()
        # context['user_messages_count'] = self.request.user.message_set.count()
        return context


def verify_email(request, user_id, token):
    user = get_object_or_404(User, id=user_id)
    if user.verification_token == token:
        user.is_verified = True
        user.verification_token = None
        user.save()
        messages.success(request, "Ваш email подтвержден!")
    else:
        messages.error(request, "Email не подтвержден")

    return redirect("users:login")


class CustomPasswordResetView(FormView):
    template_name = "users/password_reset.html"
    form_class = CustomPasswordResetForm
    success_url = reverse_lazy("users:login")

    def form_valid(self, form):
        email = form.cleaned_data["email"]
        associated_users = User.objects.filter(email=email)
        if associated_users.exists():
            for user in associated_users:
                token = default_token_generator.make_token(user)
                uid = urlsafe_base64_encode(force_bytes(user.pk))

                reset_url = self.request.build_absolute_uri(f"/users/password_reset_confirm/{uid}/{token}/")

                EmailService.send_password_reset_email(user, reset_url)

        messages.success(self.request, "На ваш email отправлены инструкции по восстановлению пароля.")
        return super().form_valid(form)


class CustomPasswordResetConfirmView(FormView):
    template_name = "users/password_reset_confirm.html"
    form_class = CustomSetPasswordForm
    success_url = reverse_lazy("users:login")

    def dispatch(self, request, *args, **kwargs):
        self.uidb64 = kwargs.get("uidb64")
        self.token = kwargs.get("token")

        return super().dispatch(request, *args, **kwargs)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        try:
            uid = force_str(urlsafe_base64_decode(self.uidb64))
            user = User.objects.get(id=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None

        if user is not None and default_token_generator.check_token(user, token=self.token):
            kwargs["user"] = user
        else:
            messages.error(self.request, "Ссылка для восстановления пароля недействительна.")

        return kwargs

    def form_valid(self, form):
        form.save()
        messages.success(self.request, "Пароль успешно изменен!")
        return super().form_valid(form)


class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    model = User
    form_class = UserUpdateForm
    template_name = "users/profile_edit.html"
    success_url = reverse_lazy("users:profile")

    def get_object(self):
        return self.request.user

    def form_valid(self, form):
        messages.success(self.request, "Профиль успешно обновлен!")
        return super().form_valid(form)


@login_required
def profile_edit_comprehensive(request):
    user = request.user
    user_profile, created = UserProfile.objects.get_or_create(user=user)

    if request.method == "POST":
        if "user_data" in request.POST:
            user_form = UserUpdateForm(request.POST, instance=user)
            profile_form = UserProfileForm(instance=user_profile)
            password_form = UserPasswordChangeForm(user)

            if user_form.is_valid():
                user_form.save()
                messages.success(request, "Основные данные успешно обновлены!")
                return redirect("users:profile_edit")

        elif "profile_data" in request.POST:
            user_form = UserUpdateForm(instance=user)
            profile_form = UserProfileForm(request.POST, request.FILES, instance=user_profile)
            password_form = UserPasswordChangeForm(user)

            if profile_form.is_valid():
                profile_form.save()
                messages.success(request, "Дополнительные данные успешно обновлены!")
                return redirect("users:profile_edit")

        elif "password_change" in request.POST:
            user_form = UserUpdateForm(instance=user)
            profile_form = UserProfileForm(instance=user_profile)
            password_form = UserPasswordChangeForm(user, request.POST)

            if password_form.is_valid():
                password_form.save()
                messages.success(request, "Пароль успешно изменен!")
                from django.contrib.auth import update_session_auth_hash

                update_session_auth_hash(request, user)
                return redirect("users:profile_edit")

    else:
        user_form = UserUpdateForm(instance=user)
        profile_form = UserProfileForm(instance=user_profile)
        password_form = UserPasswordChangeForm(user)

    context = {
        "user_form": user_form,
        "profile_form": profile_form,
        "password_form": password_form,
        "user_profile": user_profile,
    }

    return render(request, "users/profile_edit.html", context)
