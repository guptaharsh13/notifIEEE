from django.urls import path
from . import views

urlpatterns = [
    path("commands/plan/", view=views.PlanCommand.as_view(), name="planCommand"),
    path("events/", view=views.Events.as_view(), name="events"),
]
