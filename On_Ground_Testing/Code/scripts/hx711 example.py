import time
import sys

EMULATE_HX711=False

referenceUnit = 954.5

if not EMULATE_HX711:
    import RPi.GPIO as GPIO
    from hx711 import HX711
else:
    from emulated_hx711 import HX711

def cleanAndExit():
    print("Cleaning...")

    if not EMULATE_HX711:
        GPIO.cleanup()
        
    print("Bye!")
    sys.exit()

hx = HX711(5, 6)

hx.set_reading_format("MSB", "MSB")

hx.set_reference_unit(referenceUnit)

hx.reset()

hx.tare()

print("Tare done! Add weight now...")

try:
    while True:
        val = round(hx.get_weight(5),4)
        print(val)

except (KeyboardInterrupt, SystemExit):
    cleanAndExit()
