from django.urls import path
from . import views

urlpatterns = [
    path("fire/<str:trigger_code>/", views.fire_trigger, name="fire-trigger"),
    path("triggers/", views.list_triggers, name="list-triggers"),
    path("templates/", views.list_templates, name="list-templates"),
]
