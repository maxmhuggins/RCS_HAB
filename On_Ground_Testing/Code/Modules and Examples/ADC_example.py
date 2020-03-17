import __init__ as I

ADCChannel = 0

mcp = I.ADC.MCP3008()

while True:

    voltage = mcp.getVoltage(ADCChannel)
    print(voltage)
