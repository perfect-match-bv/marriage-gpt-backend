from flask import Flask, request, jsonify
import requests
from requests.auth import HTTPBasicAuth

app = Flask(__name__)

# ✅ YOUR KEYS (CORRECTLY FORMATTED)
OPENCAGE_KEY = "5f7c0bd164774d0ab4f27a3be1d4d80b"
ASTRO_USER = "651602"
ASTRO_KEY = "ak-240208097ce6b92616cdf6294cf4d5c03c086cf4"


def geocode(location):
    url = "https://api.opencagedata.com/geocode/v1/json"
    params = {"q": location, "key": OPENCAGE_KEY}
    res = requests.get(url, params=params).json()

    lat = res["results"][0]["geometry"]["lat"]
    lng = res["results"][0]["geometry"]["lng"]

    return lat, lng


def get_chart(data, lat, lng):
    url = "https://json.astrologyapi.com/v1/western_chart_data"

    payload = {
        "day": data["day"],
        "month": data["month"],
        "year": data["year"],
        "hour": data["hour"],
        "min": data["min"],
        "lat": lat,
        "lon": lng,
        "tzone": 5.5
    }

    response = requests.post(
        url,
        json=payload,
        auth=HTTPBasicAuth(ASTRO_USER, ASTRO_KEY)
    )

    return response.json()


@app.route("/generate-marriage-timeline", methods=["POST"])
def generate():
    data = request.json

    year, month, day = map(int, data["birth_date"].split("-"))
    hour, minute = map(int, data["birth_time"].split(":"))

    lat, lng = geocode(data["birth_location"])

    chart = get_chart({
        "day": day,
        "month": month,
        "year": year,
        "hour": hour,
        "min": minute
    }, lat, lng)

    timeline = {
        "phase_1": "Meeting / attraction phase",
        "phase_2": "Deep emotional bonding",
        "phase_3": "Merging lives / cohabitation",
        "phase_4": "Marriage / long-term commitment"
    }

    return jsonify({
        "timeline": timeline,
        "chart": chart
    })


if __name__ == "__main__":
    app.run(debug=True)
