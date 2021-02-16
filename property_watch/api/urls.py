from django.urls import path
from api import views

urlpatterns = [
    path('seed/', views.seed),
    path('properties/', views.properties_list),
]