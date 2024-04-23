from flask_app.config.mysqlconnection import connectToMySQL

class Pedido:
    def __init__(self, data):
        
        self.id = data['id']
        self.user_id = data['user_id']
        self.total = data['total']
        self.metodo_entrega = data['metodo_entrega']
        self.favorito = data['favorito']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        
        self.user_name = data['user_name']
        
        
    @classmethod
    def get_by_id(cls,id):
            
        query = 'SELECT * FROM orders WHERE id = %(id)s'
        result = connectToMySQL('proyecto_pizzatime').query_db(query,id)
        
        if len(result) == 1:
        #Si existe el orden
            order = cls(result[0])
            return order #Regresamos la instancia de la orden con esa id
        else:
            return False
        
    @classmethod
    def ingresar_orden(cls, form):
                
        query = 'INSERT INTO orders(user_id,total,metodo_entrega,favorito) VALUES(%(user_id)s,%(total)s,%(metodo_entrega)s,%(favorito)s)'
        result = connectToMySQL('proyecto_pizzatime').query_db(query, form)
        
        return result
        
    @classmethod
    def get_all_orders(cls):
            
        query = 'SELECT orders.*, CONCAT(users.nombre, users.apellido) FROM orders JOIN users ON users.id = orders.user_id'
        result = connectToMySQL('proyecto_pizzatime').query_db(query)
        
        orders = []
        
        if len(result) == 1:
            for i in result:
                orders.append(cls(i))
            return orders
        else:
            return False #Si no hay ordenes retorna Falso