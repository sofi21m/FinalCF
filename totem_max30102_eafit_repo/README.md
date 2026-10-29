# 🩺 Dashboard Tótem MAX30102 - Universidad EAFIT

Aplicación web interactiva desarrollada en **Streamlit** para el análisis de indicadores fisiológicos ($BPM$ y $SpO_2$) y del comportamiento de uso de una estación de medición IoT basada en el sensor MAX30102.

## 🚀 Características
- **Filtros Interactivos:** Por rango de fechas, estado de la medición (válida/inválida) e identificador de estudiante.
- **KPIs Dinámicos:** Conteo total de mediciones, usuarios únicos, BPM promedio, SpO₂ promedio y tasa de mediciones inválidas.
- **Visualizaciones con Plotly:**
  - Evolución diaria de uso.
  - Distribución horaria de tráfico.
  - Histograma de Frecuencia Cardíaca (BPM).
  - Histograma de Saturación de Oxígeno (SpO₂).
- **Seguimiento Individual:** Histórico temporal dual de $BPM$ y $SpO_2$ por estudiante.
- **Sección de Hallazgos:** Análisis interpretativo sustentado en los datos.

## 📦 Estructura del Repositorio
```text
totem-max30102-eafit/
│
├── app.py                             # Aplicación principal de Streamlit
├── proyecto_integrador_eafit_max30102.csv  # Dataset con las mediciones
├── requirements.txt                   # Librerías requeridas
├── .gitignore                         # Exclusiones de Git
└── README.md                          # Documentación del proyecto
```

## ⚙️ Instalación y Ejecución Local

1. Clonar el repositorio:
   ```bash
   git clone https://github.com/TU_USUARIO/totem-max30102-eafit.git
   cd totem-max30102-eafit
   ```

2. Crear un entorno virtual e instalar dependencias:
   ```bash
   python -m venv venv
   source venv/bin/activate  # En Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

3. Ejecutar la aplicación:
   ```bash
   streamlit run app.py
   ```
