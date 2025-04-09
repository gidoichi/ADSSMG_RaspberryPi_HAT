#!/usr/bin/env python3

import os
import sys

import bme280
import flask
import smbus2

sys.path.append("shellmag57")

from shellmag57.TP401T import TP401T
from shellmag57.VCNL4020 import VCNL4020

BME280_ADDR = 0x76
BUS_NO = 1

i2c = smbus2.SMBus(BUS_NO)
bme280.load_calibration_params(i2c, BME280_ADDR)

app = flask.Flask(__name__)

@app.route("/")
def sample():
    result = {
        "bme280": sample_bme280(),
        "tp401t": sample_tp401t(),
        "vcnl4020": sample_vcnl4020(),
    }
    return result

@app.route("/bme280")
def sample_bme280():
    data = bme280.sample(i2c, BME280_ADDR)
    result = {
        "enable": True,
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

@app.route("/tp401t")
def sample_tp401t():
    if os.path.exists(TP401T.SYSFS_PATH):
        sensor = TP401T()
        data = sensor.getVoltage(sensor.tp401_ch)
        result = {
            "enable": True,
            "odor": {
                "value": data,
            },
        }
        return result

    else:
        return {
            "enable": False,
            "message": f"not found: {TP401T.SYSFS_PATH}",
        }

@app.route("/vcnl4020")
def sample_vcnl4020():
    sensor = VCNL4020()
    result = {
        "enable": True,
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
