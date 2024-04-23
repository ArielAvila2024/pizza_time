from flask_app.config.mysqlconnection import connectToMySQL

class Topping:
    def __init__(self, data):
        
        self.id = data['id']
        self.name = data['name']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.category_topping_id = data['category_topping_id']
        
        self.category_name = data['category']
        
        
    @classmethod
    def get_all_toppings(cls):
            
        query = 'SELECT toppings.*, category_toppings.name category FROM toppings JOIN category_toppings ON toppings.category_topping_id = category_toppings.id'
        result = connectToMySQL('proyecto_pizzatime').query_db(query)
            
        toppings = []
        for i in result:
            toppings.append(cls(i))
                
        return toppings