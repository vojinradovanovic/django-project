from django.urls import path

from . import views

urlpatterns = [
    path("cost_estimate/", views.cost_estimate, name="cost_estimate"),
    path("immigration/", views.immigration, name="immigration"),
]