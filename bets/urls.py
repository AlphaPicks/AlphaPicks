from django.urls import path
from bets import views

urlpatterns = [
    path("", views.home, name="home"),
    path("dos", views.dos, name="dos"),
    path("ejecutar", views.ejecutar, name="ejecutar"),
    path("apuestas", views.apuestas, name="apuestas"),
    path("prediccion", views.prediccion, name="prediccion"),
    path("metodologia", views.metodologia, name="metodologia"),
    path("admin22", views.admin22, name="admin22"),
    #path("beneficiosLanzar", views.beneficiosLanzar, name="beneficiosLanzar"),
    path("prediccionesLanzar", views.prediccionesLanzar, name="prediccionesLanzar"),
    #path("historicoLanzar", views.historicoLanzar, name="historicoLanzar"),
    path("historicoBeneficiosLanzar", views.historicoBeneficiosLanzar, name="historicoBeneficiosLanzar"),
    path("historico20202021", views.historico20202021, name="historico20202021"),
    path("historico20192020", views.historico20192020, name="historico20192020"),
    path("historico20182019", views.historico20182019, name="historico20182019"),
    path("historico20172018", views.historico20172018, name="historico20172018"),
    path("historico20162017", views.historico20162017, name="historico20162017"),
    path("historico20152016", views.historico20152016, name="historico20152016"),
    path("historico20142015", views.historico20142015, name="historico20142015"),
    path("historico20132014", views.historico20132014, name="historico20132014"),
    path("historico20122013", views.historico20122013, name="historico20122013"),
    path("precision", views.precision, name="precision"),
]

