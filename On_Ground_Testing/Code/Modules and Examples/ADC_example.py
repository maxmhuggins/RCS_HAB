import __init__ as I

ADCChannel = 1

mcp = I.ADC.MCP3008()

while True:

    voltage = mcp.getVoltage(ADCChannel)
    print(voltage)
