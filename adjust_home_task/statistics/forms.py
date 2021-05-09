from datetime import date
from typing import List, Optional

from django.core.exceptions import ValidationError
from django.forms import forms, fields

from adjust_home_task.statistics.models import Statistics


class GetReportQueryForm(forms.Form):
    date_from = fields.DateField(required=False)
    date_to = fields.DateField(required=False)
    channels = fields.CharField(required=False)
    countries = fields.CharField(required=False)
    os = fields.CharField(required=False)
    group_by = fields.CharField(required=False)
    order_by = fields.CharField(required=False)

    def clean(self):
        cleaned_data = super().clean()
        if cleaned_data['date_from'] > cleaned_data['date_to']:
            raise ValidationError('`date_from` should be before `date_to`')

    def clean_date_from(self) -> date:
        return self.cleaned_data['date_from'] or date.fromtimestamp(0)

    def clean_date_to(self) -> date:
        return self.cleaned_data['date_to'] or date.today()

    def clean_channels(self) -> List[str]:
        if channels := self.cleaned_data['channels']:
            channels = channels.split(',')
        return channels or [
            channel[0] for channel in Statistics.CHANNEL_CHOICES
        ]

    def clean_countries(self) -> List[str]:
        if countries := self.cleaned_data['countries']:
            countries = countries.split(',')
        return countries or [
            country[0] for country in Statistics.COUNTRY_CHOICES
        ]

    def clean_os(self) -> List[str]:
        if os := self.cleaned_data['os']:
            os = os.split(',')
        return os or [os[0] for os in Statistics.OS_CHOICES]

    def clean_group_by(self) -> List[str]:
        valid_choices = {'date', 'channel', 'country', 'os'}
        if group_by := self.cleaned_data['group_by']:
            group_by = group_by.split(',')
        else:
            return []

        if not set(group_by).issubset(valid_choices):
            raise ValidationError(
                f'`group_by` field should be one of: {valid_choices}'
            )

        return group_by

    def clean_order_by(self) -> Optional[str]:
        model_fields = [
            field for field in Statistics._meta.get_fields()
            if field.name != 'id'
        ]
        valid_choices = [
            *[field.name for field in model_fields],
            *[f'-{field.name}' for field in model_fields],
            'cpi', '-cpi'
        ]
        order_by = self.cleaned_data['order_by']

        if order_by and order_by not in valid_choices:
            raise ValidationError(
                f'`order_by` field should be one of: {valid_choices}'
            )

        return order_by
