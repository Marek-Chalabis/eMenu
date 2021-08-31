from abc import ABC, abstractmethod
from typing import List, Set, NamedTuple


from django.contrib.auth.models import User

from django.db.models import Q

from api.models import Dish
from emenu.settings import env
from datetime import datetime, timedelta


class Email(NamedTuple):
    subject: str
    message: str
    from_email: str
    recipient_list: List[str]


class EmailMixins:
    @property
    def all_active_users_emails(self) -> List[str]:
        return (
            User.objects.filter(is_active=True)
            .exclude(email='')
            .values_list('email', flat=True)
        )


class MassEmailABC(ABC):
    @abstractmethod
    def prepare_mass_emails(self) -> Set[Email]:
        """Returns Set with emails data."""


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
            Q(added_date__gte=yesterday) | Q(modified_date__gte=yesterday)
        ).values_list('name', 'id')
        dishes = " ".join(
            {
                f'{dish_name}({dish_id})'
                for dish_name, dish_id in new_or_modified_menus
            }
        )
        return f'Following dishes were added or modified: {dishes}.'
