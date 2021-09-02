import os
from unittest import mock
from unittest.mock import patch, PropertyMock

import pytest

from api.models import Dish
from api.tests.test_utils import get_random_date
from emails.emails_creators import UpdateNewDishesFromYesterday

from datetime import datetime, timedelta

from emails.emails_utils import Email


@pytest.mark.django_db()
class TestUpdateNewDishesFromYesterday:
    def test__get_message_no_dishes(self):
        assert (
            UpdateNewDishesFromYesterday()._get_message()
            == 'There are no new or modified dishes from yesterday.'
        )

    def test__get_message(self):
        date_from_yesterday = get_random_date(
            start_date=datetime.now() - timedelta(days=1)
        )
        date_before_yesterday = datetime.now() - timedelta(days=10)

        created_new_dish = Dish.objects.create(
            name='created_new_dish',
            price=1,
            preparation_time='21:37',
            vegetarian=False,
        )
        Dish.objects.filter(pk=created_new_dish.pk).update(
            created=date_from_yesterday, modified=date_from_yesterday
        )

        created_old_dish = Dish.objects.create(
            name='created_old_dish',
            price=1,
            preparation_time='21:37',
            vegetarian=False,
        )
        Dish.objects.filter(pk=created_old_dish.pk).update(
            created=date_before_yesterday, modified=date_before_yesterday
        )

        modified_old_dish = Dish.objects.create(
            name='modified_old_dish',
            price=1,
            preparation_time='21:37',
            vegetarian=False,
        )
        Dish.objects.filter(pk=modified_old_dish.pk).update(
            created=date_before_yesterday, modified=date_from_yesterday
        )
        expected_return = UpdateNewDishesFromYesterday()._get_message()
        assert all(
            dish in expected_return
            for dish in {'created_new_dish(26)', 'modified_old_dish(28)'}
        )

    @mock.patch.dict(os.environ, {"EMAIL_HOST_USER": "test_host_email@vp.pl"})
    @patch(
        'emails.emails_creators.EmailMixins.all_active_users_emails',
        new_callable=PropertyMock,
        return_value=['test@vp.pl'],
    )
    @patch(
        'emails.emails_creators.UpdateNewDishesFromYesterday._get_message',
        return_value='test_message',
    )
    def test_prepare_mass_emails(
        self, mock_all_active_users_emails, mock__get_message
    ):
        assert UpdateNewDishesFromYesterday().prepare_mass_emails() == [
            Email(
                subject='New or modified dishes',
                message='test_message',
                from_email='test_host_email@vp.pl',
                recipient_list=['test@vp.pl'],
            )
        ]
