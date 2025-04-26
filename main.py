from flask import Flask, request, jsonify
import json
import os

app = Flask(__name__)

ORDERS_FILE = "pending_orders.json"

VALID_CITIES = [
    "Adana", "Adıyaman", "Afyonkarahisar", "Ağrı", "Aksaray", "Amasya", "Ankara", "Antalya", "Artvin", "Aydın",
    "Balıkesir", "Bartın", "Batman", "Bayburt", "Bilecik", "Bingöl", "Bitlis", "Bolu", "Burdur", "Bursa",
    "Çanakkale", "Çankırı", "Çorum", "Denizli", "Diyarbakır", "Düzce", "Edirne", "Elazığ", "Erzincan",
    "Erzurum", "Eskişehir", "Gaziantep", "Giresun", "Gümüşhane", "Hakkari", "Hatay", "Iğdır", "Isparta",
    "İstanbul", "İzmir", "Kahramanmaraş", "Karabük", "Karaman", "Kars", "Kastamonu", "Kayseri", "Kırıkkale",
    "Kırklareli", "Kırşehir", "Kilis", "Kocaeli", "Konya", "Kütahya", "Malatya", "Manisa", "Mardin",
    "Mersin", "Muğla", "Muş", "Nevşehir", "Niğde", "Ordu", "Osmaniye", "Rize", "Sakarya", "Samsun", "Siirt",
    "Sinop", "Sivas", "Şanlıurfa", "Şırnak", "Tekirdağ", "Tokat", "Trabzon", "Tunceli", "Uşak", "Van",
    "Yalova", "Yozgat", "Zonguldak"
]

def save_order(data):
    if os.path.exists(ORDERS_FILE):
        with open(ORDERS_FILE, "r") as f:
            orders = json.load(f)
    else:
        orders = []
    orders.append(data)
    with open(ORDERS_FILE, "w") as f:
        json.dump(orders, f, indent=2)

def validate_city(address_city, full_address):
    if address_city.lower() not in [c.lower() for c in VALID_CITIES]:
        for city in VALID_CITIES:
            if city.lower() in full_address.lower():
                return city
        return ""
    return address_city

@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.get_json()
    try:
        shipping = data["shipping_address"]
        city = validate_city(shipping.get("province", ""), shipping.get("address1", ""))

        order_data = {
            "order_id": data["id"],
            "name": data["name"],
            "address": shipping.get("address1", ""),
            "city": city,
            "phone": shipping.get("phone", ""),
            "price": data["total_price"],
            "cod": data["financial_status"] == "pending"
        }

        save_order(order_data)
        return jsonify({"success": True, "message": "Order saved."})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 400

@app.route("/orders", methods=["GET"])
def get_orders():
    try:
        with open(ORDERS_FILE, "r", encoding="utf-8") as f:
            orders = json.load(f)
        return jsonify(orders)
    except:
        return jsonify([])

@app.route("/", methods=["GET"])
def home():
    return "Sistem çalışıyor ✅"

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=10000)
