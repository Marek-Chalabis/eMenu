import pytest
from django.contrib.auth.models import User

from emails.emails_utils import EmailMixins


@pytest.mark.django_db()
class TestEmailMixins:
    def test_email_mixin(self):
        User.objects.create(username='test_username_1', email='test@vp.pl')
        User.objects.create(
            username='test_username_2', email='test_2@vp.pl', is_active=False
        )
        User.objects.create(username='test_username_3')
        assert EmailMixins().all_active_users_emails == ['test@vp.pl']
