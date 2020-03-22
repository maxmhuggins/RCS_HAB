import __init__ as I

OE = 26

I.OutputEnable(OE)

ADCChannel = 0

mcp = I.ADC.MCP3008()

while True:

    voltage = mcp.getVoltage(ADCChannel)
    print(voltage)
