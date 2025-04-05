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
def sample():
    result = {
        "bme280": sample_bme280(),
        "vcnl4020": sample_vcnl4020(),
    }
    return result

@app.route("/bme280")
def sample_bme280():
    data = bme280.sample(i2c, BME280_ADDR)
    result = {
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
    }
    return result

@app.route("/vcnl4020")
def sample_vcnl4020():
    from shellmag57.VCNL4020 import VCNL4020
    sensor = VCNL4020()
    result = {
        "proximity": {
            "value": sensor.proximity,
        },
        "luminance": {
            "value": sensor.luminance,
            "unit": "lux"
        },
    }
    return result

if __name__ == "__main__":
    app.run(host="0.0.0.0")
