from django.db import models

from users.models import User


class Client(models.Model):
    email = models.CharField(max_length=100, unique=True, verbose_name="Email")
    full_name = models.CharField(max_length=100, verbose_name="ФИО")
    comment = models.TextField(verbose_name="Комментарий", blank=True, null=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="clients", verbose_name="Владелец")

    class Meta:
        db_table = "client"
        verbose_name = "Клиент"
        verbose_name_plural = "Клиенты"

    def __str__(self):
        return f"{self.full_name}: {self.email}"


class Message(models.Model):
    topic = models.CharField(max_length=260, verbose_name="Тема")
    body = models.TextField(verbose_name="Сообщение")
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="messages", verbose_name="Владелец")

    class Meta:
        db_table = "message"
        verbose_name = "Сообщение"
        verbose_name_plural = "Сообщения"

    def __str__(self):
        return self.topic


class Status(models.TextChoices):
    CREATED = "created", "Создана"
    STARTED = "started", "Запущена"
    COMPLETED = "completed", "Завершена"
    SUCCESS = "success", "Успешно"
    FAILED = "failed", "Не успешно"


class Mailing(models.Model):
    start_time = models.DateTimeField(verbose_name="Время начала отправки")
    end_time = models.DateTimeField(verbose_name="Время окончания отправки")
    status = models.CharField(max_length="10", choices=Status.choices, default=Status.CREATED, verbose_name="Статус")
    message = models.ForeignKey(Message, on_delete=models.CASCADE, verbose_name="Сообщение")
    clients = models.ManyToManyField(Client, verbose_name="Получатели")
    owner = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Владелец")

    class Meta:
        db_table = "mailing"
        verbose_name = "Рассылка"
        verbose_name_plural = "Рассылки"

    def __str__(self):
        return f"Рассылка: {self.id} - {self.get_status_display()}"


class MailingAttempt(models.Model):
    attempt_time = models.DateTimeField(auto_now_add=True, verbose_name="Время попытки")
    status = models.CharField(max_length=7, choices=Status.choices, verbose_name="Статус")
    mail_server_response = models.TextField(verbose_name="Ответ сервера", blank=True, null=True)
    mailing = models.ForeignKey(Mailing, on_delete=models.CASCADE, verbose_name="Рассылка")

    class Meta:
        verbose_name = "Попытка рассылки"
        verbose_name_plural = "Попытки рассылки"
        ordering = ["-attempt_time"]
