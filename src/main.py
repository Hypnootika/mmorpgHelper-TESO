""" Main entry point for the Timed Event Scheduler Overlay """

from time import time
from logging import getLogger, info, error, INFO, DEBUG
from sys import exit, argv
from PyQt5.QtWidgets import QApplication
import os
from engine import overlay
from helper import config_helper
from random import randint
import asyncio

APPNAME = "Timed Event Scheduler Overlay"
APPVERSION = "v1.0.3-teso"


def main():
    app = QApplication(argv)
    app_gui = overlay.Overlay()
    app_gui.show()
    cfg = config_helper.read_config()
    getLogger().setLevel(DEBUG)

    info("Starting up " + APPNAME + " " + APPVERSION)
    info("Starting up bot engine...")
    info("Preset class " + cfg["class"] + " is initialized")

    exit(app.exec_())


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        error(e)
