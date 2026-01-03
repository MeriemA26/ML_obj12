from django.urls import path
from .views import *

urlpatterns = [
    #path("test/", test_prediction, name="test_prediction"),
    path("predict/", predict_obesity, name="predict_obesity"),
    path("", predict_obesity, name="obesity_home"),  # Added default route
    path('analytics/', analytics_framework, name='analytics_framework')


]
