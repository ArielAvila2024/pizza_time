from flask import Flask, render_template, redirect, request, session, flash
from flask_app import app
import json

#Importamos todos los modelos
from flask_app.models.users import User
from flask_app.models.pizza import Pizza

#Hacemos la importacion de la libreria para hashear la password
from flask_bcrypt import Bcrypt
from flask import jsonify

import re #Importar las expresiones regulares

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$') 

bcrypt = Bcrypt(app)

@app.route("/")
def index():
    
    if 'user_id' in session:
        
        return redirect("/menu-principal")
    
    return render_template("index.html")

@app.route("/registration-form")
def registrationForm():
    return render_template("registration.html")

@app.route("/register", methods = ["POST"])
def register():
    
    if request.form['nombre'] == "" or request.form['apellido'] == "" or request.form['email'] == "" or request.form['ubicacion'] == "" or request.form['password'] == "" or request.form['confirm'] == "":
        return jsonify(message="No pueden haber campos en blanco")
    
    if not EMAIL_REGEX.match(request.form["email"]):
        return jsonify(message="Email con formato incorrecto")
    
    user = User.get_by_email(request.form)
    if user:
        return jsonify(message = "El email ya se encuentra registrado")
    
    if len(request.form['password']) < 6:
        return jsonify(message = "La contraseña debe tener como minimo 6 caracteres")
    
    if request.form['password'] != request.form['confirm']:
        return jsonify(message = "Las contraseñas no coinciden")
    
    #Encriptamos la contra
    pass_encrypt = bcrypt.generate_password_hash(request.form['password'])
    
    ubicacion_diccionario = json.loads(request.form['ubicacion'])
    
    latitud = ubicacion_diccionario['geometry']['coordinates'][0]
    longitud = ubicacion_diccionario['geometry']['coordinates'][1]
    direccion = ubicacion_diccionario['place_name']

    #Generamos un diccionario con toda la info y la password encriptada
    form = {
        "nombre" : request.form['nombre'],
        "apellido" : request.form['apellido'],
        "email" : request.form['email'],
        "direccion" : direccion,
        "direccion_longitud" : longitud,
        "direccion_latitud" : latitud,
        "password" : pass_encrypt
    }
    
    
    nuevo_id = User.save(form)
    
    if nuevo_id == 0:
        return jsonify(message="Ocurrio un error al intentar ingresar al usuario, vuelva a intentarlo mas tarde")
    
    session['user_id'] = nuevo_id
    return jsonify(message = "registro correcto")

@app.route("/login", methods = ['POST'])
def login():
    #Verificamos si el email exite en la BD
    user = User.get_by_email(request.form) #user = instancia User o False
    
    if not user:
        return jsonify(message = "E-mail no registrado")
    
    #Si user SI es instancia de User
    if not bcrypt.check_password_hash(user.password, request.form['password']): #contra encryptada, contra no encriptada

        return jsonify(message = "Password incorrecto")
    
    session['user_id'] = user.id #Guardo en sesion el id del usuario
    
    return jsonify(message="login correcto")

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")

@app.route("/editar-usuario", methods=['POST'])
def editar_usuario():
    # Obtener el ID de usuario de la sesión
    user_id = session.get('user_id')
    
    # verificamos si se encuentra en sesion
    if 'user_id' not in session:
        return redirect("/")
    
    if request.form['nombre'] == "" or request.form['apellido'] == "" or request.form['email'] == "" or request.form['direccion'] == "":
        return jsonify(message="No pueden haber campos en blanco")
    
    if not EMAIL_REGEX.match(request.form["email"]):
        return jsonify(message="Email con formato incorrecto")
    
    email_user = User.get_email_by_userId({"id": user_id})
    
    if  email_user[0]['email'] != request.form['email']:
        
        if User.get_by_email(request.form):
            return jsonify(message="El correo electrónico ingresado ya existe en el sistema")

    favorite_order_id = request.form.get('pedido_favorito')
    form_pedido = ""
    
    if favorite_order_id:
        form_pedido = {
            "id_user": user_id,
            "id_order": favorite_order_id
        }
        
    ubicacion_form = request.form['ubicacion']
    
    if ubicacion_form != "":
        ubicacion_diccionario = json.loads(ubicacion_form)
        latitud = ubicacion_diccionario['geometry']['coordinates'][1]
        longitud = ubicacion_diccionario['geometry']['coordinates'][0]
        direccion = ubicacion_diccionario['place_name']
    
        form_edit = {
            'id' : user_id,
            'nombre' : request.form['nombre'],
            'apellido' : request.form['apellido'],
            'email' : request.form['email'],
            'direccion' : direccion,
            'direccion_longitud' : latitud,
            'direccion_latitud' : longitud  
        }
    
    else:

        form_edit = {
            'id' : user_id,
            'nombre' : request.form['nombre'],
            'apellido' : request.form['apellido'],
            'email' : request.form['email'],
            'direccion' : request.form['direccion'],
            'direccion_longitud' : request.form['direccion_longitud'],
            'direccion_latitud' : request.form['direccion_latitud']  
        }
        
    
    user_edit = User.edit_user(form_edit)
    
    if user_edit:
        return jsonify(message="Ocurrio un error al intentar editar tu cuenta, vuelva a intentarlo mas tarde")
    
    if form_pedido != "":
        user_pedido = User.edit_pedido(form_pedido)
        
        if user_pedido:
            return jsonify(message="Ocurrio un error al intentar guardar tu pedido favorito, vuelva a intentarlo mas tarde")
        

    return jsonify(message="Edicion correcta")

@app.route("/menu-principal")
def menu_principal():
    
    # verificamos si se encuentra en sesion
    if 'user_id' not in session:
        return redirect("/")
    
    return render_template("menu-principal.html")

@app.route("/mi-cuenta")
def mi_perfil():
    
    # verificamos si se encuentra en sesion
    if 'user_id' not in session:
        return redirect("/")
    
    form = {"id": session['user_id']}
    user = User.get_by_id(form)
    
    orders = Pizza.get_pedidos_by_user_id(form)
    
    if orders:
        for item in orders:
            total_orden = item['pizza'][0]['total_orden']
            created_at = item['pizza'][0]['created_at']
            favorito = item['pizza'][0]['favorito']
            item['total_orden'] = total_orden
            item['created_at'] = created_at.strftime('%d/%m/%Y')
            item['favorito'] = favorito
            del item['pizza'][0]['total_orden']
            del item['pizza'][0]['created_at']
            del item['pizza'][0]['favorito']

    return render_template("mi-cuenta.html", user=user, orders=orders)


@app.route('/maps-prueba')
def maps():
    return render_template('maps-prueba.html')

