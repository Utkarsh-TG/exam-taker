from django.contrib import admin
from django.views.generic import RedirectView
from django.urls import path, include
from django.conf.urls import url
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    url(r'^favicon\.ico$', RedirectView.as_view(url='/static/images/favicon.ico')),
    path('', include('main.urls')),
    path('student/', include('student.urls')),
    path('teacher/', include('teacher.urls')),
]
