from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.forms import PasswordResetForm, SetPasswordForm, UserChangeForm, UserCreationForm

from .models import User, UserProfile


class UserRegisterForm(UserCreationForm):
    email = forms.EmailField(
        required=True,
    )

    class Meta:
        model = User
        fields = ("email", "password1", "password2")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["email"].widget.attrs.update({"class": "form-control", "placeholder": "Введите ваш email"})
        self.fields["password1"].widget.attrs.update({"class": "form-control", "placeholder": "Введите пароль"})
        self.fields["password2"].widget.attrs.update({"class": "form-control", "placeholder": "Подтвердите пароль"})

    def clean_email(self):
        email = self.cleaned_data.get("email")
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Пользователь с таким email существует")
        return email


class UserLoginForm(forms.Form):
    email = forms.EmailField(
        label="Email",
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'Введите ваш email'
        })
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={"class": "form-control", "placeholder": "Введите пароль"})
    )

    def clean(self):
        email = self.cleaned_data.get("email")
        password = self.cleaned_data.get("password")

        if email and password:
            try:
                user = User.objects.get(email=email)
                user = authenticate(email=user.email, password=password)

                if user is None:
                    raise forms.ValidationError("Неверный email или пароль")

                if not user.is_active:
                    raise forms.ValidationError("Аккаунт заблокирован")

                self.cleaned_data["user"] = user
            except User.DoesNotExist:
                raise forms.ValidationError("Неверный email или пароль")
        return self.cleaned_data


class CustomPasswordResetForm(PasswordResetForm):
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={"class": "form-control", "placeholder": "Введите ваш email"})
    )


class CustomSetPasswordForm(SetPasswordForm):
    new_password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={"class": "form-control", "placeholder": "Введите новый пароль"})
    )
    new_password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={"class": "form-control", "placeholder": "Подтвердите новый пароль"})
    )


class UserUpdateForm(UserChangeForm):
    password = None

    class Meta:
        model = User
        fields = ["email", "first_name", "last_name"]
        widgets = {
            "email": forms.EmailInput(attrs={"class": "form-control", "placeholder": "Введите email"}),
            "first_name": forms.TextInput(attrs={"class": "form-control", "placeholder": "Введите имя"}),
            "last_name": forms.TextInput(attrs={"class": "form-control", "placeholder": "Введите фамилию"}),
        }

    def clean_email(self):
        email = self.cleaned_data.get("email")
        if User.objects.filter(email=email).exclude(pk=self.instance.pk).exists():
            raise forms.ValidationError("Пользователь с таким email уже существует.")
        return email


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ["avatar", "phone_number", "country", "company"]
        widgets = {
            "phone_number": forms.TextInput(attrs={"class": "form-control", "placeholder": "+7 (XXX) XXX-XX-XX"}),
            "country": forms.TextInput(attrs={"class": "form-control", "placeholder": "Введите страну"}),
            "company": forms.TextInput(attrs={"class": "form-control", "placeholder": "Введите название компании"}),
        }

    def clean_phone_number(self):
        phone_number = self.cleaned_data.get("phone_number")
        if phone_number:
            import re

            phone_pattern = r"^\+?1?\d{9,15}$"
            if not re.match(phone_pattern, phone_number.replace(" ", "").replace("-", "")):
                raise forms.ValidationError("Введите корректный номер телефона.")
        return phone_number


class UserPasswordChangeForm(forms.Form):
    current_password = forms.CharField(
        label="Текущий пароль",
        widget=forms.PasswordInput(attrs={"class": "form-control", "placeholder": "Введите текущий пароль"}),
    )
    new_password1 = forms.CharField(
        label="Новый пароль",
        widget=forms.PasswordInput(attrs={"class": "form-control", "placeholder": "Введите новый пароль"}),
    )
    new_password2 = forms.CharField(
        label="Подтверждение нового пароля",
        widget=forms.PasswordInput(attrs={"class": "form-control", "placeholder": "Повторите новый пароль"}),
    )

    def __init__(self, user, *args, **kwargs):
        self.user = user
        super().__init__(*args, **kwargs)

    def clean_current_password(self):
        current_password = self.cleaned_data.get("current_password")
        if not self.user.check_password(current_password):
            raise forms.ValidationError("Текущий пароль введен неверно.")
        return current_password

    def clean_new_password2(self):
        new_password1 = self.cleaned_data.get("new_password1")
        new_password2 = self.cleaned_data.get("new_password2")

        if new_password1 and new_password2 and new_password1 != new_password2:
            raise forms.ValidationError("Новые пароли не совпадают.")

        return new_password2

    def save(self):
        new_password = self.cleaned_data.get("new_password1")
        self.user.set_password(new_password)
        self.user.save()
