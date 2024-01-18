# PRODUCTO DIGITAL PARA LA GESTIÓN DE COMUNIDADES DE VECINOS

En este repositorio se recoge el trabajo realizado para el desafío de tripulaciones del bootcamp de Data science.<br>
El proyecto consiste en una aplicación web que facilite el trabajo diario a los administradores de fincas,<br>
junto con el resto de verticales (UX/UI y Full-Stack) se han definido las siguientes funcionalidades para la aplicación.<br>


## Integración de una Inteligencia Artificial para procesar mensajes de Whatsapp <br>
Mediante técnicas de web scraping se extraen los mensajes de la aplicación whatsapp y se almacenan en una base de datos. Estos mensajes<br>
se envían a la API de ChatGPT junto con un prompt donde especificamos como queremos que se procesen estos mensajes y qué información nos<br>
tiene que devolver, en este caso los mensajes son incidencias que notifican propietarios en una comunidad de vecinos y ChatGPT nos devuelve la<br>
categoría de la incidencia y el nivel de urgencia de la incidencia. Estos datos se envían a la app FincUp para que el administrador tenga un<br>
resumen de todas las incidencias de todas su fincas.<br>
Para este proyecto hemos creado una API con Flask y una base de datos PostgreSQL. Hemos utilizado las siguientes librerías de python : <br>
- Openai&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;            - Sqlite3
- Rich&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;              - Pandas
- Sqlalchemy&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;        - Flask
  


