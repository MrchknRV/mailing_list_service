from django.core.management.base import BaseCommand

from mailing.models import Mailing
from mailing.services import EmailService


class Command(BaseCommand):
    help = "Отправка рассылки по ID"

    def add_arguments(self, parser):
        parser.add_argument("mailing_id", type=int, help="ID рассылки для отправки")

    def handle(self, *args, **options):
        mailing_id = options["mailing_id"]

        try:
            mailing = Mailing.objects.get(pk=mailing_id)
            self.stdout.write(f"Начинаем отправку рассылки #{mailing_id}...")

            successful_sends, failed_sends = EmailService.send_mass_mailing(mailing)

            self.stdout.write(
                self.style.SUCCESS(
                    f"Рассылка #{mailing_id} завершена! " f"Успешно: {successful_sends}, Неудачно: {failed_sends}"
                )
            )

        except Mailing.DoesNotExist:
            self.stdout.write(self.style.ERROR(f"Рассылка с ID {mailing_id} не найдена"))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"Ошибка при отправке рассылки: {str(e)}"))
