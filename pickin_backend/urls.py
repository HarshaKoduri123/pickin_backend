from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView

from django.urls import re_path
urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('pickin_app.urls')),
    re_path('.*', TemplateView.as_view(template_name='index.html')),
    #path('', include('pickin_app.urls')),
]

if settings.DEBUG:
  urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)