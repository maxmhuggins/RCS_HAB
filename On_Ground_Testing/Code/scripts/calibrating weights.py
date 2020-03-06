import time
import sys

EMULATE_HX711=False

referenceUnit = 1

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


avgs = []
weights = [10,20,50,100,200,500]

try:
    for i in weights:
        q = 0
        del_t = 0
        cal = []
        q = input('Are you ready?')
        if q:  
            start_time = time.time()
            while del_t < 10:
                val = hx.get_weight(5)
##                print(val)
                cal.append(val)
                hx.power_down()
                hx.power_up()
                time.sleep(0.01)
                del_t = time.time() - start_time
        avg = sum(cal)/len(cal)
        print(avg)
        avgs.append(avg/i)
    total_average = sum(avgs)/len(avgs)
    print(total_average)
    
except (KeyboardInterrupt, SystemExit):
    cleanAndExit()
