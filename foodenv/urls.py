from django.contrib import admin
from django.urls import path, include
from django.shortcuts import redirect

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('food_desert.urls')),  # Home (was obj2)
    path('quality/', include('food_quality.urls')),
    path('diabetes-risk/', include('diabetes_risk.urls')),
    path('segment/', include('segment.urls')),
    path('predictor/', include('predictor.urls')),  # RF Predictor
    path('obesity/', include('obesity_predictor.urls')),
    path('access/', include('mlapp.urls')),  # KNN Limited Access from ayoub
]

from django.conf import settings
from django.conf.urls.static import static

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS[0])
