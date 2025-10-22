from django.conf import settings
from django.core.mail import EmailMultiAlternatives, send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags

from .models import Mailing, MailingAttempt, Status


class EmailService:

    @staticmethod
    def send_verification_email(user, verification_url):
        subject = "Подтверждение email - Система рассылок"
        html_message = render_to_string(
            "users/email_verification.html",
            {
                "user": user,
                "verification_url": verification_url,
            },
        )

        plain_message = strip_tags(html_message)

        try:
            send_mail(
                subject,
                plain_message,
                settings.DEFAULT_FROM_EMAIL,
                [user.email],
                html_message=html_message,
                fail_silently=False,
            )

            return True

        except Exception:
            return False

    @staticmethod
    def send_mailing(mailing, client):
        try:
            subject = mailing.message.title
            body = mailing.message.body

            personal_body = body.replace("{full_name}", client.full_name)
            personal_body = personal_body.replace("{email}", client.email)

            send_mail(subject, personal_body, settings.DEFAULT_FROM_EMAIL, [client.email], fail_silently=False)

            MailingAttempt.objects.create(
                mailing=mailing, status=Status.SUCCESS, server_responce="Сообщение успешно доставлено"
            )

            return True

        except Exception as exp:
            error_message = f"Ошибка отправки: {str(exp)}"
            MailingAttempt.objects.create(mailing=mailing, status=Status.FAILED, server_response=error_message)
            return False

    @staticmethod
    def send_mass_mailing(mailings):
        clients = mailings.clients.all()
        success_sends = 0
        failed_sends = 0

        for client in clients:
            if EmailService.send_mailing(client, client):
                success_sends += 1
            else:
                failed_sends += 1

        if success_sends > 0 and mailings.status == Status.CREATED:
            mailings.status = Status.STARTED
            mailings.save()

        return success_sends, failed_sends

    @staticmethod
    def send_password_reset_email(user, reset_url):

        subject = "Восстановление пароля - Система рассылок"

        html_message = render_to_string(
            "users/email_password_reset.html",
            {
                "user": user,
                "reset_url": reset_url,
            },
        )

        plain_message = strip_tags(html_message)

        try:
            send_mail(
                subject=subject,
                message=plain_message,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[user.email],
                html_message=html_message,
                fail_silently=False,
            )

            return True

        except Exception:
            return False
