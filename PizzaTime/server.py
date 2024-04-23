from flask_app import app

#Importamos los controladores
from flask_app.controllers import users_controller
from flask_app.controllers import pedidos_controller

#Ejecucion de app
if __name__ == "__main__":
    app.run(debug = True)