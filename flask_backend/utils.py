from database import racks_repo
import geopy.distance
import os
import requests


def get_distance_km(
        lat1: float,
        long1: float,
        lat2: float,
        long2: float
) -> float:
    return geopy.distance.geodesic((lat1, long1), (lat2, long2)).km


def get_bicycle_rack_data():
    headers = {"accountKey": os.getenv("datamall_api_key")}
    r = requests.get(
        "http://datamall2.mytransport.sg/ltaodataservice/BicycleParkingv2"
        + "?Lat=1.3483"
        + "&Long=103.6831"
        + "&Dist=20",
        headers=headers)
    racks = r.json()["value"]
    for rack in racks:
        racks_repo.add_rack(
            description=rack["Description"],
            latitude=rack["Latitude"],
            longitude=rack["Longitude"],
            rack_type=rack["RackType"],
            rack_count=rack["RackCount"],
            shelter_indicator=rack["ShelterIndicator"],

        )
