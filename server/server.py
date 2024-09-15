from flask import Flask, jsonify
from flask_cors import CORS
from flask import request
import requests

from ads import AdsBank
from view_stats import AdStats
import time

app = Flask(__name__)
CORS(app)


ads_bank = AdsBank()


def get_ip_addr_info(ip_addr: str):
    if ip_addr == "127.0.0.1":
        # When running on localhost the remote_addr value will also be localhost
        # By setting to '', we instead get information about the public ip of the
        # client/server localhost. Note, this is just a hack so that the demo works
        # better locally, but unnecessary for a production environment.
        ip_addr = ""
    url = f"http://ip-api.com/json/{ip_addr}"
    res = requests.get(url)

    blank = {
        "country": "",
        "region": "",
        "region_code": "",
        "city": "",
        "zip": "",
    }

    if not res.ok:
        return blank

    data = res.json()
    if data["status"] != "success":
        return blank

    location_data = {
        "country": data.get("country", ""),
        "region": data.get("regionName", ""),
        "region_code": data.get("region", ""),
        "city": data.get("city", ""),
        "zip": data.get("zip", ""),
    }
    return location_data


@app.route("/api/ad", methods=["POST"])
def select_ad():
    data = request.json
    question = data["question"]
    history = data["history"]
    selected_ad = ads_bank.select_ad(question, history)

    return jsonify(selected_ad)


@app.route("/api/record", methods=["POST"])
def record_ad_view():
    location_data: dict[str, str] = get_ip_addr_info(request.remote_addr)
    if location_data is not None:
        print(location_data)

    data = request.json

    if "adId" in data and data["adId"] != "":
        AdStats.add_row(
            {
                "ad_id": data["adId"],
                "ad_duration": data["durationViewed"],
                "ip_addr": request.remote_addr,
                "time": time.time(),
                **location_data,
            }
        )

    return "OK"


if __name__ == "__main__":
    app.run(debug=True, port=8080)
