from django.contrib import admin

from adjust_home_task.statistics.models import Statistics


class StatisticsAdmin(admin.ModelAdmin):
    list_display = (
        'date', 'channel', 'country', 'os', 'impressions',
        'clicks', 'installs', 'spend', 'revenue',
    )
    list_filter = ('date', 'channel', 'country', 'os', )


admin.site.register(Statistics, StatisticsAdmin)
