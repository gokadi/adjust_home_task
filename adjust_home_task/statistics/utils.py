from django.db.models import QuerySet, Sum, F, ExpressionWrapper, FloatField


# Can be refactored to class in future to save parameters once


def filter_statistics(queryset: QuerySet, parameters: dict) -> QuerySet:
    return queryset.filter(
        date__gte=parameters['date_from'],
        date__lt=parameters['date_to'],
        channel__in=parameters['channels'],
        country__in=parameters['countries'],
        os__in=parameters['os'],
    )


def group_statistics(queryset: QuerySet, parameters: dict) -> QuerySet:
    return queryset.values(*parameters['group_by']).annotate(
        impressions=Sum('impressions'),
        clicks=Sum('clicks'),
        installs=Sum('installs'),
        spend=Sum('spend', output_field=FloatField()),
        revenue=Sum('revenue', output_field=FloatField()),
        # Please note that SQLite3 does not support decimal fields
        # internally, so it will be FloatField with extra decimal digits
        cpi=ExpressionWrapper(F('spend') / F('installs'), FloatField()),
    )


def sort_statistics(queryset: QuerySet, parameters: dict) -> QuerySet:
    if not parameters['order_by']:
        return queryset.order_by()

    return queryset.order_by(parameters['order_by'])


def get_report_data(queryset: QuerySet, parameters: dict) -> list:
    if not parameters['group_by']:
        fields_list = [
            'date', 'channel', 'country', 'os', 'impressions',
            'clicks', 'installs', 'spend', 'revenue', 'cpi'
        ]
    else:
        fields_list = [
            *parameters['group_by'], 'impressions',
            'clicks', 'installs', 'spend', 'revenue', 'cpi'
        ]

    return queryset.values_list(*fields_list)


def prepare_report_in_csv(report_in_list: list, parameters: dict) -> str:
    report_in_csv = ','.join(parameters['group_by'] or [
        'date', 'channel', 'country', 'os'
    ]) + ',impressions,clicks,installs,spend,revenue,cpi\n'
    for entry in report_in_list:
        entry_in_csv = ','.join(str(field) for field in entry)
        report_in_csv += f'{entry_in_csv}\n'

    return report_in_csv
