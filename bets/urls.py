from django.urls import path
from bets import views

urlpatterns = [
    path("", views.home, name="home"),
    path("dos", views.dos, name="dos"),
    path("ejecutar", views.ejecutar, name="ejecutar"),
    path("apuestas", views.apuestas, name="apuestas"),
]

