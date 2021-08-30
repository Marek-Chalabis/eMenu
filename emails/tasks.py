from celery import shared_task
from celery.utils.log import get_task_logger
from django.contrib.auth.models import User
from django.core.mail import send_mail

logger = get_task_logger(__name__)

#
# @shared_task
# def send_email_task():
#     send_mail(
#         'Celery Task Worked!',
#         'This is proof the task worked!',
#         'zulaber@gmail.com',
#         ['zulaber@gmail.com'],
#     )


@shared_task
def send_update_menu_emails(request):  # todo remove request
    user_emails = (
        User.objects.filter(is_active=True)
        .exclude(email='')
        .values_list('email', flat=True)
    )
    print(user_emails, 'KILL ME I BEG YOU')
