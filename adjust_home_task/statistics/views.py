import json
from datetime import datetime

from django.core.handlers.wsgi import WSGIRequest
from django.http import (
    HttpResponseNotAllowed, HttpResponse, HttpResponseBadRequest
)
from django.template.response import SimpleTemplateResponse

from adjust_home_task.statistics.forms import GetReportQueryForm
from adjust_home_task.statistics.models import Statistics
from adjust_home_task.statistics.utils import (
    filter_statistics, group_statistics, sort_statistics,
    get_report_data, prepare_report_in_csv
)


def get_report(request: WSGIRequest, *args, **kwargs) -> HttpResponse:
    if not request.method == "GET":
        return HttpResponseNotAllowed(permitted_methods=["GET"])
    # Actually, it'll be a good idea to cache requests
    # with their results to prevent too many requests to DB
    get_report_query_form = GetReportQueryForm(request.GET)
    if not get_report_query_form.is_valid():
        return HttpResponseBadRequest(
            content=json.dumps({'errors': get_report_query_form.errors})
        )

    cleaned_data = get_report_query_form.cleaned_data
    initial_queryset = Statistics.objects.all()

    filtered_queryset = filter_statistics(initial_queryset, cleaned_data)
    grouped_queryset = group_statistics(filtered_queryset, cleaned_data)
    sorted_queryset = sort_statistics(grouped_queryset, cleaned_data)
    report_data = get_report_data(sorted_queryset, cleaned_data)
    report_in_csv = prepare_report_in_csv(report_data, cleaned_data)

    view_mode = request.GET.get('view_mode', '')
    if view_mode == 'download':
        # If reports becomes very huge, use StreamingHttpResponse instead
        response = HttpResponse(content_type='text/csv', content=report_in_csv)
        response['Content-Disposition'] = (
            f'attachment; filename="report_{datetime.now()}.csv"'
        )
    elif view_mode == 'ui':
        response = SimpleTemplateResponse(
            template='report.html', context={
                'data': [row.split(',') for row in report_in_csv.split('\n')]
            }
        )
    else:
        response = HttpResponse(content=json.dumps({'report': report_in_csv}))

    return response
