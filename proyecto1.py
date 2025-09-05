# -*- coding: utf-8 -*-
"""
Created on Thu Sep  4 21:40:28 2025

@author: YARA
"""


"""
proyecto1.py
------------------------------------------------------
Modelo claro y didáctico para calcular:
- Posición solar (altitud, azimut)
- Irradiancia en plano inclinado (POA)
- Producción de energía de un módulo FV (modelo simplificado)

Autor: Jhara Castañez Martínez


Convenciones:
- Latitud (phi): grados +N, -S
- Longitud (lon): grados +E, -W
- Azimut solar (Az_sun): 0° = Norte, 90° = Este, 180° = Sur, 270° = Oeste
- Inclinación panel (beta): 0° = horizontal, 90° = vertical
- Azimut panel (γ): 0° = Norte, 90° = Este, 180° = Sur, 270° = Oeste
- Día juliano simple: número de día del año (1..365/366)
"""


#DISEÑO DE UN SISTEMA SOLAR 

#LIBRERIAS
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime


# ENTRADAS DEL USUARIO
print("    SIMULADOR DE ENERGÍA SOLAR PV")
latitud = float(input("Ingrese la latitud en grados decimales: "))
longitud = float(input("Ingrese la longitud en grados decimales: "))
fecha_str = input("Ingrese la fecha en formato 'YYYY-MM-DD': ")
inclinacion_panel = float(input("Ingrese la inclinación del panel en grados: "))
azimut_panel = float(input("Ingrese el azimut del panel en grados: "))
area_panel = float(input("Ingrese el área del panel en m²: "))
eficiencia_panel = float(input("Ingrese la eficiencia del panel en %: "))

albedo = 0.2  # Superficie terrestre promedio

# CONVERSIONES A RADIANES
latitud_rad = np.deg2rad(latitud)
beta = np.deg2rad(inclinacion_panel)  # inclinación del panel
gamma = np.deg2rad(azimut_panel)      # orientación del panel


# TIEMPO
#Definimos el intervalo de simulación: cada 15 minutos en un día
Tiempo = np.arange(0, 24, 0.25)  # cada 15 minutos
fecha_base = datetime.strptime(fecha_str, "%Y-%m-%d")
fechas = pd.date_range(start=fecha_base, periods=len(Tiempo), freq='15min')

# DÍA DEL AÑO Y DECLINACIÓN
dia_del_año = fecha_base.timetuple().tm_yday
declinacion = 23.45 * np.sin(np.deg2rad(360*(284 + dia_del_año)/365))
declinacion_rad = np.deg2rad(declinacion)


# ECUACIÓN DEL TIEMPO Y CORRECCIÓN LONGITUD
B = 2 * np.pi * (dia_del_año - 81) / 364
ET = 9.87 * np.sin(2*B) - 7.53 * np.cos(B) - 1.5 * np.sin(B)  # minutos
meridiano_huso = round(longitud / 15) * 15
correccion_longitud = (meridiano_huso - longitud)/15  # horas

# HORA SOLAR VERDADERO Y ANGULO HORARIO
Hora_solar_verdadera = Tiempo + correccion_longitud + ET/60
Angulo_horario_rad = np.deg2rad(15 * (Hora_solar_verdadera - 12))

# Hora civil en decimales (0–24 h)
Hora_decimal_civil = Tiempo  

# Hora solar ajustada en decimales (0–24 h)
#Ajustada con longitud y ecuación del tiempo
Hora_solar_decimal = np.mod(Hora_solar_verdadera + meridiano_huso/15, 24)


# ÁNGULO DE ALTITUD Y AZIMUT SOLAR 
# Altitud solar(ángulo sobre el horizonte)
sin_alt = (np.sin(declinacion_rad)*np.sin(latitud_rad) +
           np.cos(declinacion_rad)*np.cos(latitud_rad)*np.cos(Angulo_horario_rad))
altitud_solar_deg = np.rad2deg(np.arcsin(np.clip(sin_alt, 0, 1)))

# Azimut solar (ángulo respecto al norte, sentido horario)
azimut_solar_rad = np.arctan2(
    -np.sin(Angulo_horario_rad),
    np.cos(Angulo_horario_rad)*np.sin(latitud_rad) - np.tan(declinacion_rad)*np.cos(latitud_rad)
)
azimut_solar_deg = (np.rad2deg(azimut_solar_rad) + 360) % 360


# IRRADIANCIA (DNI, DHI, GHI) MODELO SIMPLIFICADO 
DNI = np.zeros_like(sin_alt)    #irradiancia directa normal
positive = sin_alt > 0
DNI[positive] = 1.4883 * (0.7 ** (sin_alt[positive] ** -0.678)) * 1000.0
DHI = 0.15 * DNI      # difusa
GHI = DNI * sin_alt + DHI    # global horizontal


# ÁNGULO DE INCIDENCIA Y PRODUCCIÓN FV
#Cos(θi): ángulo entre los rayos solares y el panel
cos_theta_i = (
    np.sin(declinacion_rad)*np.sin(latitud_rad)*np.cos(beta)
    - np.sin(declinacion_rad)*np.cos(latitud_rad)*np.sin(beta)*np.cos(gamma)
    + np.cos(declinacion_rad)*np.cos(latitud_rad)*np.cos(beta)*np.cos(Angulo_horario_rad)
    + np.cos(declinacion_rad)*np.sin(latitud_rad)*np.sin(beta)*np.cos(gamma)*np.cos(Angulo_horario_rad)
    + np.cos(declinacion_rad)*np.sin(beta)*np.sin(gamma)*np.sin(Angulo_horario_rad)
)
cos_theta_i = np.clip(cos_theta_i, 0, None)

# Irradiancia total en plano inclinado del panel
G_tilt = DNI * cos_theta_i + DHI*(1 + np.cos(beta))/2 + GHI*albedo*(1 - np.cos(beta))/2

# Potencia instantánea (teórica y simulada)
Produccion_teorica = G_tilt * area_panel * (eficiencia_panel/100) / 1000.0
produccion_real = Produccion_teorica * (0.95 + 0.05 * np.sin(np.linspace(0,4*np.pi,len(Produccion_teorica))))


# CÁLCULO DE ENERGÍA DIARIA TOTAL
delta_t = 0.25  # intervalo en horas (15 minutos)
energia_total_kwh = np.trapz(Produccion_teorica, dx=delta_t)
energia_real_kwh = np.trapz(produccion_real, dx=delta_t)


# MOSTRAR RESULTADOS EN PANTALLA
print("-"*50)
print("RESUMEN DE PRODUCCIÓN DIARIA")
print(f"Ubicación: Lat {latitud}°, Long {longitud}°")
print(f"Fecha: {fecha_str}")
print(f"Panel: {area_panel} m², {eficiencia_panel}% eficiencia")
print(f"Orientación: {inclinacion_panel}° inclinación, {azimut_panel}° azimut")
print("-"*50)
print(f"Energía total teórica: {energia_total_kwh:.3f} kWh")
print(f"Energía total real (simulada): {energia_real_kwh:.3f} kWh")



# CREAR DATAFRAME Y EXPORTAR EXCEL
df = pd.DataFrame({
    "Fecha_Hora": fechas,
    "Hora_decimal_civil": Hora_decimal_civil,
    "Hora_solar_decimal": Hora_solar_decimal,
    "Altitud_solar_deg": altitud_solar_deg,
    "Azimut_solar_deg": azimut_solar_deg,
    "DNI_Wm2": DNI,
    "DHI_Wm2": DHI,
    "GHI_Wm2": GHI,
    "Produccion_Teorica_kW": Produccion_teorica,
    "Produccion_Real_kW": produccion_real
})
df.to_excel("Resultados_produccion_solar_Jhara.xlsx", index=False)

print("\nSimulación finalizada. Resultados guardados en 'Resultados_produccion_solar_Jhara.xlsx'")



# GRÁFICOS
## Gráfico 1: altitud solar
plt.figure(figsize=(12,6))
plt.plot(fechas, altitud_solar_deg, color="red", linewidth=2)
plt.title(f"Altitud solar vs Hora del día ({fecha_str})")
plt.xlabel("Hora del día")
plt.ylabel("Altitud solar (°)")
plt.grid(True)
plt.gca().xaxis.set_major_formatter(mdates.DateFormatter("%H:%M"))
plt.gcf().autofmt_xdate()

# Gráfico 2: Producción FV
plt.figure(figsize=(12,6))
plt.plot(fechas, Produccion_teorica, label="Producción Teórica", color="orange", linewidth=2)
plt.plot(fechas, produccion_real, ".-", label="Producción Real Simulada", color="green")
plt.title("Producción estimada del panel solar a lo largo del día")
plt.xlabel("Hora del día")
plt.ylabel("Potencia (kW)")

plt.ylim(-0.02, max(Produccion_teorica)*1.2) 

plt.legend()
plt.grid(True)
plt.tight_layout()
plt.gca().xaxis.set_major_formatter(mdates.DateFormatter("%H:%M"))
plt.gcf().autofmt_xdate()
plt.show()