from flask import Blueprint, jsonify, request

from app.models.restaurant_model import Restaurant
from app.utils.decorators import jwt_required, roles_required
from app.views.restaurant_view import render_restaurant_detail, render_restaurant_list

# Crear un blueprint para el controlador de animales
restaurant_bp = Blueprint("restaurant", __name__)


# Ruta para obtener la lista de animales
@restaurant_bp.route("/restaurants", methods=["GET"])
@jwt_required
@roles_required(roles=["admin", "customer"])
def get_restaurants():
    restaurants = Restaurant.get_all()
    return jsonify(render_restaurant_list(restaurants))


# Ruta para obtener un restaurant específico por su ID
@restaurant_bp.route("/restaurants/<int:id>", methods=["GET"])
@jwt_required
@roles_required(roles=["admin", "customer"])
def get_restaurant(id):
    restaurant = Restaurant.get_by_id(id)
    if restaurant:
        return jsonify(render_restaurant_detail(restaurant))
    return jsonify({"error": "Restaurant no encontrado"}), 404


# Ruta para crear un nuevo restaurant
@restaurant_bp.route("/restaurants", methods=["POST"])
@jwt_required
@roles_required(roles=["admin"])
def create_restaurant():
    data = request.json
    name = data.get("name")
    address = data.get("address")
    city = data.get("city")
    phone = data.get("phone")
    description = data.get("description")
    rating = data.get("rating")

    # Validación simple de datos de entrada
    if not name or not address or city or phone or description or rating is None:
        return jsonify({"error": "Faltan datos requeridos"}), 400

    # Crear un nuevo restaurant y guardarlo en la base de datos
    restaurant = Restaurant(name=name, address=address, city=city, phone=phone, description=description, rating=rating)
    restaurant.save()

    return jsonify(render_restaurant_detail(restaurant)), 201


# Ruta para actualizar un restaurant existente
@restaurant_bp.route("/restaurants/<int:id>", methods=["PUT"])
@jwt_required
@roles_required(roles=["admin"])
def update_restaurant(id):
    restaurant = Restaurant.get_by_id(id)

    if not restaurant:
        return jsonify({"error": "Restaurant no encontrado"}), 404

    data = request.json
    name = data.get("name")
    address = data.get("address")
    city = data.get("city")
    phone = data.get("phone")
    description = data.get("description")
    rating = data.get("rating")

    # Actualizar los datos del restaurant
    restaurant = Restaurant(name=name, address=address, city=city, phone=phone, description=description, rating=rating)

    return jsonify(render_restaurant_detail(restaurant))


# Ruta para eliminar un restaurant existente
@restaurant_bp.route("/restaurants/<int:id>", methods=["DELETE"])
@jwt_required
@roles_required(roles=["admin"])
def delete_animal(id):
    restaurant = Restaurant.get_by_id(id)

    if not restaurant:
        return jsonify({"error": "Restaurant no encontrado"}), 404
    restaurant.delete()

    return "", 204
