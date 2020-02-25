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
from bets.models import BeneficiosMes
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

def dos(request):
    return HttpResponse("Hello, Django 2!")

def ejecutar(request):
     #return HttpResponse("Hello, Django 3!")
     return render(request, 'ejecutar.html')

def metodologia(request):
    return render(request, 'metodologia.html')

def apuestas2(request):
    return render(request, 'apuestas.html')

def apuestas(request):
    return render(request, 'apuestas.html')

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

def historicoBeneficiosLanzarOtrasTemporadas():
    Historico.objects.all().delete()
    
    temporadas = ["1819", "1718", "1617", "1516", "1415", "1314", "1213"]#, "1112", "1011"]
    for t in temporadas:
        df_test = pd.DataFrame()
        data_path = staticfiles_storage.path("data/" + t + ".zip")
        #with open(data_path, 'rb') as file:
        #    data = pickle.load(file)
        #resp = urlopen(data_path)
        #zipfile = ZipFile(BytesIO(data_path.read()))
        zipfile = ZipFile(data_path, "r")
        #zipfile.ZipFile('images.zip', 'r')
        #zipfile = ZipFile(BytesIO(data.read()))
        zipfile.namelist()
        df_new = pd.read_csv(zipfile.open('B1.csv'), encoding= 'unicode_escape')
        df_test = pd.concat([df_test, df_new], sort=True)
        df_new = pd.read_csv(zipfile.open('D1.csv'), encoding= 'unicode_escape')
        df_test = pd.concat([df_test, df_new], sort=True)
        df_new = pd.read_csv(zipfile.open('D2.csv'), encoding= 'unicode_escape')
        df_test = pd.concat([df_test, df_new], sort=True)
        #df_new = pd.read_csv(zipfile.open('D3.csv'))
        #df_test = pd.concat([df_test, df_new], sort=True)
        df_new = pd.read_csv(zipfile.open('E0.csv'), encoding= 'unicode_escape')
        df_test = pd.concat([df_test, df_new], sort=True)
        df_new = pd.read_csv(zipfile.open('E1.csv'), encoding= 'unicode_escape')
        df_test = pd.concat([df_test, df_new], sort=True)
        df_new = pd.read_csv(zipfile.open('E2.csv'), encoding= 'unicode_escape')
        df_test = pd.concat([df_test, df_new], sort=True)
        df_new = pd.read_csv(zipfile.open('E3.csv'), encoding= 'unicode_escape')
        df_test = pd.concat([df_test, df_new], sort=True)
        df_new = pd.read_csv(zipfile.open('EC.csv'), encoding= 'unicode_escape')
        df_test = pd.concat([df_test, df_new], sort=True)
        df_new = pd.read_csv(zipfile.open('F1.csv'), encoding= 'unicode_escape')
        df_test = pd.concat([df_test, df_new], sort=True)
        df_new = pd.read_csv(zipfile.open('F2.csv'), encoding= 'unicode_escape')
        df_test = pd.concat([df_test, df_new], sort=True)
        df_new = pd.read_csv(zipfile.open('G1.csv'), encoding= 'unicode_escape')
        df_test = pd.concat([df_test, df_new], sort=True)
        df_new = pd.read_csv(zipfile.open('I1.csv'), encoding= 'unicode_escape')
        df_test = pd.concat([df_test, df_new], sort=True)
        df_new = pd.read_csv(zipfile.open('I2.csv'), encoding= 'unicode_escape')
        df_test = pd.concat([df_test, df_new], sort=True)
        df_new = pd.read_csv(zipfile.open('N1.csv'), encoding= 'unicode_escape')
        df_test = pd.concat([df_test, df_new], sort=True)
        df_new = pd.read_csv(zipfile.open('P1.csv'), encoding= 'unicode_escape')
        df_test = pd.concat([df_test, df_new], sort=True)
        df_new = pd.read_csv(zipfile.open('SC0.csv'), encoding= 'unicode_escape')
        df_test = pd.concat([df_test, df_new], sort=True)
        df_new = pd.read_csv(zipfile.open('SC1.csv'), encoding= 'unicode_escape')
        df_test = pd.concat([df_test, df_new], sort=True)
        df_new = pd.read_csv(zipfile.open('SC2.csv'), encoding= 'unicode_escape')
        df_test = pd.concat([df_test, df_new], sort=True)
        df_new = pd.read_csv(zipfile.open('SC3.csv'), encoding= 'unicode_escape')
        df_test = pd.concat([df_test, df_new], sort=True)
        df_new = pd.read_csv(zipfile.open('SP1.csv'), encoding= 'unicode_escape')
        df_test = pd.concat([df_test, df_new], sort=True)
        df_new = pd.read_csv(zipfile.open('SP2.csv'), encoding= 'unicode_escape')
        df_test = pd.concat([df_test, df_new], sort=True)
        df_new = pd.read_csv(zipfile.open('T1.csv'), encoding= 'unicode_escape')
        df_test = pd.concat([df_test, df_new], sort=True)
        df_test["temporada"] = t
        
        df_actual = df_test

        #print(df_actual)
        ###
        now = datetime.now()
        timestamp = datetime.timestamp(now)
        t_object = datetime.fromtimestamp(timestamp)
        #Se guarda el dato de la prediccion
        #export_csv = df_actual.to_csv (r"data_prediccion/" + str(t_object.year) + str(t_object.month) + str(t_object.day) + "data_prediccion.csv", index = None, header=True)
        clumnas_trabajo = ['Div', 'Date', 'HomeTeam', 'AwayTeam', "temporada", 'B365H', 'B365D', 'B365A', 'WHH', 'WHD', 'WHA', 'BWH', 'BWD', 'BWA', 'IWH', 'IWD', 'IWA', 'PSH', 'PSD', 'PSA', 'VCH', 'VCD', 'VCA', 'FTR']
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
        df_prediccion_rf_empates["temporada"] = df_actual_rf_empates["temporada"]

        y_pred_rf_resultado = []
        y_pred_rf_stats = []
        for x in ligas:
            #with open("modelos/randon_forest_empates_" + x + ".pkl", 'rb') as file:
            model_path = staticfiles_storage.path("modelos/randon_forest_empates_" + VERSION_MODELO + ".pkl") #static("modelos/randon_forest_" + "E0" + ".pkl") #"modelos/randon_forest_" + "E0" + ".pkl" #os.path.join(os.path.dirname(os.path.realpath(__file__)), "/modelos/randon_forest_" + "E0" + ".pkl")
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
        print(round(((ganancias_totales - capital_inicial_total2)*100/CAPITAL_INICIAL_TOTAL_APUESTAS),2))
        b = Beneficios(dia = timezone.now(), capital_inicial = round(capital_inicial_total2, 2), ganancias_brutas = round(ganancias_totales, 2), ganancias_netas = round(ganancias_totales - capital_inicial_total2, 2), porcentaje_beneficio = round(ganancias_totales * 100 / capital_inicial_total2 - 100, 2), porcentaje_beneficio_frente_al_inicial = round(((ganancias_totales - capital_inicial_total2)*100/CAPITAL_INICIAL_TOTAL_APUESTAS),2), temporada = t) 
        b.save()

        #ejecucion_actual = Historico.objects.latest('ejecucion').ejecucion + 1
        ejecucion_actual = 1
        
        resultado_actual = 0
        away_team_actual = "" 
        home_team_actual = ""
        cuotaEmpate = 0
        date_actual = timezone.now()
        prediction_actual = 0
        probabilidad = 0
        temporada_ac = ""

        df_prediccion_rf_empates['date_created'] = pd.to_datetime(df_prediccion_rf_empates['Date'], dayfirst=True)
        df_prediccion_rf_empates = df_prediccion_rf_empates.sort_values(by='date_created', ascending=False)

        #print(df_prediccion_rf_empates["temporada"])

        for index, row in df_prediccion_rf_empates[df_prediccion_rf_empates["Prediccion"] == "1"].iterrows():
            resultado_actual= row["FTR"]
            away_team_actual = row["AwayTeam"]
            home_team_actual = row["HomeTeam"]
            if(len(row["Date"]) <= 9):
            #if(row["Date"].endswith("/13")):
                date_actual = datetime.strptime(row["Date"], '%d/%m/%y')
            else:
                date_actual = datetime.strptime(row["Date"], '%d/%m/%Y')
            prediction_actual = row["Prediccion"]
            cuotaEmpate = row["B365D"]
            probabilidad = row["rf_empate"]
            temporada_ac = int(row["temporada"]) 
            p = Historico(prediction = prediction_actual, date = date_actual, home_team = home_team_actual, away_team = away_team_actual, resultado = resultado_actual, cuotaEmpate = cuotaEmpate, ejecucion = ejecucion_actual, temporada = temporada_ac, probabilidad = probabilidad)
            p.save()

    

def historicoBeneficiosLanzar(request):
    historicoBeneficiosLanzarOtrasTemporadas()
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

    #ejecucion_actual = Historico.objects.latest('ejecucion').ejecucion + 1
    #ejecucion_actual = Historico.objects.latest('ejecucion').ejecucion
    #ejecucion_actual = Historico.objects.latest('ejecucion').ejecucion + 1
    ejecucion_actual = 1
    #Historico.objects.all().delete()

    #ejecucion_actual = 0
    resultado_actual = 0
    away_team_actual = "" 
    home_team_actual = ""
    cuotaEmpate = 0
    date_actual = timezone.now()
    prediction_actual = 0
    probabilidad = 0

    df_prediccion_rf_empates['date_created'] = pd.to_datetime(df_prediccion_rf_empates['Date'], dayfirst=True)
    df_prediccion_rf_empates = df_prediccion_rf_empates.sort_values(by='date_created', ascending=False)

    for index, row in df_prediccion_rf_empates[df_prediccion_rf_empates["Prediccion"] == "1"].iterrows():
        resultado_actual= row["FTR"]
        away_team_actual = row["AwayTeam"]
        home_team_actual = row["HomeTeam"]
        date_actual = datetime.strptime(row["Date"], '%d/%m/%Y')
        prediction_actual = row["Prediccion"]
        cuotaEmpate = row["B365D"]
        probabilidad = row["rf_empate"]
        p = Historico(prediction = prediction_actual, date = date_actual, home_team = home_team_actual, away_team = away_team_actual, resultado = resultado_actual, cuotaEmpate = cuotaEmpate, ejecucion = ejecucion_actual, temporada = TEMPORADA_ACTUAL, probabilidad = probabilidad)
        p.save()

   
    
    df_prediccion_rf_empates["mes"] = df_prediccion_rf_empates['date_created'].map(lambda x: 100*x.year + x.month)
    #df_prediccion_rf_empates["mes"] = str(df_prediccion_rf_empates['date_created'].map(lambda x: 100*x.year)) + str(df_prediccion_rf_empates['date_created'].map(lambda x: x.month))
    
    #print(df_prediccion_rf_empates)
    #df_prediccion_rf_empates["mes"] = str(df_prediccion_rf_empates['date_created'].dt.year) + " - " + str(df_prediccion_rf_empates['date_created'].dt.month)
    df_mensual = pd.DataFrame()
    df_mensual["Ganancias"] = df_prediccion_rf_empates[(df_prediccion_rf_empates["Prediccion"] == "1") & (df_prediccion_rf_empates["FTR"] == "1")].groupby(['mes'])['B365D'].sum()
    df_mensual["Inversion"] = df_prediccion_rf_empates[(df_prediccion_rf_empates["Prediccion"] == "1")].groupby(['mes'])['B365D'].count()
    df_mensual["Beneficio"] = df_mensual["Ganancias"] - df_mensual["Inversion"]
    #df_mensual["mes_nombre"] = mes(df_mensual.index.item()) 
    df_mensual["mes_nombre2"] = df_mensual.index
    df_mensual["mes"] = df_mensual["mes_nombre2"].astype(int)
    BeneficiosMes.objects.all().delete()

    for index, row in df_mensual.iterrows():
        bM = BeneficiosMes(capital_inicial = row["Inversion"], ganancias_brutas = row["Ganancias"], ganancias_netas = row["Beneficio"], mes = row["mes"], temporada = TEMPORADA_ACTUAL)
        bM.save()

    return render(request, 'home.html')

def prediccionesLanzar(request):
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
    probabilidad = 0
    cuota = 0
    for index, row in df_prediccion_rf_empates.iterrows():
        away_team_actual = row["AwayTeam"]
        home_team_actual = row["HomeTeam"]
        date_actual = datetime.strptime(row["Date"], '%d/%m/%Y')
        prediction_actual = row["Prediccion"]
        probabilidad =  row["rf_empate"]
        cuota =  row["B365D"]
        p = Predicciones(prediction = prediction_actual, date = date_actual, home_team = home_team_actual, away_team = away_team_actual, resultado = resultado_actual, ejecucion = ejecucion_actual, temporada = TEMPORADA_ACTUAL, probabilidad = probabilidad, cuota = cuota)
        p.save()


    #Envia correo de los empates
    asunto_mensaje = "Prediccion Empates (" + str(t_object.year) + "/" + str(t_object.month) + "/" + str(t_object.day) + ")"
    texto_mensaje = df_prediccion_rf_empates[(df_prediccion_rf_empates["entrar"] == "si")].filter(items=["Date", "HomeTeam", "AwayTeam", "B365D"]).to_string(col_space = 20, justify='start', index=False)
    #& ((df_prediccion_rf_empates["Div"] == "B1") | (df_prediccion_rf_empates["Div"] == "D1") | (df_prediccion_rf_empates["Div"] == "E0") | (df_prediccion_rf_empates["Div"] == "EC") | (df_prediccion_rf_empates["Div"] == "F2") | (df_prediccion_rf_empates["Div"] == "G1") | (df_prediccion_rf_empates["Div"] == "I1") | (df_prediccion_rf_empates["Div"] == "N1") | (df_prediccion_rf_empates["Div"] == "P1") | (df_prediccion_rf_empates["Div"] == "SC0") | (df_prediccion_rf_empates["Div"] == "SC2") | (df_prediccion_rf_empates["Div"] == "SP1") | (df_prediccion_rf_empates["Div"] == "SP2") | (df_prediccion_rf_empates["Div"] == "T1"))
    #send_email(user_email, pass_email, mails, asunto_mensaje, texto_mensaje)

    return render(request, 'home.html')

def precision(request):
    #Temporada actual
    #last_beneficio = Beneficios.objects.latest('temporada')
    last_beneficio = Beneficios.objects.filter(temporada = "1920").order_by('-id')[0]
    data_informacion = [[last_beneficio.dia, last_beneficio.capital_inicial, last_beneficio.ganancias_brutas, last_beneficio.ganancias_netas, last_beneficio.porcentaje_beneficio, last_beneficio.porcentaje_beneficio_frente_al_inicial, last_beneficio.temporada]] 
    df_data_informacion = pd.DataFrame(data_informacion, columns = ['Día',' Capital inicial', 'Ganancia brutas', 'Ganancia netas', 'Beneficio', 'Beneficio frente inicial', "Temporada"]) 
    
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

    #Temporada 1112
    #last_beneficio = Beneficios.objects.filter(temporada = "1112").order_by('-id')[0]
    #data_informacion = [[last_beneficio.dia, last_beneficio.capital_inicial, last_beneficio.ganancias_brutas, last_beneficio.ganancias_netas, last_beneficio.porcentaje_beneficio, last_beneficio.porcentaje_beneficio_frente_al_inicial, last_beneficio.temporada]] 
    #df_data_informacion_1112 = pd.DataFrame(data_informacion, columns = ['Día',' Capital inicial', 'Ganancia brutas', 'Ganancia netas', 'Beneficio', 'Beneficio frente inicial', "Temporada"]) 
    
    #Temporada 1011
    #last_beneficio = Beneficios.objects.filter(temporada = "1011").order_by('-id')[0]
    #data_informacion = [[last_beneficio.dia, last_beneficio.capital_inicial, last_beneficio.ganancias_brutas, last_beneficio.ganancias_netas, last_beneficio.porcentaje_beneficio, last_beneficio.porcentaje_beneficio_frente_al_inicial, last_beneficio.temporada]] 
    #df_data_informacion_1011 = pd.DataFrame(data_informacion, columns = ['Día',' Capital inicial', 'Ganancia brutas', 'Ganancia netas', 'Beneficio', 'Beneficio frente inicial', "Temporada"]) 
    
    frames = [df_data_informacion, df_data_informacion_1819, df_data_informacion_1718, df_data_informacion_1617, df_data_informacion_1516, df_data_informacion_1415, df_data_informacion_1314, df_data_informacion_1213]
    df_data_evolucion = pd.concat(frames)

    #print(df_data_evolucion)

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
    if(capital_inicial_total2>0):
        rentabilidad = round(ganancias_totales * 100 / capital_inicial_total2 - 100, 2)
    else:
        rentabilidad = 0
    beneficio_mes = BeneficiosMes.objects.latest('temporada')
    all_entries_mes = BeneficiosMes.objects.filter(temporada = beneficio_mes.temporada)
    
    first_mes = all_entries_mes.values_list()    
    
    df_mes = pd.DataFrame(data=first_mes, columns=['id', 'capital_inicial', 'ganancias_brutas', 'ganancias_netas', "temporada", 'mes'])

    

    return render(request, 'precision.html', {"df_data_evolucion": df_data_evolucion.to_json(orient='split'), "data_mes": df_mes.to_json(orient='split'), 'data_informacion': df_data_informacion.to_json(orient='split'), 'data_informacion_1819': df_data_informacion_1819.to_json(orient='split'), 'data_informacion_1718': df_data_informacion_1718.to_json(orient='split'), 'data_informacion_1617': df_data_informacion_1617.to_json(orient='split'), 'data_informacion_1516': df_data_informacion_1516.to_json(orient='split'), 'data_informacion_1415': df_data_informacion_1415.to_json(orient='split'), 'data_informacion_1314': df_data_informacion_1314.to_json(orient='split'), 'data_informacion_1213': df_data_informacion_1213.to_json(orient='split'), "capital_inicial_total2": capital_inicial_total2, "ganancias_totales": ganancias_totales, "beneficios": beneficios, "rentabilidad": rentabilidad})   

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
    #print(df)


    #print(df)
    #return render(request, 'home.html')
    #return render(request, 'prediccion.html', {'data': df_prediccion_rf_empates[df_prediccion_rf_empates["Prediccion"] == "1"].filter(items=["Prediccion", "Date", "HomeTeam", "AwayTeam"]).to_json(orient='split')})   
    return render(request, 'prediccion.html', {'data': df.to_json(orient='split')})   
    #return render(request, 'prediccion.html', {'data': data})   

        

