from flask import Flask, render_template, request, jsonify

app = Flask(__name__)
from flask import Flask, render_template, request, jsonify
import os

app = Flask(__name__, template_folder=os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'templates'))

# El resto de tu código igual...from flask import Flask, render_template, request, jsonify
import os

app = Flask(__name__, template_folder=os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'templates'))

# El resto de tu código igual...
# Datos de ejemplo para productos básicos
sample_products = [
    {
        "id": 1,
        "name": "Leche Alpura 1L",
        "category": "Lácteos",
        "image": "https://via.placeholder.com/300x200/24A9DC/FFFFFF?text=Leche",
        "stores": [
            {"name": "Walmart Altabrisa", "price": 23.50, "distance": 1.2, "offer_valid": "🟢"},
            {"name": "Soriana Montejo", "price": 24.30, "distance": 2.1, "offer_valid": "🟢"},
            {"name": "Chedraui Itzaes", "price": 22.90, "distance": 3.5, "offer_valid": "🟡"}
        ],
        "description": "Leche entera pasteurizada de 1 litro. Rica en calcio y vitaminas."
    },
    {
        "id": 2,
        "name": "Huevo Blanco 30pz",
        "category": "Abarrotes",
        "image": "https://via.placeholder.com/300x200/EB692C/FFFFFF?text=Huevo",
        "stores": [
            {"name": "Walmart Altabrisa", "price": 68.50, "distance": 1.2, "offer_valid": "🟢"},
            {"name": "Soriana Montejo", "price": 65.90, "distance": 2.1, "offer_valid": "🟡"},
            {"name": "Chedraui Itzaes", "price": 70.20, "distance": 3.5, "offer_valid": "🟢"}
        ],
        "description": "Huevo blanco grado A, paquete de 30 piezas."
    },
    {
        "id": 3,
        "name": "Frijol Negro 1kg",
        "category": "Legumbres",
        "image": "https://via.placeholder.com/300x200/36C07E/FFFFFF?text=Frijol",
        "stores": [
            {"name": "Walmart Altabrisa", "price": 38.00, "distance": 1.2, "offer_valid": "🟡"},
            {"name": "Soriana Montejo", "price": 35.50, "distance": 2.1, "offer_valid": "🟢"},
            {"name": "Chedraui Itzaes", "price": 36.80, "distance": 3.5, "offer_valid": "🟢"}
        ],
        "description": "Frijol negro de primera calidad, paquete de 1kg."
    },
    {
        "id": 4,
        "name": "Arroz SOS 1kg",
        "category": "Granos",
        "image": "https://via.placeholder.com/300x200/24A9DC/FFFFFF?text=Arroz",
        "stores": [
            {"name": "Walmart Altabrisa", "price": 28.50, "distance": 1.2, "offer_valid": "🟢"},
            {"name": "Soriana Montejo", "price": 26.90, "distance": 2.1, "offer_valid": "🟢"},
            {"name": "Chedraui Itzaes", "price": 27.80, "distance": 3.5, "offer_valid": "🟡"}
        ],
        "description": "Arroz blanco grano largo, paquete de 1kg."
    },
    {
        "id": 5,
        "name": "Aceite Capullo 1L",
        "category": "Aceites",
        "image": "https://via.placeholder.com/300x200/EB692C/FFFFFF?text=Aceite",
        "stores": [
            {"name": "Walmart Altabrisa", "price": 45.00, "distance": 1.2, "offer_valid": "🟡"},
            {"name": "Soriana Montejo", "price": 42.50, "distance": 2.1, "offer_valid": "🟢"},
            {"name": "Chedraui Itzaes", "price": 43.80, "distance": 3.5, "offer_valid": "🟢"}
        ],
        "description": "Aceite vegetal comestible, botella de 1 litro."
    }
]

# Datos de ejemplo para tiendas
sample_stores = [
    {"name": "Walmart Altabrisa", "lat": 20.983113, "lng": -89.624222, "avg_price": "$$"},
    {"name": "Soriana Montejo", "lat": 20.987654, "lng": -89.618765, "avg_price": "$$"},
    {"name": "Chedraui Itzaes", "lat": 20.976543, "lng": -89.632109, "avg_price": "$"},
    {"name": "Bodega Aurrera", "lat": 20.991234, "lng": -89.621987, "avg_price": "$"},
    {"name": "La Comer", "lat": 20.985432, "lng": -89.627654, "avg_price": "$$$"}
]

@app.route('/')
def index():
    """Pantalla de inicio/Splash"""
    return render_template('index.html')

@app.route('/login')
def login():
    """Pantalla de registro/inicio de sesión"""
    return render_template('login.html')

@app.route('/home')
def home():
    """Pantalla principal con productos destacados"""
    return render_template('home.html', products=sample_products)

@app.route('/search')
def search():
    """Buscador de productos"""
    query = request.args.get('q', '')
    # Filtrar productos basado en la búsqueda
    if query:
        filtered_products = [p for p in sample_products if query.lower() in p['name'].lower() or query.lower() in p['category'].lower()]
    else:
        filtered_products = sample_products
    return render_template('search.html', query=query, products=filtered_products)

@app.route('/compare')
def compare():
    """Comparador de precios"""
    product_id = request.args.get('product_id', 1)
    product = next((p for p in sample_products if p["id"] == int(product_id)), sample_products[0])
    
    # Calcular mejor opción (precio + distancia)
    for store in product["stores"]:
        store["score"] = store["price"] + (store["distance"] * 5)  # Ponderación distancia
    
    best_option = min(product["stores"], key=lambda x: x["score"])
    best_option["is_best"] = True
    
    return render_template('compare.html', product=product)

@app.route('/map')
def map_view():
    """Mapa de tiendas"""
    return render_template('map.html', stores=sample_stores)

@app.route('/product/<int:product_id>')
def product_detail(product_id):
    """Detalle de producto"""
    product = next((p for p in sample_products if p["id"] == product_id), sample_products[0])
    return render_template('product.html', product=product)

@app.route('/cart')
def cart():
    """Carrito de compras"""
    cart_items = sample_products[:2]  # Simular productos en carrito
    return render_template('cart.html', cart_items=cart_items)

@app.route('/chat')
def chat():
    """Chat asistente"""
    return render_template('chat.html')

@app.route('/profile')
def profile():
    """Perfil de usuario"""
    return render_template('profile.html')

# APIs para funcionalidades dinámicas
@app.route('/api/products')
def api_products():
    """API para obtener productos"""
    return jsonify(sample_products)

@app.route('/api/stores')
def api_stores():
    """API para obtener tiendas"""
    return jsonify(sample_stores)

@app.route('/api/chat', methods=['POST'])
def api_chat():
    """API para el chat asistente"""
    data = request.json
    user_message = data.get('message', '')
    
    # Respuestas predefinidas del chatbot
    responses = {
        "leche": "En Soriana, la leche cuesta $23.50 y está a 1.2 km de ti.",
        "huevo": "En Walmart Altabrisa, el huevo cuesta $68.50 y está a 1.2 km de ti.",
        "frijol": "En Chedraui Itzaes, el frijol cuesta $35.50 y está a 3.5 km de ti.",
        "arroz": "En Soriana, el arroz cuesta $26.90 y está a 2.1 km de ti.",
        "aceite": "En Soriana, el aceite cuesta $42.50 y está a 2.1 km de ti."
    }
    
    # Buscar respuesta basada en palabras clave
    response = "Lo siento, no tengo información sobre ese producto en este momento. Puedo ayudarte con leche, huevo, frijol, arroz o aceite."
    for keyword, resp in responses.items():
        if keyword in user_message.lower():
            response = resp
            break
    
    return jsonify({"response": response})

if __name__ == '__main__':
    app.run(debug=True, port=5000)