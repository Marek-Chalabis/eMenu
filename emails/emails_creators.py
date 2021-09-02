from datetime import datetime, timedelta
from typing import List

from django.db.models import Q

from api.models import Dish
from emails.emails_utils import Email, EmailMixins, MassEmailABC
from emenu.settings import env


class UpdateNewDishesFromYesterday(EmailMixins, MassEmailABC):
    def prepare_mass_emails(self) -> List[Email]:
        subject = 'New or modified dishes'
        message = self._get_message()
        return [
            Email(
                subject=subject,
                message=message,
                from_email=env('EMAIL_HOST_USER'),
                recipient_list=[user_email],
            )
            for user_email in self.all_active_users_emails
        ]

    def _get_message(self) -> str:
        yesterday = datetime.now() - timedelta(days=1)
        new_or_modified_menus = Dish.objects.filter(
            Q(created__gte=yesterday) | Q(modified__gte=yesterday)
        ).values_list('name', 'id')
        dishes = ' '.join(
            {
                f'{dish_name}({dish_id})'
                for dish_name, dish_id in new_or_modified_menus
            }
        )
        if dishes:
            return f'Following dishes were added or modified: {dishes}.'
        return 'There are no new or modified dishes from yesterday.'
