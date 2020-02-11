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
#from tabulate import tabulate
import numpy as np
from urllib.request import urlopen
from zipfile import ZipFile
from django.utils import timezone
from django.core import serializers
from datetime import datetime
from datetime import timedelta
#import datetime

#from apscheduler.schedulers.background import BackgroundScheduler

#from schedule import Scheduler

from bets.models import Beneficios
from bets.models import Predicciones
from bets.models import Historico


#VERSION_MODELO = "E0"
VERSION_MODELO = "D1"
CAPITAL_INICIAL_TOTAL_APUESTAS = 10
TEMPORADA_ACTUAL = 1920


#from celery.schedules import crontab
#from celery.task import periodic_task
from datetime import timedelta
#@periodic_task(run_every=timedelta(seconds=2))
#def every_monday_morning():
#    print("This is run every Monday morning at 7:30")

#@periodic_task(run_every=crontab(hour=7, minute=30, day_of_week="mon"))
#def every_monday_morning():
#    print("This is run every Monday morning at 7:30")

#@periodic_task(run_every=timedelta(seconds=2))
#def every_monday_morning():
#    print("This is run every Monday morning at 7:30")



mails = ["ibon.bengoa@opendeusto.es"]
user_email = "ibongaraybengoabets@gmail.com"
pass_email = "IbonGaray7777777777"



def send_email(user, pwd, recipient, subject, body):
    FROM = user
    TO = recipient if isinstance(recipient, list) else [recipient]
    SUBJECT = subject
    TEXT = body
    # Prepare actual message
    message = """From: %s\nTo: %s\nSubject: %s\n\n%s
    """ % (FROM, ", ".join(TO), SUBJECT, TEXT)
    #print(message)
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

def admin(request):
    return render(request, 'admin.html')

def obtenerDatosTemporada():
    df_test = pd.DataFrame()
    resp = urlopen('https://www.football-data.co.uk/mmz4281/1920/data.zip')
    zipfile = ZipFile(BytesIO(resp.read()))
    zipfile.namelist()
    df_new = pd.read_csv(zipfile.open('B1.csv'))
    df_test = pd.concat([df_test, df_new], sort=True)
    df_new = pd.read_csv(zipfile.open('D1.csv'))
    df_test = pd.concat([df_test, df_new], sort=True)
    df_new = pd.read_csv(zipfile.open('D2.csv'))
    df_test = pd.concat([df_test, df_new], sort=True)
    #df_new = pd.read_csv(zipfile.open('D3.csv'))
    #df_test = pd.concat([df_test, df_new], sort=True)
    df_new = pd.read_csv(zipfile.open('E0.csv'))
    df_test = pd.concat([df_test, df_new], sort=True)
    df_new = pd.read_csv(zipfile.open('E1.csv'))
    df_test = pd.concat([df_test, df_new], sort=True)
    df_new = pd.read_csv(zipfile.open('E2.csv'))
    df_test = pd.concat([df_test, df_new], sort=True)
    df_new = pd.read_csv(zipfile.open('E3.csv'))
    df_test = pd.concat([df_test, df_new], sort=True)
    df_new = pd.read_csv(zipfile.open('EC.csv'))
    df_test = pd.concat([df_test, df_new], sort=True)
    df_new = pd.read_csv(zipfile.open('F1.csv'))
    df_test = pd.concat([df_test, df_new], sort=True)
    df_new = pd.read_csv(zipfile.open('F2.csv'))
    df_test = pd.concat([df_test, df_new], sort=True)
    df_new = pd.read_csv(zipfile.open('G1.csv'))
    df_test = pd.concat([df_test, df_new], sort=True)
    df_new = pd.read_csv(zipfile.open('I1.csv'))
    df_test = pd.concat([df_test, df_new], sort=True)
    df_new = pd.read_csv(zipfile.open('I2.csv'))
    df_test = pd.concat([df_test, df_new], sort=True)
    df_new = pd.read_csv(zipfile.open('N1.csv'))
    df_test = pd.concat([df_test, df_new], sort=True)
    df_new = pd.read_csv(zipfile.open('P1.csv'))
    df_test = pd.concat([df_test, df_new], sort=True)
    df_new = pd.read_csv(zipfile.open('SC0.csv'))
    df_test = pd.concat([df_test, df_new], sort=True)
    df_new = pd.read_csv(zipfile.open('SC1.csv'))
    df_test = pd.concat([df_test, df_new], sort=True)
    df_new = pd.read_csv(zipfile.open('SC2.csv'))
    df_test = pd.concat([df_test, df_new], sort=True)
    df_new = pd.read_csv(zipfile.open('SC3.csv'))
    df_test = pd.concat([df_test, df_new], sort=True)
    df_new = pd.read_csv(zipfile.open('SP1.csv'))
    df_test = pd.concat([df_test, df_new], sort=True)
    df_new = pd.read_csv(zipfile.open('SP2.csv'))
    df_test = pd.concat([df_test, df_new], sort=True)
    df_new = pd.read_csv(zipfile.open('T1.csv'))
    df_test = pd.concat([df_test, df_new], sort=True)
    return df_test

def historicoBeneficiosLanzar(request):
    df_test = obtenerDatosTemporada()
    df_actual = df_test
    ### ************
    #df_actual = pd.read_csv("data_prediccion/20191018data_prediccion.csv")
    ### ************
    now = datetime.now()
    timestamp = datetime.timestamp(now)
    t_object = datetime.fromtimestamp(timestamp)
    #Se guarda el dato de la prediccion
    #export_csv = df_actual.to_csv (r"data_prediccion/" + str(t_object.year) + str(t_object.month) + str(t_object.day) + "data_prediccion.csv", index = None, header=True)
    clumnas_trabajo = ['Div', 'Date', 'HomeTeam', 'AwayTeam', 'B365H', 'B365D', 'B365A', 'WHH', 'WHD', 'WHA', 'BWH', 'BWD', 'BWA', 'IWH', 'IWD', 'IWA', 'PSH', 'PSD', 'PSA', 'VCH', 'VCD', 'VCA', 'FTR']
    columnas_prediccion = ['B365H', 'B365D', 'B365A', 'WHH', 'WHD', 'WHA', 'BWH', 'BWD', 'BWA', 'IWH', 'IWD', 'IWA', 'PSH', 'PSD', 'PSA', 'VCH', 'VCD', 'VCA']
    df_actual_rf = df_actual.filter(items=clumnas_trabajo)
    df_actual_rf.dropna(inplace=True)
    ligas =["B1", "D1", "D2", "E0", "E1", "E2", "E3", "EC", "F1", "F2", "G1", "I1", "I2", "N1", "P1", "SC0", "SC1", "SC2", "SC3", "SP1", "SP2", "T1"]
    df_actual_rf_empates = df_actual.filter(items=clumnas_trabajo)
    df_actual_rf_empates.dropna(inplace=True)
    df_prediccion_rf_empates = pd.DataFrame()
    df_prediccion_rf_empates["Date"] = df_actual_rf_empates["Date"]
    df_prediccion_rf_empates["Div"] = df_actual_rf_empates["Div"]
    df_prediccion_rf_empates["HomeTeam"] = df_actual_rf_empates["HomeTeam"]
    df_prediccion_rf_empates["AwayTeam"] = df_actual_rf_empates["AwayTeam"]
    df_prediccion_rf_empates["B365H"] = df_actual_rf_empates["B365H"]
    df_prediccion_rf_empates["B365D"] = df_actual_rf_empates["B365D"]
    df_prediccion_rf_empates["B365A"] = df_actual_rf_empates["B365A"]
    df_prediccion_rf_empates["FTR"] = df_actual_rf_empates["FTR"]

    y_pred_rf_resultado = []
    y_pred_rf_stats = []
    for x in ligas:
        #with open("modelos/randon_forest_empates_" + x + ".pkl", 'rb') as file:
        model_path = url = staticfiles_storage.path("modelos/randon_forest_empates_" + VERSION_MODELO + ".pkl") #static("modelos/randon_forest_" + "E0" + ".pkl") #"modelos/randon_forest_" + "E0" + ".pkl" #os.path.join(os.path.dirname(os.path.realpath(__file__)), "/modelos/randon_forest_" + "E0" + ".pkl")
        with open(model_path, 'rb') as file:
            rf = pickle.load(file) 
        if not df_actual_rf_empates[columnas_prediccion][df_actual_rf_empates["Div"] == x].empty:
            y_pred_rf2 = rf.predict(df_actual_rf_empates[columnas_prediccion][df_actual_rf_empates["Div"] == x])
            for i in y_pred_rf2 : 
                y_pred_rf_resultado.append(i) 
        if not df_actual_rf_empates[columnas_prediccion][df_actual_rf_empates["Div"] == x].empty:
            y_pred_rf3 = rf.predict_proba(df_actual_rf_empates[columnas_prediccion][df_actual_rf_empates["Div"] == x])
            for i in y_pred_rf3 : 
                y_pred_rf_stats.append(i) 
    df_prediccion_rf_empates["Prediccion"] = [row for row in y_pred_rf_resultado]
    df_prediccion_rf_empates["rf_empate"] = [row[1] for row in y_pred_rf_stats]
    df_prediccion_rf_empates["rf_no_empate"] = [row[0] for row in y_pred_rf_stats]
    df_prediccion_rf_empates["beneficio_total"] = (1/df_prediccion_rf_empates["B365H"]) + (1/df_prediccion_rf_empates["B365D"]) + (1/df_prediccion_rf_empates["B365A"])
    df_prediccion_rf_empates["porcentaje_pagos"] = (1/df_prediccion_rf_empates["beneficio_total"])
    df_prediccion_rf_empates["probabilidad_h"] = (1/df_prediccion_rf_empates["B365H"]*df_prediccion_rf_empates["porcentaje_pagos"])
    df_prediccion_rf_empates["probabilidad_d"] = (1/df_prediccion_rf_empates["B365D"]*df_prediccion_rf_empates["porcentaje_pagos"])
    df_prediccion_rf_empates["probabilidad_a"] = (1/df_prediccion_rf_empates["B365A"]*df_prediccion_rf_empates["porcentaje_pagos"])
    df_prediccion_rf_empates["entrar"] = "no"
    df_prediccion_rf_empates.loc[(df_prediccion_rf_empates["Prediccion"] == "1") & (df_prediccion_rf_empates["rf_empate"] > df_prediccion_rf_empates["probabilidad_d"]), "entrar"] = "si"
    

    df_prediccion_rf_empates.loc[df_prediccion_rf_empates.FTR == "H", 'FTR'] = "0"
    df_prediccion_rf_empates.loc[df_prediccion_rf_empates.FTR == "A", 'FTR'] = "0"
    df_prediccion_rf_empates.loc[df_prediccion_rf_empates.FTR == "D", 'FTR'] = "1"

    capital_inicial_total2 = len(df_prediccion_rf_empates[df_prediccion_rf_empates["Prediccion"] == "1"].index)
    ganancias_totales = df_prediccion_rf_empates[(df_prediccion_rf_empates["Prediccion"] == "1") & (df_prediccion_rf_empates["FTR"] == "1")]["B365D"].values.sum()
    
    #Beneficios.objects.all().delete()

    b = Beneficios(dia = timezone.now(), capital_inicial = round(capital_inicial_total2, 2), ganancias_brutas = round(ganancias_totales, 2), ganancias_netas = round(ganancias_totales - capital_inicial_total2, 2), porcentaje_beneficio = round(ganancias_totales * 100 / capital_inicial_total2 - 100, 2), porcentaje_beneficio_frente_al_inicial = round(((ganancias_totales - capital_inicial_total2)*100/CAPITAL_INICIAL_TOTAL_APUESTAS),2), temporada = TEMPORADA_ACTUAL) 
    b.save()

    ejecucion_actual = Historico.objects.latest('ejecucion').ejecucion + 1
    
    #Historico.objects.all().delete()

    #ejecucion_actual = 0
    resultado_actual = 0
    away_team_actual = "" 
    home_team_actual = ""
    cuotaEmpate = 0
    date_actual = timezone.now()
    prediction_actual = 0

    df_prediccion_rf_empates['date_created'] = pd.to_datetime(df_prediccion_rf_empates['Date'], dayfirst=True)
    df_prediccion_rf_empates = df_prediccion_rf_empates.sort_values(by='date_created', ascending=False)

    for index, row in df_prediccion_rf_empates[df_prediccion_rf_empates["Prediccion"] == "1"].iterrows():
        resultado_actual= row["FTR"]
        away_team_actual = row["AwayTeam"]
        home_team_actual = row["HomeTeam"]
        date_actual = datetime.strptime(row["Date"], '%d/%m/%Y')
        prediction_actual = row["Prediccion"]
        cuotaEmpate = row["B365D"]
        p = Historico(prediction = prediction_actual, date = date_actual, home_team = home_team_actual, away_team = away_team_actual, resultado = resultado_actual, cuotaEmpate = cuotaEmpate, ejecucion = ejecucion_actual, temporada = TEMPORADA_ACTUAL)
        p.save()

   

    return render(request, 'home.html')

def prediccionesLanzar(request):
    data = {
        'name': 'Vitor',
        'location': 'Finland',
        'is_active': True,
        'count': 28
        }
    ##############################################
    url_actual = 'https://www.football-data.co.uk/fixtures.csv'
    s=requests.get(url_actual).content
    df_actual = pd.read_csv(io.StringIO(s.decode('utf-8')))
    ### ************
    #df_actual = pd.read_csv("data_prediccion/20191018data_prediccion.csv")
    ### ************
    now = datetime.now()
    timestamp = datetime.timestamp(now)
    t_object = datetime.fromtimestamp(timestamp)
    #Se guarda el dato de la prediccion
    #export_csv = df_actual.to_csv (r"data_prediccion/" + str(t_object.year) + str(t_object.month) + str(t_object.day) + "data_prediccion.csv", index = None, header=True)
    clumnas_trabajo = ['Div', 'Date', 'HomeTeam', 'AwayTeam', 'B365H', 'B365D', 'B365A', 'WHH', 'WHD', 'WHA', 'BWH', 'BWD', 'BWA', 'IWH', 'IWD', 'IWA', 'PSH', 'PSD', 'PSA', 'VCH', 'VCD', 'VCA']
    columnas_prediccion = ['B365H', 'B365D', 'B365A', 'WHH', 'WHD', 'WHA', 'BWH', 'BWD', 'BWA', 'IWH', 'IWD', 'IWA', 'PSH', 'PSD', 'PSA', 'VCH', 'VCD', 'VCA']
    df_actual_rf = df_actual.filter(items=clumnas_trabajo)
    df_actual_rf.dropna(inplace=True)
    ligas =["B1", "D1", "D2", "E0", "E1", "E2", "E3", "EC", "F1", "F2", "G1", "I1", "I2", "N1", "P1", "SC0", "SC1", "SC2", "SC3", "SP1", "SP2", "T1"]
    df_actual_rf_empates = df_actual.filter(items=clumnas_trabajo)
    df_actual_rf_empates.dropna(inplace=True)
    df_prediccion_rf_empates = pd.DataFrame()
    df_prediccion_rf_empates["Date"] = df_actual_rf_empates["Date"]
    df_prediccion_rf_empates["Div"] = df_actual_rf_empates["Div"]
    df_prediccion_rf_empates["HomeTeam"] = df_actual_rf_empates["HomeTeam"]
    df_prediccion_rf_empates["AwayTeam"] = df_actual_rf_empates["AwayTeam"]
    df_prediccion_rf_empates["B365H"] = df_actual_rf_empates["B365H"]
    df_prediccion_rf_empates["B365D"] = df_actual_rf_empates["B365D"]
    df_prediccion_rf_empates["B365A"] = df_actual_rf_empates["B365A"]

    y_pred_rf_resultado = []
    y_pred_rf_stats = []
    for x in ligas:
        #with open("modelos/randon_forest_empates_" + x + ".pkl", 'rb') as file:
        model_path = url = staticfiles_storage.path("modelos/randon_forest_empates_" + VERSION_MODELO + ".pkl") #static("modelos/randon_forest_" + "E0" + ".pkl") #"modelos/randon_forest_" + "E0" + ".pkl" #os.path.join(os.path.dirname(os.path.realpath(__file__)), "/modelos/randon_forest_" + "E0" + ".pkl")
        with open(model_path, 'rb') as file:
            rf = pickle.load(file) 
        if not df_actual_rf_empates[columnas_prediccion][df_actual_rf_empates["Div"] == x].empty:
            y_pred_rf2 = rf.predict(df_actual_rf_empates[columnas_prediccion][df_actual_rf_empates["Div"] == x])
            for i in y_pred_rf2 : 
                y_pred_rf_resultado.append(i) 
        if not df_actual_rf_empates[columnas_prediccion][df_actual_rf_empates["Div"] == x].empty:
            y_pred_rf3 = rf.predict_proba(df_actual_rf_empates[columnas_prediccion][df_actual_rf_empates["Div"] == x])
            for i in y_pred_rf3 : 
                y_pred_rf_stats.append(i) 
    df_prediccion_rf_empates["Prediccion"] = [row for row in y_pred_rf_resultado]
    df_prediccion_rf_empates["rf_empate"] = [row[1] for row in y_pred_rf_stats]
    df_prediccion_rf_empates["rf_no_empate"] = [row[0] for row in y_pred_rf_stats]
    df_prediccion_rf_empates["beneficio_total"] = (1/df_prediccion_rf_empates["B365H"]) + (1/df_prediccion_rf_empates["B365D"]) + (1/df_prediccion_rf_empates["B365A"])
    df_prediccion_rf_empates["porcentaje_pagos"] = (1/df_prediccion_rf_empates["beneficio_total"])
    df_prediccion_rf_empates["probabilidad_h"] = (1/df_prediccion_rf_empates["B365H"]*df_prediccion_rf_empates["porcentaje_pagos"])
    df_prediccion_rf_empates["probabilidad_d"] = (1/df_prediccion_rf_empates["B365D"]*df_prediccion_rf_empates["porcentaje_pagos"])
    df_prediccion_rf_empates["probabilidad_a"] = (1/df_prediccion_rf_empates["B365A"]*df_prediccion_rf_empates["porcentaje_pagos"])
    df_prediccion_rf_empates["entrar"] = "no"
    df_prediccion_rf_empates.loc[(df_prediccion_rf_empates["Prediccion"] == "1") & (df_prediccion_rf_empates["rf_empate"] > df_prediccion_rf_empates["probabilidad_d"]), "entrar"] = "si"
    
    df_prediccion_rf_empates['date_created'] = pd.to_datetime(df_prediccion_rf_empates['Date'], dayfirst=True)
    df_prediccion_rf_empates = df_prediccion_rf_empates.sort_values(by='date_created', ascending=True)

    ejecucion_actual = Predicciones.objects.latest('ejecucion').ejecucion + 1

    #Predicciones.objects.all().delete()

    #ejecucion_actual = 0
    resultado_actual = 0
    away_team_actual = "" 
    home_team_actual = ""
    date_actual = timezone.now()
    prediction_actual = 0
    for index, row in df_prediccion_rf_empates.iterrows():
        away_team_actual = row["AwayTeam"]
        home_team_actual = row["HomeTeam"]
        date_actual = datetime.strptime(row["Date"], '%d/%m/%Y')
        prediction_actual = row["Prediccion"]
        p = Predicciones(prediction = prediction_actual, date = date_actual, home_team = home_team_actual, away_team = away_team_actual, resultado = resultado_actual, ejecucion = ejecucion_actual, temporada = TEMPORADA_ACTUAL)
        p.save()


    #Envia correo de los empates
    asunto_mensaje = "Prediccion Empates (" + str(t_object.year) + "/" + str(t_object.month) + "/" + str(t_object.day) + ")"
    texto_mensaje = df_prediccion_rf_empates[(df_prediccion_rf_empates["entrar"] == "si")].filter(items=["Date", "HomeTeam", "AwayTeam", "B365D"]).to_string(col_space = 20, justify='start', index=False)
    #& ((df_prediccion_rf_empates["Div"] == "B1") | (df_prediccion_rf_empates["Div"] == "D1") | (df_prediccion_rf_empates["Div"] == "E0") | (df_prediccion_rf_empates["Div"] == "EC") | (df_prediccion_rf_empates["Div"] == "F2") | (df_prediccion_rf_empates["Div"] == "G1") | (df_prediccion_rf_empates["Div"] == "I1") | (df_prediccion_rf_empates["Div"] == "N1") | (df_prediccion_rf_empates["Div"] == "P1") | (df_prediccion_rf_empates["Div"] == "SC0") | (df_prediccion_rf_empates["Div"] == "SC2") | (df_prediccion_rf_empates["Div"] == "SP1") | (df_prediccion_rf_empates["Div"] == "SP2") | (df_prediccion_rf_empates["Div"] == "T1"))
    #send_email(user_email, pass_email, mails, asunto_mensaje, texto_mensaje)

    return render(request, 'home.html')

def dos(request):
    return HttpResponse("Hello, Django 2!")

def ejecutar(request):
     #return HttpResponse("Hello, Django 3!")
     return render(request, 'ejecutar.html')

def precision(request):
    last_beneficio = Beneficios.objects.latest('dia')
    data_informacion = [[last_beneficio.dia, last_beneficio.capital_inicial, last_beneficio.ganancias_brutas, last_beneficio.ganancias_netas, last_beneficio.porcentaje_beneficio, last_beneficio.porcentaje_beneficio_frente_al_inicial, last_beneficio.temporada]] 
    df_data_informacion = pd.DataFrame(data_informacion, columns = ['Día',' Capital inicial', 'Ganancia brutas', 'Ganancia netas', 'Beneficio', 'Beneficio frente inicial', "Temporada"]) 

    historico = Historico.objects.latest('ejecucion')
    all_entries = Historico.objects.filter(ejecucion = historico.ejecucion, prediction = 1)
    first = all_entries.values_list()    
    df = pd.DataFrame(data=first, columns=['id', 'prediccion', 'date', 'home_team', 'away_team', 'resultado', "cuotaEmpates", 'ejecucion', "temporada"])

    print(datetime.today().weekday())
    print()

    tiempoJornadaInicio = jornadaInicio(datetime.today().weekday()) + "day"
    tiempoJornadaFin = jornadaFin(datetime.today().weekday()) + "day"

    print(tiempoJornadaInicio)
    print(tiempoJornadaFin)

    df_last_jornada = df[(df.date > (datetime.now().date() - pd.to_timedelta(tiempoJornadaInicio))) & (df.date < (datetime.now().date() - pd.to_timedelta(tiempoJornadaFin)))]

    capital_inicial_total2 = round(len(df_last_jornada[df_last_jornada["prediccion"] == 1].index), 2)
    ganancias_totales = round(df_last_jornada[(df_last_jornada["prediccion"] == 1) & (df_last_jornada["resultado"] == 1)]["cuotaEmpates"].values.sum(), 2)
    beneficios = round(ganancias_totales - capital_inicial_total2, 2)
    rentabilidad = round(ganancias_totales * 100 / capital_inicial_total2 - 100, 2)

    return render(request, 'precision.html', {'data_informacion': df_data_informacion.to_json(orient='split'), "capital_inicial_total2": capital_inicial_total2, "ganancias_totales": ganancias_totales, "beneficios": beneficios, "rentabilidad": rentabilidad})   

def jornadaInicio(i):
    switcher={
        0:'4',
        1:'5',
        2:'6',
        3:'7',
        4:'3',
        5:'4',
        6:'5'
    }
    return switcher.get(i,"Invalid day of week")

def jornadaFin(i):
    switcher={
        0:'0',
        1:'1',
        2:'2',
        3:'3',
        4:'0',
        5:'1',
        6:'2'
    }
    return switcher.get(i,"Invalid day of week")

def metodologia(request):
    return render(request, 'metodologia.html')

def apuestas2(request):
    return render(request, 'apuestas.html')

def apuestas(request):
    return render(request, 'apuestas.html')

def historico(request):
    
    historico = Historico.objects.latest('ejecucion')
    all_entries = Historico.objects.filter(ejecucion = historico.ejecucion, prediction = 1)
    first = all_entries.values_list()    
    df = pd.DataFrame(data=first, columns=['id', 'prediccion', 'date', 'home_team', 'away_team', 'resultado', 'ejecucion', "cuotaEmpates", "temporada"])
    #print(df)

    #return render(request, 'home.html')
    #return render(request, 'prediccion.html', {'data': df_prediccion_rf_empates[df_prediccion_rf_empates["Prediccion"] == "1"].filter(items=["Prediccion", "Date", "HomeTeam", "AwayTeam"]).to_json(orient='split')})   
    return render(request, 'historico.html', {'data': df.to_json(orient='split')})   

def prediccion(request):
    ultima_ejecucion = Predicciones.objects.latest('ejecucion')
    all_entries = Predicciones.objects.filter(ejecucion = ultima_ejecucion.ejecucion, prediction = 1)
    first = all_entries.values_list()    
    df = pd.DataFrame(data=first, columns=['id', 'prediccion', 'date', 'home_team', 'away_team', 'resultado', 'ejecucion', "temporada"])
    #print(df)

    #return render(request, 'home.html')
    #return render(request, 'prediccion.html', {'data': df_prediccion_rf_empates[df_prediccion_rf_empates["Prediccion"] == "1"].filter(items=["Prediccion", "Date", "HomeTeam", "AwayTeam"]).to_json(orient='split')})   
    return render(request, 'prediccion.html', {'data': df.to_json(orient='split')})   
    #return render(request, 'prediccion.html', {'data': data})   

        

