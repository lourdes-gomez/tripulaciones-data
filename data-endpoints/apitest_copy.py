import openai
import typer
from rich import print
from rich.table import Table
import os

global response_content

def main():
    archivo = "apikey.txt"
    with open(archivo, "r") as apikey:
        openai.api_key = apikey.read()

    print("💬 [bold green]ChatGPT API en Python[/bold green]")

    # table = Table("Comando", "Descripción")
    # table.add_row("exit", "Salir de la aplicación")
    # table.add_row("new", "Crear una nueva conversación")

    # print(table)

    context = {"role": "system", "content": '''Responde con un máximo de 10 palabras. 
               Voy a darte mensajes tipo de gente que expresa incidencias en una finca,  
               quiero que lo categorices dentro de: 
               [Ascensor, Tuberias/agua, Luz, Goteras, Humedades, Grietas, Suciedad, Ruidos, Conflicto Vecinal, No incidencia]
                y le asignes un nivel de urgencia para resolver la urgencia de 1-5.'''}
    messages = [context]

    # while True:
    for i in range(1):
        content = __prompt()

        # if content == "new":
        #     print("🆕 Nueva conversación creada")
        #     messages = [context]
        #     content = __prompt()

        messages.append({"role": "user", "content": content})

        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo", messages=messages)

        response_content = response['choices'][0]['message']['content']

        messages.append({"role": "assistant", "content": response_content})

        print(f"[bold green]> [/bold green] [green]{response_content}[/green]")

        i +=1

    return response_content

def __prompt() -> str:
    prompt = typer.prompt("\n¿Sobre qué quieres hablar? ")

    # if prompt == "exit":
    #     exit = typer.confirm("✋ ¿Estás seguro?")
    #     if exit:
    #         print("👋 ¡Hasta luego!")
    #         raise typer.Abort()

    #     return __prompt()

    return prompt

if __name__ == "__main__":
    # typer.run(main)
    response_content = typer.run(main)

