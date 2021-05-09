from datetime import date
from typing import Any, Optional

import pytest

from adjust_home_task.statistics.forms import GetReportQueryForm
from adjust_home_task.statistics.models import Statistics


class TestGetReportQueryForm:
    def test_date_from_after_date_to(self):
        form = GetReportQueryForm(
            {'date_from': date.today(), 'date_to': date.fromtimestamp(0)}
        )
        form.is_valid()

        assert (
            '`date_from` should be before `date_to`' in form.errors['__all__']
        )

    @pytest.mark.parametrize(('field_name', 'field_value', 'expected_value'), (
        ('channels', 'some,value', ['some', 'value']),
        ('channels', None, [c[0] for c in Statistics.CHANNEL_CHOICES]),
        ('countries', 'some,value', ['some', 'value']),
        ('countries', None, [c[0] for c in Statistics.COUNTRY_CHOICES]),
        ('os', 'some,value', ['some', 'value']),
        ('os', None, [c[0] for c in Statistics.OS_CHOICES]),
    ))
    def test_common_fields_present_or_absent(
        self, field_name: str, field_value: Any, expected_value: list
    ):
        form = GetReportQueryForm({field_name: field_value})
        form.is_valid()

        assert form.cleaned_data[field_name] == expected_value

    @pytest.mark.parametrize(('field_value', 'expected_value'), (
        (None, []),
        ('channel,country', ['channel', 'country']),
    ))
    def test_group_by_field_empty_or_non_empty_should_proceed(
        self, field_value: Optional[str], expected_value: list
    ):
        form = GetReportQueryForm({'group_by': field_value})
        form.is_valid()

        assert form.cleaned_data['group_by'] == expected_value

    def test_group_by_field_invalid_values_should_raise(self):
        form = GetReportQueryForm({'group_by': 'some bad values'})
        form.is_valid()

        assert (
            "`group_by` field should be one of: " in form.errors['group_by'][0]
        )

    @pytest.mark.parametrize(('field_value', 'expected_value'), (
        (None, ''),
        ('date', 'date'),
    ))
    def test_order_by_field_empty_or_non_empty_should_proceed(
        self, field_value: Optional[str], expected_value: str
    ):
        form = GetReportQueryForm({'order_by': field_value})
        form.is_valid()

        assert form.cleaned_data['order_by'] == expected_value

    def test_order_by_field_invalid_values_should_raise(self):
        form = GetReportQueryForm({'order_by': 'some bad values'})
        form.is_valid()

        assert (
            "`order_by` field should be one of: " in form.errors['order_by'][0]
        )
