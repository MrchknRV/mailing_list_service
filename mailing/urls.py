from django.urls import path

from . import views

app_name = "mailing"

urlpatterns = [
    path("", views.IndexView.as_view(), name="index"),
    path("clients/", views.ClientListView.as_view(), name="client_list"),
    path("clients/create/", views.ClientCreateView.as_view(), name="client_create"),
    path("clients/<int:pk>/", views.ClientDetailView.as_view(), name="client_detail"),
    path("clients/<int:pk>/update/", views.ClientUpdateView.as_view(), name="client_update"),
    path("clients/<int:pk>/delete/", views.ClientDeleteView.as_view(), name="client_delete"),
    path("messages/", views.MessageListView.as_view(), name="message_list"),
    path("messages/create/", views.MessageCreateView.as_view(), name="message_create"),
    path("messages/<int:pk>/", views.MessageDetailView.as_view(), name="message_detail"),
    path("messages/<int:pk>/update/", views.MessageUpdateView.as_view(), name="message_update"),
    path("messages/<int:pk>/delete/", views.MessageDeleteView.as_view(), name="message_delete"),
    path("mailing/", views.MailingListView.as_view(), name="mailing_list"),
    path("mailing/create/", views.MailingCreateView.as_view(), name="mailing_create"),
    path("mailing/<int:pk>/", views.MailingDetailView.as_view(), name="mailing_detail"),
    path("mailing/<int:pk>/update/", views.MailingUpdateView.as_view(), name="mailing_update"),
    path("mailing/<int:pk>/delete/", views.MailingDeleteView.as_view(), name="mailing_delete"),
]
