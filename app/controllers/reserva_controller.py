from flask import Blueprint, jsonify, request

from app.models.reserva_model import Reserva
from app.utils.decorators import jwt_required, roles_required
from app.views.reserva_view import render_reservation_detail, render_reservation_list

# Crear un blueprint para el controlador de animales
reserva_bp = Blueprint("reserva", __name__)


# Ruta para obtener la lista de animales
@reserva_bp.route("/reservations", methods=["GET"])
@jwt_required
@roles_required(roles=["admin", "customer"])
def get_reservations():
    reserva = Reserva.get_all()
    return jsonify(render_reservation_list(reserva))


# Ruta para obtener un reserva específico por su ID
@reserva_bp.route("/reservations/<int:id>", methods=["GET"])
@jwt_required
@roles_required(roles=["admin", "customer"])
def get_restaurant(id):
    reserva = Reserva.get_by_id(id)
    if reserva:
        return jsonify(render_reservation_detail(reserva))
    return jsonify({"error": "Reserva no encontrado"}), 404


# Ruta para crear un nuevo reserva
@reserva_bp.route("/reservations", methods=["POST"])
@jwt_required
@roles_required(roles=["admin"])
def create_restaurant():
    data = request.json
    user_id = data.get("user_id")
    restaurant_id = data.get("restaurant_id")
    reservation_date = data.get("reservation_date")
    num_guests = data.get("num_guests")
    special_resquests = data.get("special_resquests")
    status = data.get("status")

    # Validación simple de datos de entrada
    if not user_id or not restaurant_id or reservation_date or num_guests or special_resquests or status is None:
        return jsonify({"error": "Faltan datos requeridos"}), 400

    # Crear un nuevo reserva y guardarlo en la base de datos
    reserva = Reserva(user_id=user_id, restaurant_id=restaurant_id, reservation_date=reservation_date, num_guests=num_guests, special_resquests=special_resquests, status=status)
    reserva.save()

    return jsonify(render_reservation_detail(reserva)), 201


# Ruta para actualizar un reserva existente
@reserva_bp.route("/reservations/<int:id>", methods=["PUT"])
@jwt_required
@roles_required(roles=["admin"])
def update_restaurant(id):
    reserva = Reserva.get_by_id(id)

    if not reserva:
        return jsonify({"error": "Reserva no encontrado"}), 404

    data = request.json
    user_id = data.get("user_id")
    restaurant_id = data.get("restaurant_id")
    reservation_date = data.get("reservation_date")
    num_guests = data.get("num_guests")
    special_resquests = data.get("special_resquests")
    status = data.get("status")

    # Actualizar los datos del reserva
    reserva = Reserva(user_id=user_id, restaurant_id=restaurant_id, reservation_date=reservation_date, num_guests=num_guests, special_resquests=special_resquests, status=status)

    return jsonify(render_reservation_detail(reserva))


# Ruta para eliminar un reserva existente
@reserva_bp.route("/reservations/<int:id>", methods=["DELETE"])
@jwt_required
@roles_required(roles=["admin"])
def delete_animal(id):
    reserva = Reserva.get_by_id(id)

    if not reserva:
        return jsonify({"error": "Reserva no encontrado"}), 404
    reserva.delete()

    return "", 204
