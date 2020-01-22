from django.urls import path
from bets import views

urlpatterns = [
    path("", views.home, name="home"),
    path("dos", views.dos, name="dos"),
    path("ejecutar", views.ejecutar, name="ejecutar"),
    path("apuestas", views.apuestas, name="apuestas"),
    path("prediccion", views.prediccion, name="prediccion"),
    path("metodologia", views.metodologia, name="metodologia"),
    path("admin", views.admin, name="admin"),
    path("beneficiosLanzar", views.beneficiosLanzar, name="beneficiosLanzar"),
    path("prediccionesLanzar", views.prediccionesLanzar, name="prediccionesLanzar"),
    path("precision", views.precision, name="precision"),
]

