from django.urls import path

from emails.tasks import send_update_menu_emails

urlpatterns = [
    path(
        '', send_update_menu_emails, name='send_update_menu_emails'
    ),  # TODO remove after test
]
