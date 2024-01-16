import openai
import typer
from rich import print
from rich.table import Table
import os
import sqlite3
from sqlalchemy import create_engine, text, update, MetaData, Table, Column, String
import pandas as pd
import re
import flask 
from flask import Flask, jsonify
import json
import time


app = Flask(__name__)

app.config['JSON_AS_ASCII'] = False

# engine = create_engine("sqlite:///./bbdd/db_final.db")
engine = create_engine("postgresql://postgres:12345678@database-2.c0tj9rzcjeux.eu-north-1.rds.amazonaws.com:5432/postgres")

@app.route('/api/actualizar', methods=['GET','POST'])
def main():
    
    query = '''SELECT incidencias."Incidencia" FROM incidencias
            WHERE (incidencias."Categoría" IS NULL) OR (incidencias."Urgencia" IS NULL)'''

    result = pd.read_sql(query, engine).values
    lista_inc = [elem[0] for elem in result]

    for incidencia in lista_inc:
        prompt = incidencia

        archivo = "apikey.txt"
        with open(archivo, "r") as apikey:
            openai.api_key = apikey.read()

        print("💬 [bold green]ChatGPT API en Python[/bold green]")

        context = {"role": "system", "content": '''Responde con un máximo de 10 palabras. 
                Voy a darte mensajes tipo de gente que expresa incidencias en una finca,  
                quiero que lo categorices dentro de: 
                [Ascensor, Tuberias/agua, Luz, Goteras, Humedades, Grietas, Suciedad, Ruidos, Conflicto Vecinal, No incidencia]
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

        categoria = match_categoria.group(1) if match_categoria else None
        urgencia = int(match_urgencia.group(1)) if match_urgencia else None


        mapeo_servicios = {
        'Ascensor': 'Reparación ascensores',
        'Ruidos': 'Servicios de emergencia',
        'Tuberías': 'Fontanería',
        'Goteras': 'Reparación instalaciones eléctricas',
        'Humedades': 'Mantenimiento áreas comunes',
        'Grietas': 'Pintura y reparación de paredes',
        'Suciedad': 'Servicios de limpieza',
        'No': None,  # Puedes asignar un servicio específico o dejarlo como None según tus necesidades
        'Luz': 'Reparación instalaciones eléctricas',
        'Tuberias': 'Fontanería',
        'Aire': 'Mantenimiento calefacción y aire acondicionado',
        'Conflicto': 'Colegio de administradores',
        'Olores': 'Servicios de limpieza'
        }

        estado_inc = "Recibida"

        query = '''
            UPDATE incidencias
            SET "Categoría" = ?,
                "Urgencia" = ?,
                "Servicio" = ?,
                "Estado incidencia" = ?
            WHERE "Incidencia" = ?
        '''

        with engine.connect() as connection:
            with connection.begin():  # Inicia una transacción
                result = connection.execute(text(query), (categoria, urgencia, mapeo_servicios[categoria], estado_inc, incidencia))
            print(f"Número de filas afectadas: {result.rowcount}")



# if __name__ == "__main__":
#     typer.run(main)

@app.route('/api/incidencias', methods=['GET','POST'])
def consulta():
    query = '''SELECT * FROM incidencias
    WHERE (incidencias."Categoría" != 'No') AND ("Estado incidencia" = 'Por recibir')'''

    df = pd.read_sql(query, engine).drop(columns=["level_0"])

    # dict_columnas = {}

    # for columna in df.columns:
    #     dict_columnas[columna] = df[columna].tolist()
        

    result = df.to_dict(orient='records')

    # Usa el módulo json para serializar con ensure_ascii=False
    json_result = json.dumps(result, ensure_ascii=False)


    return json_result


@app.route('/api/fincas', methods=['GET','POST'])
def consulta_fincas():
    query = '''SELECT * FROM fincas
    '''

    df = pd.read_sql(query, engine).drop(columns=["level_0"])

    result = df.to_dict(orient='records')

    # Usa el módulo json para serializar con ensure_ascii=False
    json_result = json.dumps(result, ensure_ascii=False)


    return json_result


@app.route('/api/proveedores', methods=['GET','POST'])
def consulta_prov():
    query = '''SELECT * FROM proveedores
    '''

    df = pd.read_sql(query, engine)

    result = df.to_dict(orient='records')

    # Usa el módulo json para serializar con ensure_ascii=False
    json_result = json.dumps(result, ensure_ascii=False)


    return json_result

if __name__ == "__main__":
    # typer.run(main)
    app.run(debug=True, port=8000)
