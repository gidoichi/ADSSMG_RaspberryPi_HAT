#!/usr/bin/env python3

import logging

import bme280
import flask
import smbus2

BME280_ADDR = 0x76
BUS_NO = 1

i2c = smbus2.SMBus(BUS_NO)
bme280.load_calibration_params(i2c, BME280_ADDR)

app = flask.Flask(__name__)
werkzeug_logger = logging.getLogger("werkzeug")
werkzeug_logger.setLevel(logging.WARNING)

@app.route("/")
@app.route("/<path:_>")
def sample(_=None):
    data = bme280.sample(i2c, BME280_ADDR)
    result = {
        "adssmg02": {
            "temperature": {
                "value": data.temperature,
                "unit": "°C",
            },
            "humidity": {
                "value": data.humidity,
                "unit": "%rH",
            },
            "pressure": {
                "value": data.pressure,
                "unit": "hPa",
            },
        },
    }
    return result

if __name__ == "__main__":
    app.run(host="0.0.0.0")
