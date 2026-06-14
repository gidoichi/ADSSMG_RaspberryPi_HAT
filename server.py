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

@dataclass
class ModuleData:
    enable: bool
    data: Optional[dict[str, SensorData]] = None
    message: Optional[str] = None

@app.route("/")
def sample() -> dict[str, ModuleData]:
    result: dict[str, ModuleData] = {
        "bme280": sample_bme280(),
        "tp401t": sample_tp401t(),
        "vcnl4020": sample_vcnl4020(),
    }
    return result

@app.route("/bme280")
def sample_bme280() -> ModuleData:
    data = bme280.sample(i2c, BME280_ADDR)
    result = ModuleData(
        enable=True,
        data={
            "temperature": SensorData(value=data.temperature, unit="°C"),
            "humidity": SensorData(value=data.humidity, unit="%rH"),
            "pressure": SensorData(value=data.pressure, unit="hPa"),
        },
    )
    return result

@app.route("/tp401t")
def sample_tp401t() -> ModuleData:
    if os.path.exists(TP401T.SYSFS_PATH):
        sensor = TP401T()
        data = sensor.getVoltage(sensor.tp401_ch)
        result = ModuleData(
            enable=True,
            data={
                "odor": SensorData(value=data),
            },
        )
        return result

    else:
        return ModuleData(
            enable=False,
            message=f"not found: {TP401T.SYSFS_PATH}",
        )

@app.route("/vcnl4020")
def sample_vcnl4020() -> ModuleData:
    sensor = VCNL4020()
    result = ModuleData(
        enable=True,
        data={
            "proximity": SensorData(value=sensor.proximity),
            "luminance": SensorData(value=sensor.luminance, unit="lux"),
        },
    )
    return result

if __name__ == "__main__":
    logging.getLogger('waitress').setLevel(logging.INFO)

    waitress.serve(app)
