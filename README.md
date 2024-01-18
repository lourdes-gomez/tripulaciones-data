# PRODUCTO DIGITAL PARA LA GESTIÓN DE COMUNIDADES DE VECINOS

En este repositorio se recoge el trabajo realizado para el desafío de tripulaciones del bootcamp de TheBridge.<br>

El proyecto consiste en una aplicación web que facilite el trabajo diario a los administradores de fincas,<br>
junto con el resto de verticales (UX/UI y Full-Stack) se han definido las siguientes funcionalidades para la aplicación.<br>


## Integración de una Inteligencia Artificial para procesar mensajes de Whatsapp <br>
Mediante técnicas de web scraping se extraen los mensajes de la aplicación whatsapp y se almacenan en una base de datos.<br> 
Estos mensajes se envían a la API de ChatGPT junto con un prompt donde especificamos como queremos que se procesen estos mensajes<br> 
y qué información nos tiene que devolver, en este caso los mensajes son incidencias que notifican propietarios en una comunidad de<br> 
vecinos y ChatGPT nos devuelve la categoría de la incidencia y el nivel de urgencia de la incidencia. Estos datos se envían a la app<br>
FincUp para que el administrador tenga un resumen de todas las incidencias de todas su fincas.<br>

Para este proyecto hemos creado una API con Flask y una base de datos PostgreSQL. Hemos utilizado las siguientes librerías de python : <br>
- Openai                     
- Sqlalchemy        
- Sqlite3 
- Pandas
- Flask
- Rich

## Modelo de análisis de sentimiento de feedback de los propietarios <br>
Mediante técnicas de NLP (Natural Language Processing) se puede analizar y automatizar el proceso de feedback para averiguar en cada momento <br>
si la gestión de la finca se está llevando a cabo satisfactoriamente. Este modelo nos indica el índice de satisfacción de los propietarios de <br>
la comunidad con la gestión de los administradores de fincas.<br>

Para este proyecto hemos utilizado las siguientes librerías de python : <br> 
- Nltk
- Sklearn
- Re

## Dashboard de todas las incidencias registradas<br>
Con este dashboard pretendemos que el administrador pueda acceder en tiempo real a todas las incidencias clasificadas por categorias,<br> 
en qué fincas se producen y en qué meses del año se registran mas incidencias. Este dashboard permite crear un informe automático de<br> 
todo el trabajo que realiza un administrador de fincas automatizando sus tareas y ahorrándole tiempo.<br>
