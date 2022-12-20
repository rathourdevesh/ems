"""ems_handler URL Configuration

This file contains all the url_patterns for ems handler app.
"""
from django.urls import path

from . import views

urlpatterns = [
    path("create-elavators", views.create_elevators, name="create-elevators"),
    path("get-elavators", views.get_elevators, name="get-elevators"),
    path("assign-elavator", views.assign_elevator, name="assign-elevator"),
    path("update-floor", views.update_user_request, name="update-floor"),
    path("mark-maintaince", views.mark_maintaince, name="mark-maintaince")
]