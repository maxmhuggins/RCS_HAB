import __init__

ADCChannel = 0

mcp = ADC.MCP3008()

while True:

    voltage = mcp.getVoltage(ADCChannel)
    print(voltage)
