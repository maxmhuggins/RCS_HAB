import __init__ as I

OE = 22

I.OutputEnable(OE)

ADCChannel = 2

mcp = I.ADC.MCP3008()

while True:

    voltage = mcp.getVoltage(ADCChannel)
    print(voltage)
