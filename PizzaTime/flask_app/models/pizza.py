from flask_app.config.mysqlconnection import connectToMySQL
from collections import defaultdict
import datetime

class Pizza:
    def __init__(self, data):
        
        self.id = data['id']
        self.size = data['size']
        self.corteza = data['corteza']
        self.cantidad = data['cantidad']
        self.total = data['total']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        
        #data necesaria
        self.order_id = data['order_id']
    
    @staticmethod
    def save_pizza(form):
            
        query = 'INSERT INTO pizzas(size,corteza,cantidad,total,order_id) VALUES(%(size)s,%(corteza)s,%(cantidad)s,%(total)s,%(order_id)s);'
        pizza_id = connectToMySQL('proyecto_pizzatime').query_db(query,form)
        
        if pizza_id > 0:
            query = ''
            for topping in form['toppings']:
                
                form_pizza = {
                    'pizza_id' : pizza_id,
                    'topping' : topping
                }
                
                query = 'INSERT INTO pizzas_has_toppings(pizza_id,topping_id) VALUES(%(pizza_id)s,%(topping)s)'
                result = connectToMySQL('proyecto_pizzatime').query_db(query,form_pizza)
                
        return result
    
    @staticmethod
    def get_pedidos_by_user_id(id):
        
        query = '''select orders.id, orders.total as total_orden, orders.created_at, orders.user_id, orders.favorito, pizzas.id as pizza_id, pizzas.size, pizzas.corteza, pizzas.total as total_pizza, GROUP_CONCAT(toppings.name SEPARATOR ', ') AS ingredientes from pizzas_has_toppings 
                    join toppings on pizzas_has_toppings.topping_id = toppings.id
                    join pizzas on pizzas.id = pizzas_has_toppings.pizza_id
                    join orders on pizzas.order_id = orders.id
                    WHERE orders.user_id = %(id)s 
                    group by pizzas.id'''
        
        result = connectToMySQL('proyecto_pizzatime').query_db(query,id)
        
        pedidos = []
        
        if result:
            for o in result:
                pedidos.append(o)
                pizzas_unificadas = defaultdict(list)

            for pizza in pedidos:
                pizza_id = pizza['id']
                user_id = pizza['user_id']
                pizza.pop('id')  # Quitamos el ID para evitar duplicados en el diccionario final
                pizzas_unificadas[pizza_id].append(pizza)
                
            resultado = []
            for pizza_id, pizzas in pizzas_unificadas.items():
                pizza_unificada = {
                    'id': pizza_id,
                    'user_id': user_id,
                    'pizza': pizzas
                }
                resultado.append(pizza_unificada)
            return resultado
        else:
            return False
