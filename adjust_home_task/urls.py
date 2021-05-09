from django.apps import apps
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),

]

if apps.is_installed('adjust_home_task.statistics'):
    urlpatterns += [
        path(
            'statistics/',
            include('adjust_home_task.statistics.urls', namespace='statistics')
        )
    ]

if settings.DEBUG:
    urlpatterns = urlpatterns + static(
        settings.STATIC_URL, document_root=settings.STATIC_ROOT
    )
