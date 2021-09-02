from abc import ABC, abstractmethod
from typing import List, NamedTuple

from django.contrib.auth.models import User


class Email(NamedTuple):
    subject: str
    message: str
    from_email: str
    recipient_list: List[str]


class EmailMixins:
    @property
    def all_active_users_emails(self) -> List[str]:
        return list(
            User.objects.filter(is_active=True)
            .exclude(email='')
            .values_list('email', flat=True)
        )


class MassEmailABC(ABC):
    @abstractmethod
    def prepare_mass_emails(self) -> List[Email]:
        """Returns list with emails data."""
