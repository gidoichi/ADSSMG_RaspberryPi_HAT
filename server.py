#!/usr/bin/env python3

import logging
import os
import sys

import bme280
import flask
from dataclasses import dataclass
from typing import Optional
import smbus2
import waitress

sys.path.append("shellmag57")

from shellmag57.TP401T import TP401T
from shellmag57.VCNL4020 import VCNL4020

BME280_ADDR = 0x76
BUS_NO = 1

i2c = smbus2.SMBus(BUS_NO)
bme280.load_calibration_params(i2c, BME280_ADDR)

app = flask.Flask(__name__)

@dataclass
class SensorData:
    value: float
    unit: Optional[str] = None

@app.route("/")
def sample() -> dict[str, dict[str, bool|str|SensorData]]:
    result: dict[str, dict[str, bool|str|SensorData]] = {
        "bme280": sample_bme280(),
        "tp401t": sample_tp401t(),
        "vcnl4020": sample_vcnl4020(),
    }
    return result

@app.route("/bme280")
def sample_bme280() -> dict[str, bool|str|SensorData]:
    data = bme280.sample(i2c, BME280_ADDR)
    result: dict[str, bool|str|SensorData] = {
        "enable": True,
        "temperature": SensorData(value=data.temperature, unit="°C"),
        "humidity": SensorData(value=data.humidity, unit="%rH"),
        "pressure": SensorData(value=data.pressure, unit="hPa"),
    }
    return result

@app.route("/tp401t")
def sample_tp401t() -> dict[str, bool|str|SensorData]:
    if os.path.exists(TP401T.SYSFS_PATH):
        sensor = TP401T()
        data = sensor.getVoltage(sensor.tp401_ch)
        result: dict[str, bool|str|SensorData] = {
            "enable": True,
            "odor": SensorData(value=data),
        }
        return result

    else:
        return {
            "enable": False,
            "message": f"not found: {TP401T.SYSFS_PATH}",
        }

@app.route("/vcnl4020")
def sample_vcnl4020() -> dict[str, bool|str|SensorData]:
    sensor = VCNL4020()
    result: dict[str, bool|str|SensorData] = {
        "enable": True,
        "proximity": SensorData(value=sensor.proximity),
        "luminance": SensorData(value=sensor.luminance, unit="lux"),
    }
    return result

if __name__ == "__main__":
    logging.getLogger('waitress').setLevel(logging.INFO)

    waitress.serve(app)
