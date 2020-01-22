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

def dos(request):
    return HttpResponse("Hello, Django 2!")

def ejecutar(request):
     #return HttpResponse("Hello, Django 3!")
     return render(request, 'ejecutar.html')

def precision(request):
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
    #df_historico_rf_empates = df_historico.filter(items=columnas_trabajo)
    df_test_rf_empates = df_test.filter(items=columnas_trabajo)

    #df_historico_rf_empates["target"] = df_historico_rf_empates["FTR"]
    #df_historico_rf_empates.loc[df_historico_rf_empates.target == "H", 'target'] = "0"
    #df_historico_rf_empates.loc[df_historico_rf_empates.target == "A", 'target'] = "0"
    #df_historico_rf_empates.loc[df_historico_rf_empates.target == "D", 'target'] = "1"
    #df_historico_rf_empates.drop(columns=["FTR"], inplace=True)
    df_test_rf_empates["target"] = df_test_rf_empates["FTR"]
    df_test_rf_empates.loc[df_test_rf_empates.target == "H", 'target'] = "0"
    df_test_rf_empates.loc[df_test_rf_empates.target == "A", 'target'] = "0"
    df_test_rf_empates.loc[df_test_rf_empates.target == "D", 'target'] = "1"
    df_test_rf_empates.drop(columns=["FTR"], inplace=True)

    return render(request, 'precision.html')

def metodologia(request):
    return render(request, 'metodologia.html')

def apuestas2(request):
    return render(request, 'apuestas.html')

def apuestas(request):
    return render(request, 'apuestas.html')

def prediccion(request):
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
        model_path = url = staticfiles_storage.path("modelos/randon_forest_empates_" + "E0" + ".pkl") #static("modelos/randon_forest_" + "E0" + ".pkl") #"modelos/randon_forest_" + "E0" + ".pkl" #os.path.join(os.path.dirname(os.path.realpath(__file__)), "/modelos/randon_forest_" + "E0" + ".pkl")
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

    return render(request, 'prediccion.html', {'data': df_prediccion_rf_empates[df_prediccion_rf_empates["Prediccion"] == "1"].filter(items=["Prediccion", "Date", "HomeTeam", "AwayTeam"]).to_json(orient='split')})   
    #return render(request, 'apuestas.html', {'data': data})
    #df.to_json(orient='split')
        

