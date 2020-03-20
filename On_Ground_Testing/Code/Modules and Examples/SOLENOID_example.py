import __init__ as I

Solenoid = 18

I.RGPIO.setmode(I.RGPIO.BCM)
I.RGPIO.setup(Solenoid, I.RGPIO.OUT)

while True:
    I.RGPIO.output(Solenoid, True)
    I.time.sleep(1)
    I.RGPIO.output(Solenoid, False)
    I.time.sleep(1)
