import time
import ADC
import SPI
import TEMP
import SOLENOID as SND
import PRESSURE as PR
import numpy as np
import RPi.GPIO as RGPIO
from FORCE import HX711 as HX

def OutputEnable(OE):
    RGPIO.setmode(RGPIO.BCM)
    RGPIO.setup(OE, RGPIO.OUT)
    RGPIO.output(OE, True)
