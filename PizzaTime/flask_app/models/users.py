from flask_app.config.mysqlconnection import connectToMySQL
import json

class User:
    def __init__(self, data):
        
        self.id = data['id']
        self.nombre = data['nombre']
        self.apellido = data['apellido']
        self.email = data['email']
        self.direccion = data['direccion']
        self.direccion_longitud = data['direccion_longitud']
        self.direccion_latitud = data['direccion_latitud']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    @staticmethod
    def save(form):
        query = 'INSERT INTO users(nombre,apellido,email,direccion,direccion_longitud,direccion_latitud,password) VALUES(%(nombre)s,%(apellido)s,%(email)s,%(direccion)s,%(direccion_longitud)s,%(direccion_latitud)s,%(password)s)'
        result = connectToMySQL('proyecto_pizzatime').query_db(query, form)
        return result
        
    
    @classmethod
    def get_by_email(cls, form):
        query = "SELECT * FROM users WHERE email = %(email)s"
        results = connectToMySQL('proyecto_pizzatime').query_db(query, form)
        if len(results) == 1:
            
            user = cls(results[0])
            
            return user #Regresamos la instancia del usuario con ese correo
        else:
            return False
        
    @classmethod
    def get_by_id(cls,form):
        query = "SELECT * FROM users WHERE id = %(id)s"
        result = connectToMySQL('proyecto_pizzatime').query_db(query, form)
        
        user = cls(result[0])
        return user
    
    @staticmethod
    def get_email_by_userId(form):
        
        query = "SELECT email FROM users WHERE id = %(id)s"
        result = connectToMySQL('proyecto_pizzatime').query_db(query, form)
        
        return result
    
    @staticmethod
    def edit_user(form):
        
        query = '''UPDATE users SET
        nombre = %(nombre)s,
        apellido = %(apellido)s,
        email = %(email)s,
        direccion = %(direccion)s,
        direccion_longitud = %(direccion_longitud)s,
        direccion_latitud = %(direccion_latitud)s
        WHERE id = %(id)s;
        '''
        result = connectToMySQL('proyecto_pizzatime').query_db(query, form)
        
        print(result)
        
        return result
    
    @staticmethod
    def edit_pedido(form):
        
        query ="UPDATE orders SET favorito = 0 WHERE user_id = %(id_user)s"
        result = connectToMySQL('proyecto_pizzatime').query_db(query, form)
        query = "UPDATE orders SET favorito = 1 WHERE id = %(id_order)s and user_id = %(id_user)s;"
        result = connectToMySQL('proyecto_pizzatime').query_db(query, form)
        
        
        return result
    
    @staticmethod
    def get_pedido_favorito(form):
        
        query = '''select pizzas.id as pizza_id, pizzas.size, pizzas.corteza, pizzas.cantidad, pizzas.total, toppings.id as topping_id from orders 
                    JOIN pizzas on pizzas.order_id = orders.id 
                    JOIN pizzas_has_toppings on pizzas_has_toppings.pizza_id = pizzas.id
                    JOIN toppings on toppings.id = pizzas_has_toppings.topping_id
                    WHERE orders.favorito = 1 and orders.user_id = %(user_id)s'''
        result = connectToMySQL('proyecto_pizzatime').query_db(query, form)
        
        return result