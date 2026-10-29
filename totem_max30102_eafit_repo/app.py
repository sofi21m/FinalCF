import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# Configuración de la página
st.set_page_config(
    page_title="Dashboard Tótem MAX30102 - EAFIT",
    page_icon="🩺",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Estilos CSS personalizados
st.markdown("""
<style>
    .main-header {
        font-size: 2.2rem;
        font-weight: 700;
        color: #1E293B;
        margin-bottom: 0.2rem;
    }
    .sub-header {
        font-size: 1rem;
        color: #64748B;
        margin-bottom: 1.5rem;
    }
    .metric-card {
        background-color: #F8FAFC;
        border: 1px solid #E2E8F0;
        border-radius: 8px;
        padding: 1rem;
        text-align: center;
    }
</style>
""", unsafe_allow_html=True)

@st.cache_data
def load_data():
    df = pd.read_csv('proyecto_integrador_eafit_max30102.csv')
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    df['date'] = df['timestamp'].dt.date
    df['hour'] = df['timestamp'].dt.hour
    df['day_name'] = df['timestamp'].dt.day_name()
    return df

try:
    df_raw = load_data()
except Exception as e:
    st.error(f"Error al cargar el archivo de datos: {e}")
    st.stop()

# --- BARRA LATERAL: FILTROS ---
st.sidebar.header("🔍 Filtros de Análisis")

min_date = df_raw['date'].min()
max_date = df_raw['date'].max()

date_range = st.sidebar.date_input(
    "Rango de Fechas",
    value=(min_date, max_date),
    min_value=min_date,
    max_value=max_date
)

status_options = ["Todos", "Válidas (valid)", "Inválidas (invalid)"]
selected_status = st.sidebar.selectbox("Estado de la Medición", status_options)

students_list = ["Todos"] + sorted(df_raw['student_id'].unique().tolist())
selected_student = st.sidebar.selectbox("Filtrar por Estudiante", students_list)

# Filtrado de datos
df_filtered = df_raw.copy()

if isinstance(date_range, tuple) and len(date_range) == 2:
    start_date, end_date = date_range
    df_filtered = df_filtered[(df_filtered['date'] >= start_date) & (df_filtered['date'] <= end_date)]

if selected_status == "Válidas (valid)":
    df_filtered = df_filtered[df_filtered['measurement_status'] == 'valid']
elif selected_status == "Inválidas (invalid)":
    df_filtered = df_filtered[df_filtered['measurement_status'] != 'valid']

if selected_student != "Todos":
    df_filtered = df_filtered[df_filtered['student_id'] == selected_student]

# --- ENCABEZADO ---
st.markdown('<div class="main-header">🩺 Dashboard Tótem MAX30102 - Universidad EAFIT</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-header">Análisis de Indicadores Fisiológicos y Comportamiento de Uso del Tótem IoT</div>', unsafe_allow_html=True)

# --- NAVEGACIÓN POR PESTAÑAS ---
tab1, tab2, tab3, tab4 = st.tabs([
    "📊 Indicadores y Visualizaciones",
    "👤 Seguimiento Individual",
    "🧠 Análisis e Interpretación",
    "📄 Registro de Datos"
])

# --- PESTAÑA 1: INDICADORES Y VISUALIZACIONES ---
with tab1:
    # Indicadores Generales (KPIs)
    total_measurements = len(df_filtered)
    unique_students = df_filtered['student_id'].nunique()
    
    valid_df = df_filtered[df_filtered['measurement_status'] == 'valid']
    avg_hr = valid_df['heart_rate_bpm'].mean() if not valid_df.empty else 0
    avg_spo2 = valid_df['spo2_percent'].mean() if not valid_df.empty else 0
    
    invalid_count = (df_filtered['measurement_status'] != 'valid').sum()
    invalid_pct = (invalid_count / total_measurements * 100) if total_measurements > 0 else 0

    col1, col2, col3, col4, col5 = st.columns(5)
    col1.metric("Total Mediciones", f"{total_measurements:,}")
    col2.metric("Estudiantes Únicos", f"{unique_students:,}")
    col3.metric("FC Promedio (Válidas)", f"{avg_hr:.1f} BPM" if avg_hr > 0 else "N/A")
    col4.metric("SpO₂ Promedio (Válidas)", f"{avg_spo2:.1f} %" if avg_spo2 > 0 else "N/A")
    col5.metric("Mediciones Inválidas", f"{invalid_pct:.1f}%", delta=f"{invalid_count} reg.", delta_color="inverse")

    st.markdown("---")

    # Visualizaciones
    c1, c2 = st.columns(2)
    
    with c1:
        st.subheader("📅 Evolución Diaria de Mediciones")
        daily_counts = df_filtered.groupby(['date', 'measurement_status']).size().reset_index(name='count')
        fig_daily = px.bar(
            daily_counts, x='date', y='count', color='measurement_status',
            title="Cantidad de mediciones por día",
            labels={'date': 'Fecha', 'count': 'Número de Mediciones', 'measurement_status': 'Estado'},
            color_discrete_map={'valid': '#0EA5E9', 'invalid': '#EF4444'}
        )
        st.plotly_chart(fig_daily, use_container_width=True)

    with c2:
        st.subheader("⏰ Horarios de Mayor Utilización")
        hourly_counts = df_filtered.groupby('hour').size().reset_index(name='count')
        fig_hourly = px.line(
            hourly_counts, x='hour', y='count', markers=True,
            title="Distribución de uso por hora del día (0-23 hrs)",
            labels={'hour': 'Hora del Día', 'count': 'Uso Total'},
            line_shape='spline'
        )
        fig_hourly.update_traces(line_color='#8B5CF6', line_width=3)
        st.plotly_chart(fig_hourly, use_container_width=True)

    c3, c4 = st.columns(2)
    
    with c3:
        st.subheader("💓 Distribución de Frecuencia Cardíaca (BPM)")
        if not valid_df.empty:
            fig_hr = px.histogram(
                valid_df, x='heart_rate_bpm', nbins=25,
                title="Distribución de BPM (Mediciones Válidas)",
                labels={'heart_rate_bpm': 'Frecuencia Cardíaca (BPM)'},
                color_discrete_sequence=['#10B981']
            )
            st.plotly_chart(fig_hr, use_container_width=True)
        else:
            st.info("No hay mediciones válidas para mostrar la distribución de BPM.")

    with c4:
        st.subheader("🫁 Distribución de Saturación de Oxígeno (SpO₂)")
        if not valid_df.empty:
            fig_spo2 = px.histogram(
                valid_df, x='spo2_percent', nbins=20,
                title="Distribución de SpO₂ % (Mediciones Válidas)",
                labels={'spo2_percent': 'SpO₂ (%)'},
                color_discrete_sequence=['#06B6D4']
            )
            st.plotly_chart(fig_spo2, use_container_width=True)
        else:
            st.info("No hay mediciones válidas para mostrar la distribución de SpO₂.")

# --- PESTAÑA 2: SEGUIMIENTO INDIVIDUAL ---
with tab2:
    st.subheader("👤 Seguimiento Histórico Individual")
    
    target_student = st.selectbox(
        "Seleccione un estudiante para consultar su historial:",
        options=sorted(df_raw['student_id'].unique().tolist()),
        key="student_tracker"
    )
    
    student_df = df_raw[df_raw['student_id'] == target_student].sort_values('timestamp')
    student_valid = student_df[student_df['measurement_status'] == 'valid']
    
    sc1, sc2, sc3, sc4 = st.columns(4)
    sc1.metric("ID Estudiante", target_student)
    sc2.metric("Total Mediciones", len(student_df))
    sc3.metric("Primera Medición", student_df['timestamp'].min().strftime('%d/%m/%Y %H:%M'))
    sc4.metric("Última Medición", student_df['timestamp'].max().strftime('%d/%m/%Y %H:%M'))
    
    st.markdown("---")
    
    st.subheader(f"📈 Evolución Fisiológica Temporal - {target_student}")
    
    if not student_df.empty:
        fig_ind = go.Figure()
        fig_ind.add_trace(go.Scatter(
            x=student_df['timestamp'], y=student_df['heart_rate_bpm'],
            mode='lines+markers', name='Frecuencia Cardíaca (BPM)',
            line=dict(color='#EF4444', width=2)
        ))
        fig_ind.add_trace(go.Scatter(
            x=student_df['timestamp'], y=student_df['spo2_percent'],
            mode='lines+markers', name='Saturación de Oxígeno (SpO₂ %)',
            line=dict(color='#0EA5E9', width=2), yaxis='y2'
        ))
        
        fig_ind.update_layout(
            title=f"Histórico Temporal de BPM y SpO₂ ({target_student})",
            xaxis=dict(title="Fecha y Hora"),
            yaxis=dict(title="Frecuencia Cardíaca (BPM)", titlefont=dict(color="#EF4444"), tickfont=dict(color="#EF4444")),
            yaxis2=dict(title="Saturación SpO₂ (%)", titlefont=dict(color="#0EA5E9"), tickfont=dict(color="#0EA5E9"), overlaying="y", side="right"),
            legend=dict(x=0.01, y=0.99),
            hovermode="x unified"
        )
        st.plotly_chart(fig_ind, use_container_width=True)
    else:
        st.warning("No se encontraron registros para este estudiante.")

# --- PESTAÑA 3: ANÁLISIS E INTERPRETACIÓN ---
with tab3:
    st.subheader("🧠 Hallazgos Relevantes y Análisis de Datos")
    
    st.markdown("""
    ### 1. Horarios y Días de Mayor Utilización
    - **Picos de Uso:** Los registros muestran una mayor concurrencia durante los días **miércoles (594 registros)** y **viernes (490 registros)**.
    - **Franja Horaria:** Se evidencia una alta concentración de uso en las horas de la tarde, destacando picos entre la **1:00 PM (14:00 h)** y las **6:00 PM (18:00 h)**, lo que coincide con los recesos entre clases del campus académico.

    ### 2. Comportamiento y Frecuencia de Uso por Estudiante
    - **Participación:** Un total de **295 estudiantes distintos** utilizaron la estación IoT durante el período evaluado.
    - **Frecuencia:** Cada estudiante realizó en promedio **9.04 mediciones**. El usuario con mayor cantidad de registros fue **`EST-0241`** con **21 interacciones**, demostrando una adopción recurrente del sistema.

    ### 3. Calidad de Señal y Variabilidad Fisiológica
    - **Tasa de Calidad:** Únicamente el **2.89%** ($77$ mediciones) resultaron inválidas por baja calidad de señal o mala posición del dedo.
    - **Patrones Observados:** En las mediciones válidas, la media de frecuencia cardíaca se ubicó en **75.5 BPM** y la saturación de oxígeno en **97.7%**. Se registraron $73$ mediciones con $BPM > 100$ (asociadas a actividad física reciente o estrés) y $41$ con $SpO_2 < 95\%$.

    ---

    > ⚠️ **Consideración Metodológica Importante**
    > 
    > Las mediciones de $BPM$ y $SpO_2$ obtenidas a través del sensor **MAX30102** en este entorno académico tienen un propósito educativo y experimental. **No constituyen un diagnóstico médico ni una evaluación clínica validada.** Factores como la presión sobre el sensor, el movimiento periférico o la temperatura del dedo pueden afectar la precisión de la lectura.
    """)

# --- PESTAÑA 4: REGISTRO DE DATOS ---
with tab4:
    st.subheader("📄 Registros de Datos Filtrados")
    st.write(f"Mostrando **{len(df_filtered)}** filas según los filtros seleccionados:")
    st.dataframe(df_filtered, use_container_width=True)
    
    csv = df_filtered.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="📥 Descargar datos filtrados (CSV)",
        data=csv,
        file_name="mediciones_max30102_filtradas.csv",
        mime="text/csv"
    )
