import __init__ as I

SolenoidPin = 23

Solenoid = I.SND.Solenoid(SolenoidPin)

hold = .5
I.time.sleep(10)
try:
    while True:
        Solenoid.SolenoidOPEN()
        I.time.sleep(hold)
        Solenoid.SolenoidCLOSE()
        I.time.sleep(hold)

except KeyboardInterrupt:
    print('great job... you made toast')

finally:
    I.RGPIO.cleanup()
    print('Isaac cleaned the oven...')


