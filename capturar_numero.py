'''funcao para obter e retornar a temperatura do CPU
Hardware: Intel Core i3-7020U
  Sensor: CPU Package | Tipo: Temperature | Valor: None
'''
import clr
import time
import os

# Carrega a DLL
clr.AddReference(r'C:\OpenHardwareMonitor\OpenHardwareMonitorLib.dll')

from OpenHardwareMonitor import Hardware
from OpenHardwareMonitor.Hardware import SensorType

# Inicializa o monitor
computer = Hardware.Computer()
computer.MainboardEnabled = True
computer.CPUEnabled = True
computer.GPUEnabled = True
computer.FanControllerEnabled = True
computer.ChipsetEnabled = True
computer.HDDEnabled = True
computer.Open()

print('arquivo obrigatorio:  C:\OpenHardwareMonitor\OpenHardwareMonitorLib.dll')
print('Executando comunicação com DLL OpenHardwareMonitor...\n\n')

def get_values():
    cpu_fan = None
    cpu_temp = None
    cpu_load = None
    mem_load = None
    gpu_temp = None
    gpu_load = None
    gpu_fan = None

    for hardware in computer.Hardware:
        hardware.Update()
        for sensor in hardware.Sensors:
            if ('Intel X99' in hardware.Name):
                if ('Fan #2' in sensor.Name):
                    cpu_fan = sensor.Value
            elif ('Intel Core i3-7020U' in hardware.Name):
                if ('CPU Package' in sensor.Name) and (cpu_temp is None) and (sensor.SensorType == SensorType.Temperature):
                    cpu_temp = sensor.Value
                elif ('CPU Total' in sensor.Name) and (cpu_load is None) and (sensor.SensorType == SensorType.Load):
                    cpu_load = sensor.Value
            elif ('Generic Memory' in hardware.Name):
                if ('Memory' in sensor.Name) and (mem_load is None):
                    mem_load = sensor.Value
            elif ('NVIDIA' in hardware.Name):
                if ('GPU Core' in sensor.Name) and (gpu_temp is None) and (sensor.SensorType == SensorType.Temperature):
                    gpu_temp = sensor.Value
                elif ('GPU Core' in sensor.Name) and (gpu_load is None) and (sensor.SensorType == SensorType.Load):
                    gpu_load = sensor.Value
                elif ('GPU' in sensor.Name) and (gpu_fan is None) and (sensor.SensorType == SensorType.Fan):
                    gpu_fan = sensor.Value
                    
#    return cpu_fan, cpu_temp, cpu_load, mem_load, gpu_temp, gpu_load, gpu_fan
#    print('resultados:', cpu_fan, cpu_temp, cpu_load, mem_load, gpu_temp, gpu_load, gpu_fan)

    output_lines = []

    if gpu_temp > 74:
        output_lines.append("\n GPU TEMP ALERT!\n")

    if gpu_temp is not None:
        output_lines.append(f"GPU Temp:  {gpu_temp:.0f} C")
#    else:
#        output_lines.append("GPU Temp:  N/A")

    if gpu_load is not None:
        output_lines.append(f"GPU Load:  {gpu_load:.0f} % ")
#    else:
#        output_lines.append("GPU Load:  N/A")

    if gpu_fan is not None:
        output_lines.append(f"GPU Fan:  {gpu_fan:.0f}RPM")
#    else:
#        output_lines.append("GPU Fan    N/A")

    if cpu_temp is not None:
        output_lines.append(f"CPU Temp:  {cpu_temp:.0f} C")
#    else:
#        output_lines.append("CPU Temp:  N/A")

    if cpu_load is not None:
        output_lines.append(f"CPU Load:  {cpu_load:.0f} % ")
#    else:
#        output_lines.append("CPU Load:  N/A")

    if mem_load is not None:
        output_lines.append(f"RAM Load:  {mem_load:.0f} % ")
#    else:
#        output_lines.append("RAM Load:  N/A")

    if cpu_fan is not None:
        output_lines.append(f"CPU Fan: {cpu_fan:.0f}RPM")
#    else:
#        output_lines.append("CPU Fan:   N/A")

    # Junta tudo em uma única string
    output = "\n".join(output_lines)
#    output = ">".join(output_lines)
    if (output == None): output = 'Nenhum sensor compativel'
    return output
#    print(output)

def capturar_temp():
    cpu_temp = None
    cpu_load = None

    for hardware in computer.Hardware:
        hardware.Update()
        for sensor in hardware.Sensors:
            if ('Intel Core i3-7020U' in hardware.Name):
                if ('CPU Package' in sensor.Name) and (cpu_temp is None) and (sensor.SensorType == SensorType.Temperature):
                    cpu_temp = sensor.Value
                elif ('CPU Total' in sensor.Name) and (cpu_load is None) and (sensor.SensorType == SensorType.Load):
                    cpu_load = sensor.Value

    if cpu_temp is not None:
        output = f"{cpu_temp:.0f}"
    else:
        output = f"{cpu_load:.0f}"
        print('nao foi possivel obter CPU Temp. CPU LOAD:', end=' ')

    print(output)
    return output

# Atualiza e lista sensores
log_lines = []  # lista para acumular as linhas

for hardware in computer.Hardware:
    hardware.Update()
    header = f"\nHardware: {hardware.Name}"
    print(header)
    log_lines.append(header)

    for sensor in hardware.Sensors:
        line = f"  Sensor: {sensor.Name} | Tipo: {sensor.SensorType} | Valor: {sensor.Value}"
        print(line)
        log_lines.append(line)

# Salva no arquivo 'sensors.txt'
with open("sensors.txt", "w", encoding="utf-8") as f:
    f.write("\n".join(log_lines) + "\n")
print('\nArquivo sensors.txt atualizado com itens disponiveis')

#executar se essa for o modulo principal:
if __name__ == "__main__":
    print('\n---- executando modulo isolado ----\n')
    while True:
        capturar_temp()
        time.sleep(5)

#x = input()
