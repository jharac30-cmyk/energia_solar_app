# energia_solar_app
Simulador de Generación Fotovoltaica: Cálculo del potencial solar para paneles solares


Este proyecto en Python calcula la generación fotovoltaica y el potencial solar para paneles solares a través de:

- Cálculo de la posición solar (altitud y azimut).
- Cálculo de la irradiancia en plano inclinado (POA).
- Estimación diaria de la producción de energía de un panel fotovoltaico.

Los resultados se entregan en un archivo Excel con datos horarios y gráficas que muestran la posición solar y la producción FV.

---

## Requisitos

- Python 3.8 o superior  
- Librerías necesarias:
  - numpy  
  - pandas  
  - matplotlib  
  - openpyxl  

---

## Instalación de dependencias

Instala las librerías ejecutando en la terminal.
Puedes instalar todas las dependencias con un solo comando:

```bash
pip install numpy pandas matplotlib openpyxl
```
---

## Ejecución

Sigue estos pasos para ejecutar el simulador:

1. Abre una terminal o línea de comandos.  
2. Navega hasta el directorio donde se encuentra el archivo `proyecto1.py`
3. Ejecuta el script:
El programa solicitará por consola los siguientes datos:

- Latitud y longitud en grados decimales
- Fecha (formato YYYY-MM-DD)
- Inclinación y azimut del panel
- Área del panel en metros cuadrados (m²) y eficiencia en %

---

## Resultados Generados

Al finalizar la ejecución, el programa genera automáticamente:

- Un archivo Excel con los resultados horarios: `Resultados_produccion_solar_Jhara.xlsx`
- Gráficas de:
  - Altitud solar a lo largo del día
  - Producción fotovoltaica (teórica y simulada)

---

## Ejemplo de salida

RESUMEN DE PRODUCCIÓN DIARIA
Ubicación: Lat -16.5°, Long -68.1°
Fecha: 2025-09-05
Panel: 1.6 m², 18% eficiencia
Orientación: 25° inclinación, 180° azimut

--------------------------------------------------
Energía total teórica: 5.234 kWh
Energía total real (simulada): 4.982 kWh

---



