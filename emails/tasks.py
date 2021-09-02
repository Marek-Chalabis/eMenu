from celery import shared_task
from django.core.mail import send_mass_mail

from emails.emails_creators import UpdateNewDishesFromYesterday


@shared_task
def send_update_dish_emails() -> None:
    send_mass_mail(UpdateNewDishesFromYesterday().prepare_mass_emails())
