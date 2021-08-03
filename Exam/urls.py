from django.contrib import admin
from django.views.generic import RedirectView
from django.urls import path, include
from django.conf.urls import url
from django.conf import settings
from django.conf.urls.static import static
from django.core.exceptions import PermissionDenied
from django.http import HttpResponse
from django.test import SimpleTestCase, override_settings


def response_error_handler(request, exception=None):
    return HttpResponse('Error handler content', status=403)


def permission_denied_view(request):
    raise PermissionDenied

handler404 = 'main.views.error_404_view'
#handler500 = 'main.views.my_custom_error_view'
#handler403 = 'main.views.my_custom_permission_denied_view'
#handler400 = 'main.views.my_custom_bad_request_view'

urlpatterns = [
    path('', include('main.urls')),
    path('student/', include('student.urls')),
    path('teacher/', include('teacher.urls')),
    path('admin/', admin.site.urls),
    url(r'^favicon\.ico$', RedirectView.as_view(url='/static/images/favicon.ico')),
]
