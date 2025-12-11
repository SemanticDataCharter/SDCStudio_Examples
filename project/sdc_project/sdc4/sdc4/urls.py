"""
URL configuration for sdc4 project.
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path('statepopulation/', include('statepopulation.urls', namespace='statepopulation')),
    path('test_data3/', include('test_data3.urls', namespace='test_data3')),
    path('', views.index, name='index'),
    path('admin/', admin.site.urls),
    path('docs/', include('core.urls', namespace='docs')),
    # App URLs will be added by AppGen
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
