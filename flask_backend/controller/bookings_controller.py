from datetime import datetime
from flask import jsonify
from database import bookings_repo, racks_repo


def confirm_booking(username: str, rack_id: str):
    bookings_repo.confirm_booking(username, rack_id)
    return "Confirmed", 200


def get_bookings(username: str):
    data = bookings_repo.get_bookings(username)
    return jsonify(data)


def create_booking(username: str, rack_id: str, booking_time: datetime):
    rack_limit = racks_repo.get_rack_limit(rack_id)
    if bookings_repo.get_rack_booking_count(rack_id) >= rack_limit:
        return "Rack is already full", 400
    if bookings_repo.add_booking(username, rack_id, booking_time):
        bookings_repo.prune_bookings()
        return "Booking Success"
    return "Booking already exists for your user!", 400


def clear_booking(username: str, rack_id: str):
    bookings_repo.clear_booking(username, rack_id)
    return "Cleared", 200
