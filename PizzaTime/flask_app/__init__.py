#Importacion de Flask
from flask import Flask

#Inicializacion de la app
app = Flask(__name__)

#Declaramos llave secreta
app.secret_key = "La llave secreta de sesion"

app.config['MAPBOX_ACCESS_TOKEN'] = 'pk.eyJ1IjoiYXJpZWxjdmN4IiwiYSI6ImNsdmJuNXBvYjBhbHkya3FtZ2d1dG50cTIifQ.0m8_eMRY8yqswpGtGwy8iw'  # Reemplaza 'TU_ACCESS_TOKEN' con tu token de acceso de Mapbox
app.config['MAPBOX_MAP_ID'] = 'arielcvcx'