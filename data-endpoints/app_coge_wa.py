import openai
import typer
from rich import print
from rich.table import Table
import os
import sqlite3
from sqlalchemy import create_engine, text, update, MetaData, Table, Column, String
import pandas as pd
import numpy as np
import re
import flask 
from flask import Flask, jsonify
import json
import time
import datetime

from selenium import webdriver

from simon.accounts.pages import LoginPage
from simon.chat.pages import ChatPage
from simon.chats.pages import PanePage
from simon.header.pages import HeaderPage



app = Flask(__name__)

app.config['JSON_AS_ASCII'] = False

# Base de datos en local:

# engine = create_engine("sqlite:///./bbdd/db_final.db")

# Base de datos en cloud:

engine = create_engine("postgresql://postgres:12345678@database-2.c0tj9rzcjeux.eu-north-1.rds.amazonaws.com:5432/postgres")

# Creamos el driver de Chrome:
driver = webdriver.Chrome()
driver.maximize_window()

# 1. Login
#       and uncheck the remember check box
#       (Get your phone ready to read the QR code)
login_page = LoginPage(driver)
login_page.load()
# login_page.remember_me = False
time.sleep(2)

# Endpoint bienvenida:
@app.route('/', methods=['GET','POST'])
def welcome():

    return """<h1>Bienvenido a la API de FincUp</h1>
    <h2>Endpoints:</h2>

    1) Actualizar BBDD: -> '/api/actualizar'<br> 
    2) Consultar nuevas incidencias: -> '/api/incidencias'<br>
    3) Consultar fincas: -> '/api/fincas'<br>
    4) Consultar proveedores: -> '/api/proveedores'<br>
    """

# Endpoint para actualizar incidencias (se ejecuta cada x mins con archivo while.py)
@app.route('/api/actualizar', methods=['GET','POST'])
def main():

    engine = create_engine("postgresql://postgres:12345678@database-2.c0tj9rzcjeux.eu-north-1.rds.amazonaws.com:5432/postgres")

    #Localizamos y entramos en la conversación de whatsapp de ese número:
    for chat in [x for x in driver.find_elements(by="class name", value="_21S-L")]:
        if chat.text  == "+34 642 96 74 14":
            print(chat.text)
            chat.click()
            break

    span_element = driver.find_elements(by="css selector",value='div._2au8k span')

    # Obtenemos el texto dentro del span (que es el número de teléfono):
    numero_telefono = span_element[0].text


    # Utilizamos expresiones regulares para extraer solo los dígitos:
    num_limpio = re.sub(r'\+\d+\s*', '', numero_telefono)
    num_limpio = num_limpio.replace(" ", "")


    # Extraemos la hora del último mensaje:
    horas = []

    for msg in driver.find_elements(by="css selector", value="div.copyable-text"):
        horas.append(msg.get_attribute("data-pre-plain-text"))

    ult_fecha_hora = horas[-1]

    inicio = ult_fecha_hora.find('[') + 1
    fin = ult_fecha_hora.find(']')
    fecha_hora = ult_fecha_hora[inicio:fin]


   # Ajustamos el formato de la hora y lo cambiamos a string:
    formato = '%H:%M, %d/%m/%Y'

    dt_fecha_hora = datetime.datetime.strptime(fecha_hora, formato)

 
    formato_salida = '%Y-%m-%d %H:%M:%S'  # Puedes ajustar el formato según tus necesidades
    str_fecha_hora = dt_fecha_hora.strftime(formato_salida)

# Esta parte del código es para intentar enviar un mensaje automáticamente:

    num_tel = '+34' + num_limpio

    # fecha_hora = '19:40, 17/1/2024'
    lista_fh = fecha_hora.split(":")

    # hora_wa_recibido = int(lista_fh[0])
    # mins_wa_recibido = int(lista_fh[1][0:2]) + 2

    hora = int(datetime.datetime.now().hour)

    mins = int(datetime.datetime.now().minute) + 2

    # time.sleep(30)


    # import pywhatkit
    # pywhatkit.sendwhatmsg(num_tel, 
    #                     "Incidencia registrada. Se le informará de posteriores actualizaciones en el estado de su incidencia.", hora, mins)

# A partir de aquí continua el código:
    
    # Almacenar los mensajes de la conversación en una lista:
    mensajes = []

    for msg in [x for x in driver.find_elements(by="css selector", value="div._1BOF7 span")]:
        if msg.get_property("dir") == "ltr":
            ult_mensaje = msg.text

            if ult_mensaje not in mensajes:
                mensajes.append(ult_mensaje)

        
    # Guardamos solo el último mensaje:
    ult_mensaje = mensajes[-1]

    incidencia = ult_mensaje

    # Creamos los campos para completar por defecto en la BBDD al recibir una incidencia:

    level_0 = 1
    index = 1
    categoria = None
    urgencia = None
    servicio = None
    estado_inc = "Por recibir"

    # Query para insertar la incidencia recibida en la base de datos:
    query = '''
        INSERT INTO incidencias ("level_0", "index", "Teléfono", "Fecha", "Incidencia", "Categoría", "Urgencia", "Servicio", "Estado incidencia")
        VALUES (:level_0, :index, :num_limpio, :str_fecha_hora, :ult_mensaje, :categoria, :urgencia, :servicio, :estado_inc)
    '''

    # Ejecutar la query anterior:

    with engine.connect() as connection:
        with connection.begin():  # Inicia una transacción
            result = connection.execute(
                text(query),
                {
                    "level_0": str(level_0),
                    "index": str(index),
                    "num_limpio": str(num_limpio),
                    "str_fecha_hora": str(str_fecha_hora),
                    "ult_mensaje": str(ult_mensaje),
                    "categoria": str(categoria),
                    # "urgencia": str(urgencia),
                    "urgencia": urgencia,
                    "servicio": str(servicio),
                    "estado_inc": str(estado_inc)
                }
            )


    # Query para seleccionar las incidencias cuya categoría o incidencia no está clasificada:

    query = '''SELECT incidencias."Incidencia" FROM incidencias
            WHERE (incidencias."Categoría" = 'None') OR (incidencias."Urgencia" IS NULL)'''

    result = pd.read_sql(query, engine).values
    lista_inc = [elem[0] for elem in result]

    # Bucle que se ejecuta para cada incidencia seleccionada en la query anterior (incidencia sin clasificar):

    for incidencia in lista_inc:
        prompt = incidencia

    # Importar la apikey de ChatGPT:

        #archivo = "apikey.txt"
        #with open(archivo, "r") as apikey:
        #       openai.api_key = apikey.read()

    # Código que conecta con api de ChatGPT y categoriza la incidencia:

        openai.api_key = ''

        print("💬 [bold green]ChatGPT API en Python[/bold green]")

        context = {"role": "system", "content": '''Responde con un máximo de 10 palabras. 
                Voy a darte mensajes tipo de gente que expresa incidencias en una finca,  
                quiero que lo categorices dentro de: 
                [Ascensor, Tuberías/agua, Luz, Goteras, Humedades, Grietas, Suciedad, Ruidos, Conflicto Vecinal, No incidencia]
                y le asignes un nivel de urgencia para resolver la urgencia de 1-5.
                Responde en este formato: "Categoría: , Urgencia: "'''}
        messages = [context]

        for _ in range(1):
            content = prompt

            messages.append({"role": "user", "content": content})  
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo", messages=messages)

            response_content = response['choices'][0]['message']['content']

            messages.append({"role": "assistant", "content": response_content})

            print(f"[bold green]> [/bold green] [green]{response_content}[/green]")

        patron_categoria = r"Categoría: (\w+)"
        patron_urgencia = r"Urgencia: (\d+)"
        match_categoria = re.search(patron_categoria, response_content)
        match_urgencia = re.search(patron_urgencia, response_content)

        categoria = match_categoria.group(1) if match_categoria else 'No'
        urgencia = int(match_urgencia.group(1)) if match_urgencia else None


        mapeo_servicios = {
        'Ascensor': 'Reparación ascensores',
        'Ruidos': 'Servicios de emergencia',
        'Tuberías': 'Fontanería',
        'Agua': 'Fontanería',
        'Goteras': 'Reparación instalaciones eléctricas',
        'Humedades': 'Mantenimiento áreas comunes',
        'Grietas': 'Pintura y reparación de paredes',
        'Suciedad': 'Servicios de limpieza',
        'No': None,  
        'Luz': 'Reparación instalaciones eléctricas',
        'Tuberias': 'Fontanería',
        'Aire': 'Mantenimiento calefacción y aire acondicionado',
        'Conflicto': 'Colegio de administradores',
        'Olores': 'Servicios de limpieza',
        'No incidencia': None
        }
        estado_inc = "Por recibir"

        # Query para actualizar la BBDD con las incidencias nuevas categorizadas:

        query = '''
            UPDATE incidencias
            SET "Categoría" = :categoria,
                "Urgencia" = :urgencia,
                "Servicio" = :servicio,
                "Estado incidencia" = :estado_inc
            WHERE "Incidencia" = :incidencia
        '''

        # Ejecutar la query anterior:

        with engine.connect() as connection:
            with connection.begin():  
                result = connection.execute(
                    text(query),
                    {
                        'categoria': categoria,
                        'urgencia': urgencia,
                        'servicio': str(mapeo_servicios[categoria]),
                        'estado_inc': estado_inc,
                        'incidencia': incidencia
                    }
                )

    # Retorna un json con la información:
    return jsonify({"status": "success", "message": "Incidencias actualizadas correctamente"})


# Endpoint para consultar las incidencias sin procesar:
@app.route('/api/incidencias', methods=['GET','POST'])
def consulta():

    engine = create_engine("postgresql://postgres:12345678@database-2.c0tj9rzcjeux.eu-north-1.rds.amazonaws.com:5432/postgres")

# Query para seleccionar solo las incidencias clasificadas como incidencia:

    # query = '''SELECT * FROM incidencias
    # WHERE (incidencias."Categoría" != 'No') AND ("Estado incidencia" = 'Por recibir')'''

# Query para seleccionar todas las incidencias (también las clasificadas como no incidencia por si en la demo pasa, para verlo):

    query = '''SELECT * FROM incidencias
    WHERE "Estado incidencia" = 'Por recibir'
    '''

    df = pd.read_sql(query, engine).drop(columns=["level_0"])


    result = df.to_dict(orient='records')


    json_result = json.dumps(result, ensure_ascii=False)

    # Retorna la información de la tabla de la BBDD en un json:
    return json_result

# Endpoint para consultar fincas:
@app.route('/api/fincas', methods=['GET','POST'])
def consulta_fincas():

    engine = create_engine("postgresql://postgres:12345678@database-2.c0tj9rzcjeux.eu-north-1.rds.amazonaws.com:5432/postgres")

    # Query para seleccionar todas las fincas de la tabla de la BBDD:
    query = '''SELECT * FROM fincas
    '''

    df = pd.read_sql(query, engine).drop(columns=["level_0"])

    result = df.to_dict(orient='records')

    # Usa el módulo json para serializar con ensure_ascii=False
    json_result = json.dumps(result, ensure_ascii=False)

    # Retorna la información de la tabla de la BBDD en un json:
    return json_result


# Endpoint para consultar proveedores de servicios:
@app.route('/api/proveedores', methods=['GET','POST'])
def consulta_prov():

    engine = create_engine("postgresql://postgres:12345678@database-2.c0tj9rzcjeux.eu-north-1.rds.amazonaws.com:5432/postgres")

    # QUery para seleccionar toda la tabla de proveedores:
    query = '''SELECT * FROM prov
    '''

    df = pd.read_sql(query, engine).drop(columns=["level_0"])

    result = df.to_dict(orient='records')

    # Usa el módulo json para serializar con ensure_ascii=False
    json_result = json.dumps(result, ensure_ascii=False)

    # Retorna la información de la tabla de la BBDD en un json:
    return json_result

if __name__ == "__main__":
    app.run(debug=True, port=8000)
