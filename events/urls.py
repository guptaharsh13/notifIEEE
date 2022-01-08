from django.urls import path
from . import views

urlpatterns = [path("", view=views.Events.as_view(), name="events")]
