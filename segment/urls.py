from django.urls import path
from . import views

urlpatterns = [
    path('', views.predict_segment, name='segment_home'),
]
