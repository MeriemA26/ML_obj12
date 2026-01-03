from django.contrib import admin
from django.urls import path, include
from django.shortcuts import redirect

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('obj2.urls')),  # Home (was obj2)
    path('quality/', include('obj1.urls')),
    path('diabetes-risk/', include('diabetes_risk.urls')),
    path('segment/', include('segment.urls')),
    path('predictor/', include('predictor.urls')),  # RF Predictor
    path('obesity/', include('obesity_predictor.urls')),
]

from django.conf import settings
from django.conf.urls.static import static

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS[0])
