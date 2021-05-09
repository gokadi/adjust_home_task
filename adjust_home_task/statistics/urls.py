from django.urls import path

from adjust_home_task.statistics.views import get_report

app_name = 'statistics'

urlpatterns = [
    path('get_report/', get_report, name="get_report"),
]
