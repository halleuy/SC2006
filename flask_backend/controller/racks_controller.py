from flask import jsonify
from database import bookings_repo, racks_repo
from utils import get_distance_km


def get_rack_data(lat: float, long: float, dist: float, limit: int | None):
    eligible_racks = []
    bicycle_data = racks_repo.get_all_racks()
    for bicycle_rack in bicycle_data:
        distance = get_distance_km(
            lat, long, bicycle_rack["Latitude"], bicycle_rack["Longitude"])
        if distance < dist:
            new_bicycle_rack = bicycle_rack.copy()
            new_bicycle_rack["Distance"] = distance
            new_bicycle_rack["RackUsed"] = bookings_repo.get_rack_booking_count(
                bicycle_rack["Description"]
            )
            eligible_racks.append(new_bicycle_rack)
    # Sorted racks by distance
    eligible_racks.sort(key=lambda x: x["Distance"])

    if limit is None:
        return jsonify(eligible_racks)
    else:
        return jsonify(eligible_racks[:limit])
