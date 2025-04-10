from flask import Flask, request
from datetime import datetime
from dotenv import load_dotenv
from middleware.auth_middleware import jwt_required
from controller import users_controller, bookings_controller, racks_controller
from database import racks_repo, users_repo, bookings_repo
import utils


app = Flask(__name__)


@app.route("/")
def hello_world():
    return "Hello World"


@app.route("/confirm", methods=["POST"])
@jwt_required
def confirm(username):
    data = request.get_json()
    if "rack_id" not in data:
        return "Rack ID field missing", 400
    rack_id = data["rack_id"]
    return bookings_controller.confirm_booking(username, rack_id)


@app.route("/get_bookings", methods=["GET"])
@jwt_required
def get_booking(username):
    return bookings_controller.get_bookings(username)


@app.route("/book", methods=["POST"])
@jwt_required
def book(username):
    data = request.get_json()
    if "rack_id" not in data:
        return "Rack ID field missing", 400
    if "booking_time" not in data:
        return "Booking time field missing", 400
    if not racks_repo.rack_exists(data["rack_id"]):
        return "Invalid rack chosen", 400
    try:
        booking_time = datetime.strptime(
            data["booking_time"], "%Y-%m-%d %H:%M:%S.%f")
        rack_id = data["rack_id"]
        return bookings_controller.create_booking(
            username,
            rack_id,
            booking_time
        )
    except Exception:
        return "Invalid booking time", 400


@app.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    if "username" not in data:
        return "Username field missing", 400
    if "password" not in data:
        return "Password field missing", 400
    username = data["username"]
    password = data["password"]
    return users_controller.login(username, password)


@app.route("/clear", methods=["POST"])
@jwt_required
def clear_booking(username):
    data = request.get_json()
    if "rack_id" not in data:
        return "Rack ID field missing", 400
    rack_id = data["rack_id"]
    return bookings_controller.clear_booking(username, rack_id)


@app.route("/register", methods=["POST"])
def register():
    data = request.get_json()
    if "username" not in data:
        return "Username field missing", 400
    if "password" not in data:
        return "Password field missing", 400
    username = data["username"]
    password = data["password"]
    return users_controller.register(username, password)


@app.route("/data", methods=["GET"])
def get_data():
    lat = request.args.get("Lat", default=None, type=float)
    long = request.args.get("Long", default=None, type=float)
    dist = request.args.get("Dist", default=0.5, type=float)
    limit = request.args.get("Limit", default=None, type=int)
    if lat is None:
        return "Missing Lat parameter", 400
    if long is None:
        return "Missing Long parameter", 400
    return racks_controller.get_rack_data(lat, long, dist, limit)


@app.route("/logout", methods=["GET"])
def logout():
    return users_controller.logout()


if __name__ == "__main__":
    load_dotenv()
    bookings_repo.init()
    users_repo.init()
    racks_repo.init()
    # fetching bicycle rack info from API. Only needs to be run once
    # utils.get_bicycle_rack_data()
    app.run(host="0.0.0.0")
