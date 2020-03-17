import time
import ADC
import SPI
import TEMP
import PRESSURE as PR
import numpy as np
import RPi.GPIO as RGPIO
from FORCE import HX711 as HX
from GPIOTranslator import GPIODictionary as GD

OE = 26

RGPIO.setmode(RGPIO.BCM)
RGPIO.setup(OE, RGPIO.OUT)
RGPIO.output(OE, True)
