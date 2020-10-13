from django.shortcuts import render
from django.http import HttpResponse
from .forms import NameForm
from .forms import Prediccion
from django.templatetags.static import static
from django.contrib.staticfiles.storage import staticfiles_storage
import os
import io
import csv
import pickle
from datetime import datetime
from io import BytesIO
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib
import requests
import pandas as pd
import numpy as np
from urllib.request import urlopen
from zipfile import ZipFile
from django.utils import timezone
from django.core import serializers
from datetime import datetime
from datetime import date
from datetime import timedelta
from bets.models import Beneficios
from bets.models import BeneficiosMes
from bets.models import Predicciones
from bets.models import Historico


CAPITAL_INICIAL_TOTAL_APUESTAS = 10
CAPITAL_APORTADO = {"1213": 10, "1314": 10, "1415": 10, "1516": 10, "1617": 5, "1718": 2, "1819": 10, "1920": 14, "2021": 10}
TEMPORADA_ACTUAL = 2021
LIGAS = ['D1','D2', 'E0', 'EC', 'F2', 'G1', 'I1', "SC1", "SP1", "SP2", "T1"]



def send_email(user, pwd, recipient, bcc, subject, body):
    FROM = user
    TO = recipient if isinstance(recipient, list) else [recipient]
    SUBJECT = subject
    TEXT = body
    message = """From: %s\nTo: %s\nSubject: %s\n\n%s
    """ % (FROM, ", ".join(TO), SUBJECT, TEXT)
    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.ehlo()
        server.starttls()
        server.login(user, pwd)
        server.sendmail(FROM, TO, message)
        server.close()
        print ('successfully sent the mail')
    except:
        print ("failed to send mail")

def home(request):
    return render(request, 'home.html')

def admin22(request):
    return render(request, 'admin22.html')

def dos(request):
    return HttpResponse("Hello, Django 2!")

def ejecutar(request):
     return render(request, 'ejecutar.html')

def metodologia(request):
    return render(request, 'metodologia.html')

def apuestas2(request):
    return render(request, 'apuestas.html')

def apuestas(request):
    return render(request, 'apuestas.html')

def obtenerDatosTemporada():
    df_test = pd.DataFrame()
    resp = urlopen('https://www.football-data.co.uk/mmz4281/2021/data.zip')
    zipfile = ZipFile(BytesIO(resp.read()))
    zipfile.namelist()
    LIGAS_2 =  ['D1','D2', 'E0',       'F2', 'G1', 'I1',        "SP1", "SP2", "T1"]
    #LIGAS_2 = ['D1','D2', 'E0', 'EC', 'F2', 'G1', 'I1', "SC1", "SP1", "SP2", "T1"]
    for l in LIGAS_2:
        df_new = pd.read_csv(zipfile.open(l+".csv"))
        df_test = pd.concat([df_test, df_new], sort=True) 
    return df_test

def historicoBeneficiosLanzarOtrasTemporadas():
    x=1 

def historicoBeneficiosLanzar(request):
    
    return 1

def prediccionesLanzar(request):
    
    return 1

def calcular_capital_inicial():
    historico_pd = pd.DataFrame(list(Historico.objects.all().values()))
    df_bd = historico_pd
    df_bd['date'] = pd.to_datetime(df_bd['date']).apply(lambda x: x.date())
    df_bd = df_bd[df_bd['date']>date(2016,7,28)]
    for y in [2016, 2017, 2018, 2019]:
        df_bd_aux = df_bd[(df_bd['date']>date(y,7,25)) & (df_bd['date']<date(y+1,8, 2))]
        df_bd_aux = df_bd_aux.sort_values(by="date", ascending=True)
        capital_inicial=0
        maxima_deuda = 0
        date_2=0
        dinero_necesario=0
        for x in range(5,30):
            capital_inicial=x
            maxima_deuda = 0
            date_2=0
            capital_final = capital_inicial
            for indice_fila, fila in df_bd_aux.iterrows():
                capital_final = capital_final-1
                if(capital_final<maxima_deuda):
                    maxima_deuda = capital_final
                    date_2=fila["date"]
                if(fila["resultado"]==1):
                    capital_final = capital_final + fila["cuotaEmpate"]
            if ((maxima_deuda<0) & (maxima_deuda>-1)):
                dinero_necesario=x+1
        CAPITAL_APORTADO[str(y)[2:4]+str(y+1)[2:4]] = dinero_necesario+1
        CAPITAL_APORTADO["1819"] = 10
        CAPITAL_APORTADO["1718"] = 2
        CAPITAL_APORTADO["1617"] = 5
        CAPITAL_APORTADO["2021"] = CAPITAL_INICIAL_TOTAL_APUESTAS
        print(CAPITAL_APORTADO)

def precision(request):
    #calcular_capital_inicial()
    #Temporada actual
    #last_beneficio = Beneficios.objects.latest('temporada')
    last_beneficio = Beneficios.objects.filter(temporada = "2021").order_by('-id')[0]
    data_informacion = [[last_beneficio.dia, last_beneficio.capital_inicial, last_beneficio.ganancias_brutas, last_beneficio.ganancias_netas, last_beneficio.porcentaje_beneficio, last_beneficio.porcentaje_beneficio_frente_al_inicial, last_beneficio.temporada]] 
    df_data_informacion = pd.DataFrame(data_informacion, columns = ['Día',' Capital inicial', 'Ganancia brutas', 'Ganancia netas', 'Beneficio', 'Beneficio frente inicial', "Temporada"]) 
    
    #Temporada 1920
    #last_beneficio = Beneficios.objects.latest('temporada')
    last_beneficio = Beneficios.objects.filter(temporada = "1920").order_by('-id')[0]
    data_informacion = [[last_beneficio.dia, last_beneficio.capital_inicial, last_beneficio.ganancias_brutas, last_beneficio.ganancias_netas, last_beneficio.porcentaje_beneficio, last_beneficio.porcentaje_beneficio_frente_al_inicial, last_beneficio.temporada]] 
    df_data_informacion_1920 = pd.DataFrame(data_informacion, columns = ['Día',' Capital inicial', 'Ganancia brutas', 'Ganancia netas', 'Beneficio', 'Beneficio frente inicial', "Temporada"]) 

    #Temporada 1819
    last_beneficio = Beneficios.objects.filter(temporada = "1819").order_by('-id')[0]
    data_informacion = [[last_beneficio.dia, last_beneficio.capital_inicial, last_beneficio.ganancias_brutas, last_beneficio.ganancias_netas, last_beneficio.porcentaje_beneficio, last_beneficio.porcentaje_beneficio_frente_al_inicial, last_beneficio.temporada]] 
    df_data_informacion_1819 = pd.DataFrame(data_informacion, columns = ['Día',' Capital inicial', 'Ganancia brutas', 'Ganancia netas', 'Beneficio', 'Beneficio frente inicial', "Temporada"]) 
    
    #Temporada 1718
    last_beneficio = Beneficios.objects.filter(temporada = "1718").order_by('-id')[0]
    data_informacion = [[last_beneficio.dia, last_beneficio.capital_inicial, last_beneficio.ganancias_brutas, last_beneficio.ganancias_netas, last_beneficio.porcentaje_beneficio, last_beneficio.porcentaje_beneficio_frente_al_inicial, last_beneficio.temporada]] 
    df_data_informacion_1718 = pd.DataFrame(data_informacion, columns = ['Día',' Capital inicial', 'Ganancia brutas', 'Ganancia netas', 'Beneficio', 'Beneficio frente inicial', "Temporada"]) 
    
    #Temporada 1617
    last_beneficio = Beneficios.objects.filter(temporada = "1617").order_by('-id')[0]
    data_informacion = [[last_beneficio.dia, last_beneficio.capital_inicial, last_beneficio.ganancias_brutas, last_beneficio.ganancias_netas, last_beneficio.porcentaje_beneficio, last_beneficio.porcentaje_beneficio_frente_al_inicial, last_beneficio.temporada]] 
    df_data_informacion_1617 = pd.DataFrame(data_informacion, columns = ['Día',' Capital inicial', 'Ganancia brutas', 'Ganancia netas', 'Beneficio', 'Beneficio frente inicial', "Temporada"]) 
    
    #Temporada 1516
    last_beneficio = Beneficios.objects.filter(temporada = "1516").order_by('-id')[0]
    data_informacion = [[last_beneficio.dia, last_beneficio.capital_inicial, last_beneficio.ganancias_brutas, last_beneficio.ganancias_netas, last_beneficio.porcentaje_beneficio, last_beneficio.porcentaje_beneficio_frente_al_inicial, last_beneficio.temporada]] 
    df_data_informacion_1516 = pd.DataFrame(data_informacion, columns = ['Día',' Capital inicial', 'Ganancia brutas', 'Ganancia netas', 'Beneficio', 'Beneficio frente inicial', "Temporada"]) 
    
    #Temporada 1415
    last_beneficio = Beneficios.objects.filter(temporada = "1415").order_by('-id')[0]
    data_informacion = [[last_beneficio.dia, last_beneficio.capital_inicial, last_beneficio.ganancias_brutas, last_beneficio.ganancias_netas, last_beneficio.porcentaje_beneficio, last_beneficio.porcentaje_beneficio_frente_al_inicial, last_beneficio.temporada]] 
    df_data_informacion_1415 = pd.DataFrame(data_informacion, columns = ['Día',' Capital inicial', 'Ganancia brutas', 'Ganancia netas', 'Beneficio', 'Beneficio frente inicial', "Temporada"]) 
    
    #Temporada 1314
    last_beneficio = Beneficios.objects.filter(temporada = "1314").order_by('-id')[0]
    data_informacion = [[last_beneficio.dia, last_beneficio.capital_inicial, last_beneficio.ganancias_brutas, last_beneficio.ganancias_netas, last_beneficio.porcentaje_beneficio, last_beneficio.porcentaje_beneficio_frente_al_inicial, last_beneficio.temporada]] 
    df_data_informacion_1314 = pd.DataFrame(data_informacion, columns = ['Día',' Capital inicial', 'Ganancia brutas', 'Ganancia netas', 'Beneficio', 'Beneficio frente inicial', "Temporada"]) 
    
    #Temporada 1213
    last_beneficio = Beneficios.objects.filter(temporada = "1213").order_by('-id')[0]
    data_informacion = [[last_beneficio.dia, last_beneficio.capital_inicial, last_beneficio.ganancias_brutas, last_beneficio.ganancias_netas, last_beneficio.porcentaje_beneficio, last_beneficio.porcentaje_beneficio_frente_al_inicial, last_beneficio.temporada]] 
    df_data_informacion_1213 = pd.DataFrame(data_informacion, columns = ['Día',' Capital inicial', 'Ganancia brutas', 'Ganancia netas', 'Beneficio', 'Beneficio frente inicial', "Temporada"]) 

    frames = [df_data_informacion, df_data_informacion_1920, df_data_informacion_1819, df_data_informacion_1718, df_data_informacion_1617, df_data_informacion_1516, df_data_informacion_1415, df_data_informacion_1314, df_data_informacion_1213]
    df_data_evolucion = pd.concat(frames)
    historico = Historico.objects.latest('ejecucion')
    all_entries = Historico.objects.filter(ejecucion = historico.ejecucion, prediction = 1)
    first = all_entries.values_list()    
    df = pd.DataFrame(data=first, columns=['id', 'prediccion', 'date', 'home_team', 'away_team', 'resultado', "probabilidad", "cuotaEmpates", 'ejecucion', "temporada"])
    tiempoJornadaInicio = jornadaInicio(datetime.today().weekday()) + "day"
    tiempoJornadaFin = jornadaFin(datetime.today().weekday()) + "day"
    df_last_jornada = df[(df.date > (datetime.now().date() - pd.to_timedelta(tiempoJornadaInicio))) & (df.date < (datetime.now().date() - pd.to_timedelta(tiempoJornadaFin)))]
    capital_inicial_total2 = round(len(df_last_jornada[df_last_jornada["prediccion"] == 1].index), 2)
    ganancias_totales = round(df_last_jornada[(df_last_jornada["prediccion"] == 1) & (df_last_jornada["resultado"] == 1)]["cuotaEmpates"].values.sum(), 2)
    beneficios = round(ganancias_totales - capital_inicial_total2, 2)
    if(ganancias_totales!=0):
        if(capital_inicial_total2>0):
            rentabilidad = round(ganancias_totales * 100 / capital_inicial_total2 - 100, 2)
        else:
            rentabilidad = 0
    else:
        rentabilidad = 0
    beneficio_mes = BeneficiosMes.objects.latest('temporada')
    all_entries_mes = BeneficiosMes.objects.filter(temporada = beneficio_mes.temporada)  
    first_mes = all_entries_mes.values_list()    
    df_mes = pd.DataFrame(data=first_mes, columns=['id', 'capital_inicial', 'ganancias_brutas', 'ganancias_netas', "temporada", 'mes'])
    pd_capital_aportado = pd.DataFrame(CAPITAL_APORTADO.items(), columns=["temporada", "capital"])
    return render(request, 'precision.html', {"df_data_evolucion": df_data_evolucion.to_json(orient='split'), "data_mes": df_mes.to_json(orient='split'), 'data_informacion_actual': df_data_informacion.to_json(orient='split'), 'data_informacion_1920': df_data_informacion_1920.to_json(orient='split'), 'data_informacion_1819': df_data_informacion_1819.to_json(orient='split'), 'data_informacion_1718': df_data_informacion_1718.to_json(orient='split'), 'data_informacion_1617': df_data_informacion_1617.to_json(orient='split'), 'data_informacion_1516': df_data_informacion_1516.to_json(orient='split'), 'data_informacion_1415': df_data_informacion_1415.to_json(orient='split'), 'data_informacion_1314': df_data_informacion_1314.to_json(orient='split'), 'data_informacion_1213': df_data_informacion_1213.to_json(orient='split'), "pd_capital_aportado": pd_capital_aportado.to_json(orient='split'), "capital_inicial_total2": capital_inicial_total2, "ganancias_totales": ganancias_totales, "beneficios": beneficios, "rentabilidad": rentabilidad})   

def jornadaInicio(i):
    switcher={
        0:'4', #lunes
        1:'5', #martes
        2:'6', #miercoles
        3:'7', #jueves
        4:'4', #viernes
        5:'5', #sabado
        6:'6' #domingo
    }
    return switcher.get(i,"Invalid day of week")

def jornadaFin(i):
    switcher={
        0:'0', #lunes
        1:'0', #martes
        2:'2', #miercoles
        3:'3', #jueves
        4:'0', #viernes
        5:'1', #sabado
        6:'2' #domingo
    }
    return switcher.get(i,"Invalid day of week")

def mes(i):
    switcher={
        1:'Enero', 
        2:'Febrero',
        3:'Marzo',
        4:'Abril',
        5:'Mayo',
        6:'Junio',
        7:'Julio',
        8:'Agosto',
        9:'Septiembre',
        10:'Octubre',
        11:'Noviembre',
        12:'Diciembre'
    }
    return switcher.get(i,"Invalid month")

def historico20202021(request):
    #historico = Historico.objects.latest('ejecucion')
    all_entries = Historico.objects.filter(ejecucion = 1, prediction = 1, temporada = 2021)
    first = all_entries.values_list()    
    df = pd.DataFrame(data=first, columns=['id', 'prediccion', 'date', 'home_team', 'away_team', 'resultado', 'ejecucion', "cuotaEmpates", "temporada", "probabilidad"])
    return render(request, 'historico20202021.html', {'data': df.to_json(orient='split')})   


def historico20192020(request):
    #historico = Historico.objects.latest('ejecucion')
    all_entries = Historico.objects.filter(ejecucion = 1, prediction = 1, temporada = 1920)
    first = all_entries.values_list()    
    df = pd.DataFrame(data=first, columns=['id', 'prediccion', 'date', 'home_team', 'away_team', 'resultado', 'ejecucion', "cuotaEmpates", "temporada", "probabilidad"])
    return render(request, 'historico20192020.html', {'data': df.to_json(orient='split')})   

def historico20182019(request):
    #historico = Historico.objects.latest('ejecucion')
    all_entries = Historico.objects.filter(ejecucion = 1, prediction = 1, temporada = 1819)
    first = all_entries.values_list()    
    df = pd.DataFrame(data=first, columns=['id', 'prediccion', 'date', 'home_team', 'away_team', 'resultado', 'ejecucion', "cuotaEmpates", "temporada", "probabilidad"])
    return render(request, 'historico20182019.html', {'data': df.to_json(orient='split')})

def historico20172018(request):
    #historico = Historico.objects.latest('ejecucion')
    all_entries = Historico.objects.filter(ejecucion = 1, prediction = 1, temporada = 1718)
    first = all_entries.values_list()    
    df = pd.DataFrame(data=first, columns=['id', 'prediccion', 'date', 'home_team', 'away_team', 'resultado', 'ejecucion', "cuotaEmpates", "temporada", "probabilidad"])
    return render(request, 'historico20172018.html', {'data': df.to_json(orient='split')})
    
def historico20162017(request):
    #historico = Historico.objects.latest('ejecucion')
    all_entries = Historico.objects.filter(ejecucion = 1, prediction = 1, temporada = 1617)
    first = all_entries.values_list()    
    df = pd.DataFrame(data=first, columns=['id', 'prediccion', 'date', 'home_team', 'away_team', 'resultado', 'ejecucion', "cuotaEmpates", "temporada", "probabilidad"])
    return render(request, 'historico20162017.html', {'data': df.to_json(orient='split')})   

def historico20152016(request):
    #historico = Historico.objects.latest('ejecucion')
    all_entries = Historico.objects.filter(ejecucion = 1, prediction = 1, temporada = 1516)
    first = all_entries.values_list()    
    df = pd.DataFrame(data=first, columns=['id', 'prediccion', 'date', 'home_team', 'away_team', 'resultado', 'ejecucion', "cuotaEmpates", "temporada", "probabilidad"])
    return render(request, 'historico20152016.html', {'data': df.to_json(orient='split')})

def historico20142015(request):
    #historico = Historico.objects.latest('ejecucion')
    all_entries = Historico.objects.filter(ejecucion = 1, prediction = 1, temporada = 1415)
    first = all_entries.values_list()    
    df = pd.DataFrame(data=first, columns=['id', 'prediccion', 'date', 'home_team', 'away_team', 'resultado', 'ejecucion', "cuotaEmpates", "temporada", "probabilidad"])
    return render(request, 'historico20142015.html', {'data': df.to_json(orient='split')})   

def historico20132014(request):
    #historico = Historico.objects.latest('ejecucion')
    all_entries = Historico.objects.filter(ejecucion = 1, prediction = 1, temporada = 1314)
    first = all_entries.values_list()    
    df = pd.DataFrame(data=first, columns=['id', 'prediccion', 'date', 'home_team', 'away_team', 'resultado', 'ejecucion', "cuotaEmpates", "temporada", "probabilidad"])
    return render(request, 'historico20132014.html', {'data': df.to_json(orient='split')})      

def historico20122013(request):
    #historico = Historico.objects.latest('ejecucion')
    all_entries = Historico.objects.filter(ejecucion = 1, prediction = 1, temporada = 1213)
    first = all_entries.values_list()    
    df = pd.DataFrame(data=first, columns=['id', 'prediccion', 'date', 'home_team', 'away_team', 'resultado', 'ejecucion', "cuotaEmpates", "temporada", "probabilidad"])
    return render(request, 'historico20122013.html', {'data': df.to_json(orient='split')})             

def prediccion(request):
    ultima_ejecucion = Predicciones.objects.latest('ejecucion')
    all_entries = Predicciones.objects.filter(ejecucion = ultima_ejecucion.ejecucion, prediction = 1)
    first = all_entries.values_list()    
    df = pd.DataFrame(data=first, columns=['id', 'prediccion', 'date', 'home_team', 'away_team', 'resultado', 'ejecucion', "temporada", "probabilidad", "cuota"])
    return render(request, 'prediccion.html', {'data': df.to_json(orient='split')})   


        

