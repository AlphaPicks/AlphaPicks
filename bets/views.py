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
from tabulate import tabulate
import numpy as np
from urllib.request import urlopen
from zipfile import ZipFile
from django.utils import timezone
from django.core import serializers
from datetime import datetime

#from apscheduler.schedulers.background import BackgroundScheduler

#from schedule import Scheduler

from bets.models import Beneficios
from bets.models import Predicciones


VERSION_MODELO = "D1"
CAPITAL_INICIAL_TOTAL_APUESTAS = 10


from celery.schedules import crontab
from celery.task import periodic_task
from datetime import timedelta
#@periodic_task(run_every=timedelta(seconds=2))
#def every_monday_morning():
#    print("This is run every Monday morning at 7:30")

#@periodic_task(run_every=crontab(hour=7, minute=30, day_of_week="mon"))
#def every_monday_morning():
#    print("This is run every Monday morning at 7:30")

@periodic_task(run_every=timedelta(seconds=2))
def every_monday_morning():
    print("This is run every Monday morning at 7:30")











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

def beneficiosLanzar(request):
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
    now = datetime.now()
    timestamp = datetime.timestamp(now)
    t_object = datetime.fromtimestamp(timestamp)
    columnas_trabajo = ['Div', 'Date', 'HomeTeam', 'AwayTeam', 'B365H', 'B365D', 'B365A', 'WHH', 'WHD', 'WHA', 'BWH', 'BWD', 'BWA', 'IWH', 'IWD', 'IWA', 'PSH', 'PSD', 'PSA', 'VCH', 'VCD', 'VCA', 'FTR']
    columnas_trabajo_rn = ['B365H', 'B365D', 'B365A', 'WHH', 'WHD', 'WHA', 'BWH', 'BWD', 'BWA', 'IWH', 'IWD', 'IWA', 'PSH', 'PSD', 'PSA', 'VCH', 'VCD', 'VCA', 'FTR']
    columnas_prediccion = ['B365H', 'B365D', 'B365A', 'WHH', 'WHD', 'WHA', 'BWH', 'BWD', 'BWA', 'IWH', 'IWD', 'IWA', 'PSH', 'PSD', 'PSA', 'VCH', 'VCD', 'VCA']
    columnas_prediccion_rn = ['B365H', 'B365D', 'B365A', 'WHH', 'WHD', 'WHA', 'BWH', 'BWD', 'BWA', 'IWH', 'IWD', 'IWA', 'PSH', 'PSD', 'PSA', 'VCH', 'VCD', 'VCA']

    # RF Empates
    df_test_rf_empates = df_test.filter(items=columnas_trabajo)
    df_test_rf_empates["target"] = df_test_rf_empates["FTR"]
    df_test_rf_empates.loc[df_test_rf_empates.target == "H", 'target'] = "0"
    df_test_rf_empates.loc[df_test_rf_empates.target == "A", 'target'] = "0"
    df_test_rf_empates.loc[df_test_rf_empates.target == "D", 'target'] = "1"
    df_test_rf_empates.drop(columns=["FTR"], inplace=True)

    ligas =["B1", "D1", "D2", "E0", "E1", "E2", "E3", "EC", "F1", "F2", "G1", "I1", "N1", "P1", "SC0", "SC1", "SC2", "SC3", "SP1", "SP2", "T1"]

    ganancias_totales = 0
    ganancias = 0
    capital_inicial_total = 0
    capital_inicial_total2 = 0
    capital_inicial = 0
    rentables_rf_empates = []
    for x in ligas:
        df_rf_test = df_test_rf_empates[df_test_rf_empates["Div"] == x]
        df_rf_test.dropna(inplace=True)
        X_test_rf = df_rf_test[columnas_prediccion]
        y_test_rf = df_rf_test.target
        model_path = url = staticfiles_storage.path("modelos/randon_forest_empates_" + VERSION_MODELO + ".pkl")
        with open(model_path, 'rb') as file:
            rf = pickle.load(file)  
        y_pred_rf = rf.predict(X_test_rf)
        df_aux = df_rf_test[df_rf_test["Div"] == x]
        df_aux["Prediccion"] = y_pred_rf
        df_aux["Cuota"] = 0     
        df_aux = df_aux.reset_index(drop=True)
        for index, row in df_aux.iterrows():
            if(df_aux.loc[index, "Prediccion"] == "0"):
                df_aux.loc[index, "Cuota"] = 0            
            if(df_aux.loc[index, "Prediccion"] == "1"):
                df_aux.loc[index, "Cuota"] = df_aux.iloc[index]["B365D"]
                capital_inicial_total = capital_inicial_total + 1
                capital_inicial = capital_inicial + 1
            if(df_aux.loc[index, "Prediccion"] == "0"):
                df_aux.loc[index, "Cuota"] = 0
            if(df_aux.loc[index, "Prediccion"] ==  df_aux.iloc[index]["target"]):
                ganancias = ganancias + df_aux.iloc[index]["Cuota"] 
        if(ganancias - capital_inicial>0):
            rentables_rf_empates.append(x)
        capital_inicial_total2 = capital_inicial_total2 + capital_inicial 
        capital_inicial_total = capital_inicial_total + capital_inicial
        capital_inicial = 0
        ganancias_totales = ganancias_totales + ganancias
        ganancias = 0

    p = Beneficios(dia = timezone.now(), capital_inicial = round(capital_inicial_total2, 2), ganancias_brutas = round(ganancias_totales, 2), ganancias_netas = round(ganancias_totales - capital_inicial_total2, 2), porcentaje_beneficio = round(ganancias_totales * 100 / capital_inicial_total2 - 100, 2), porcentaje_beneficio_frente_al_inicial = round(((ganancias_totales - capital_inicial_total2)*100/CAPITAL_INICIAL_TOTAL_APUESTAS),2)) 
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
    mails = ["ibon.bengoa@opendeusto.es"]
    user_email = "ibongaraybengoabets@gmail.com"
    pass_email = "IbonGaray7777777"
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
    df_prediccion_rf = pd.DataFrame()
    df_prediccion_rf["Date"] = df_actual_rf["Date"]
    df_prediccion_rf["Div"] = df_actual_rf["Div"]
    df_prediccion_rf["HomeTeam"] = df_actual_rf["HomeTeam"]
    df_prediccion_rf["AwayTeam"] = df_actual_rf["AwayTeam"]
    df_prediccion_rf["B365H"] = df_actual_rf["B365H"]
    df_prediccion_rf["B365D"] = df_actual_rf["B365D"]
    df_prediccion_rf["B365A"] = df_actual_rf["B365A"]
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
    
    ejecucion_actual = Predicciones.objects.latest('ejecucion').ejecucion + 1
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
        p = Predicciones(prediction = prediction_actual, date = date_actual, home_team = home_team_actual, away_team = away_team_actual, resultado = resultado_actual, ejecucion = ejecucion_actual)
        p.save()
    
    return render(request, 'home.html')

def dos(request):
    return HttpResponse("Hello, Django 2!")

def ejecutar(request):
     #return HttpResponse("Hello, Django 3!")
     return render(request, 'ejecutar.html')

def precision(request):
    last_beneficio = Beneficios.objects.latest('dia')

    data_informacion = [[last_beneficio.dia, last_beneficio.capital_inicial, last_beneficio.ganancias_brutas, last_beneficio.ganancias_netas, last_beneficio.porcentaje_beneficio, last_beneficio.porcentaje_beneficio_frente_al_inicial]] 
    df_data_informacion = pd.DataFrame(data_informacion, columns = ['Día',' Capital inicial', 'Ganancia brutas', 'Ganancia netas', 'Beneficio', 'Beneficio frente inicial']) 
    return render(request, 'precision.html', {'data_informacion': df_data_informacion.to_json(orient='split')})   

def metodologia(request):
    return render(request, 'metodologia.html')

def apuestas2(request):
    return render(request, 'apuestas.html')

def apuestas(request):
    return render(request, 'apuestas.html')

def prediccion(request):
    ultima_ejecucion = Predicciones.objects.latest('ejecucion')
    all_entries = Predicciones.objects.filter(ejecucion = ultima_ejecucion.ejecucion, prediction = 1)
    first = all_entries.values_list()    
    df = pd.DataFrame(data=first, columns=['id', 'prediccion', 'date', 'home_team', 'away_team', 'resultado', 'ejecucion'])
    #print(df)

    #return render(request, 'home.html')
    #return render(request, 'prediccion.html', {'data': df_prediccion_rf_empates[df_prediccion_rf_empates["Prediccion"] == "1"].filter(items=["Prediccion", "Date", "HomeTeam", "AwayTeam"]).to_json(orient='split')})   
    return render(request, 'prediccion.html', {'data': df.to_json(orient='split')})   
    #return render(request, 'prediccion.html', {'data': data})   

        

