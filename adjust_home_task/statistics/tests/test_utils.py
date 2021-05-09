from datetime import date

import pytest
from mixer.backend.django import mixer

from adjust_home_task.statistics.models import Statistics
from adjust_home_task.statistics.utils import (
    filter_statistics, group_statistics,
    sort_statistics, get_report_data, prepare_report_in_csv
)

pytestmark = pytest.mark.django_db(transaction=True)


def test_filter_statistics():
    filtered_queryset = filter_statistics(Statistics.objects.all(), {
        'date_from': date.fromtimestamp(0),
        'date_to': date.fromtimestamp(0),
        'channels': ['facebook'],
        'countries': ['US'],
        'os': ['ios']
    })

    assert (
        str(filtered_queryset.query) == (
            'SELECT "statistics_statistics"."id", '
            '"statistics_statistics"."date", '
            '"statistics_statistics"."channel", '
            '"statistics_statistics"."country", '
            '"statistics_statistics"."os", '
            '"statistics_statistics"."impressions", '
            '"statistics_statistics"."clicks", '
            '"statistics_statistics"."installs", '
            '"statistics_statistics"."spend", '
            '"statistics_statistics"."revenue" '
            'FROM "statistics_statistics" '
            'WHERE ("statistics_statistics"."channel" IN (facebook) AND '
            '"statistics_statistics"."country" IN (US) AND '
            '"statistics_statistics"."date" >= 1970-01-01 AND '
            '"statistics_statistics"."date" < 1970-01-01 AND '
            '"statistics_statistics"."os" IN (ios)) '
            'ORDER BY "statistics_statistics"."date" ASC'
        )
    )


def test_group_statistics():
    grouped_queryset = group_statistics(
        Statistics.objects.all(), {'group_by': ['channel', 'date']}
    )

    assert (
        'GROUP BY "statistics_statistics"."channel", '
        '"statistics_statistics"."date"'
    ) in str(grouped_queryset.query)


def test_sort_statistics_no_parameter_order_by():
    sorted_statistics = sort_statistics(
        Statistics.objects.all(), {'order_by': None}
    )

    assert 'ORDER BY' not in str(sorted_statistics.query)


def test_sort_statistics_with_parameter_order_by():
    sorted_statistics = sort_statistics(
        Statistics.objects.all(), {'order_by': 'date'}
    )

    assert 'ORDER BY "statistics_statistics"."date"' in str(
        sorted_statistics.query
    )


def test_get_report_data_no_parameter_group_by_should_get_all_fields():
    mixer.blend(Statistics)
    fields_list = get_report_data(group_statistics(
        Statistics.objects.all(), {'group_by': []}
    ), {'group_by': []})

    assert len(fields_list[0]) == 10


def test_get_report_data_with_parameter_group_by():
    mixer.blend(Statistics)
    fields_list = get_report_data(group_statistics(
        Statistics.objects.all(), {'group_by': ['channel', 'date']}
    ), {'group_by': ['channel', 'date']})

    assert len(fields_list[0]) == 8


def test_prepare_report_in_csv_non_empty_group_by():
    report = prepare_report_in_csv(
        [['facebook', '1', '1', '1', '1', '1', '1']],
        {'group_by': ['channel']}
    )

    assert report == (
        'channel,impressions,clicks,installs,spend,revenue,cpi\n'
        'facebook,1,1,1,1,1,1\n'
    )


def test_prepare_report_in_csv_empty_group_by():
    report = prepare_report_in_csv([[]], {'group_by': []})

    assert report == (
        'date,channel,country,os,impressions,clicks,'
        'installs,spend,revenue,cpi\n\n'
    )
