from django.urls import path
from .views import  *

urlpatterns = [
    #path("test/", test_prediction, name="test_prediction"),
    path("predict/", predict_view, name="predict_view"),
    path('analytics/', analytics_framework_view, name='analytics_framework')


]
