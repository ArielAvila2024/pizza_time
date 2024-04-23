from flask import Flask, render_template, redirect, request, session, flash, jsonify, url_for
from flask_app import app
from collections import defaultdict

#Importamos todos los modelos
from flask_app.models.toppings import Topping
from flask_app.models.pedidos import Pedido
from flask_app.models.pizza import Pizza
from flask_app.models.users import User

@app.route('/nueva-orden-menu')
def nueva_orden_menu():
    # verificamos si se encuentra en sesion
    if 'user_id' not in session:
        return redirect("/")
    
    toppings = Topping.get_all_toppings()

    return render_template('nueva-orden-menu.html', toppings=toppings)

# Esta funcion sirve para tener de forma global la variable para el carrito
@app.context_processor
def inject_session_variable():
    return dict(carrito=session.get('carrito', None))

@app.route('/agregar-pedido', methods = ['POST'])
def agregar_pedido():
    
    # verificamos si se encuentra en sesion
    if 'user_id' not in session:
        return redirect("/")
    
    form = {
        'size' : request.form['size'],
        'corteza' : request.form['masa'],
        'cantidad' : request.form['cantidad'],
        'toppings' : request.form.getlist('checkbox_vegetales') + request.form.getlist('checkbox_proteina') + request.form.getlist('radio_salsa'),
        'total' : int(request.form['sub_total']),
        'order_id' : '',
        'favorito' : 0
        }
    
    carrito = session.get('carrito',[])
    carrito.append(form)
    session['carrito'] = carrito
    
    return redirect("/nueva-orden-menu")

@app.route('/detalle-cuenta')
def detalle_cuenta():
    
    # verificamos si se encuentra en sesion
    if 'user_id' not in session:
        return redirect("/")
    
    carrito = session.get('carrito', [])
    
    return render_template('detalle-cuenta.html', carrito=carrito)

#Ingresa la orden en la base de datos
@app.route('/hacer-pedido', methods = ['POST'])
def hacer_pedido():
    
    # verificamos si se encuentra en sesion
    if 'user_id' not in session:
        return redirect("/")
    
    form = {
        'user_id' : session['user_id'],
        'total' : request.form['hidden_total'],
        'metodo_entrega' : request.form['metodo_entrega'],
        'favorito' : 0
    }
    
    order_id = Pedido.ingresar_orden(form) #retorna el id de la orden ingresada
    elementos_insertados = 0
    
    for form_session in session['carrito']:
        form_session['order_id'] =  order_id
        
        result = Pizza.save_pizza(form_session)

        if result == 0:
            elementos_insertados =+ 1
    
    if elementos_insertados > 0:
        session.pop("carrito")
        return redirect("/menu-principal")
    else:
        return redirect("/nueva-orden-menu")
    
#Limpia el carrito de pedidos
@app.route('/eliminar-pedido', methods = ['POST'])
def eliminar_pedido():
    
    # verificamos si se encuentra en sesion
    if 'user_id' not in session:
        return redirect("/")
    
    session.pop("carrito")
    return redirect("/menu-principal")

@app.route('/pedir-favorito')
def pedir_favorito():
    
    # verificamos si se encuentra en sesion
    if 'user_id' not in session:
        return redirect("/")
    
    form_idUser = {
        "user_id" : session["user_id"]
    }
    pedido_fav = User.get_pedido_favorito(form_idUser)

    pizzas_dict = defaultdict(lambda: {'toppings': []})

    # Agrupar las pizzas por pizza_id
    for pizza in pedido_fav:
        pizza_id = pizza['pizza_id']
        del pizza['pizza_id']
        toppings = str(pizza.pop('topping_id'))
        pizzas_dict[pizza_id].update(pizza)
        pizzas_dict[pizza_id]['toppings'].append(toppings)

    # Convertir el diccionario a la lista de dicts en el formato deseado
    transformed_array = [
        {**pizza_info, 'pizza_id': str(pizza_id), 'order_id': ''} 
        for pizza_id, pizza_info in pizzas_dict.items()
    ]

    # Imprimir el resultado
    for pizza in transformed_array:
        form = {
        'size' : pizza['size'],
        'corteza' : pizza['corteza'],
        'cantidad' : pizza['cantidad'],
        'toppings' : pizza['toppings'],
        'total' : pizza['total'],
        'order_id' : '',
        'favorito' : 1
        }
        carrito = session.get('carrito',[])
        carrito.append(form)
        session['carrito'] = carrito
    
    return redirect("/detalle-cuenta")
