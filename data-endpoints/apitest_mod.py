import openai
import typer
from rich import print
from rich.table import Table
import os
import sqlite3
from sqlalchemy import create_engine, text, update, MetaData, Table, Column, String
import pandas as pd
import re

def main():
    engine = create_engine("sqlite:///./bbdd/db_test.db")

    query = '''SELECT inc_rec FROM inc_table
               WHERE (categ IS NULL) OR (urg IS NULL)'''

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

        query = """
            UPDATE inc_table
            SET categ = :categoria, urg = :urgencia
            WHERE inc_rec = :incidencia
        """

        with engine.connect() as connection:
            with connection.begin():  # Inicia una transacción
                result = connection.execute(text(query), {'categoria': categoria, 'urgencia': urgencia, 'incidencia': incidencia})
            print(f"Número de filas afectadas: {result.rowcount}")

if __name__ == "__main__":
    typer.run(main)
