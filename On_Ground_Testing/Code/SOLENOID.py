import __init__ as I

class Solenoid:
    
    def __init__(self, BCMPin):
        self.BCMPin = BCMPin
        I.RGPIO.setmode(I.RGPIO.BCM)
        I.RGPIO.setup(BCMPin, I.RGPIO.OUT)

    def SolenoidOPEN(self):
        I.RGPIO.output(self.BCMPin, True)

    def SolenoidCLOSE(self):
        I.RGPIO.output(self.BCMPin, False)
