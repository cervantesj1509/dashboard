import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np

# =========================
# CONFIGURACIÓN GENERAL
# =========================

st.set_page_config(
    page_title="Dashboard Deserción",
    page_icon="📊",
    layout="wide"
)
st.markdown("""
    <style>
        body { 
            color: #202124 !important; 
            background-color: #FFFFFF !important; 
        }
        .main {
            background-color: #F5F7FB !important;
            color: #202124 !important;
        }
        [data-testid="stAppViewContainer"] {
            background-color: #F5F7FB !important;
            color: #202124 !important;
        }
        [data-testid="stSidebar"] {
            background-color: #FFFFFF !important;
        }
        html, body, div, span, p, h1, h2, h3, h4, h5, h6 {
            color: #202124 !important;
        }
    </style>
""", unsafe_allow_html=True)


# ====== ESTILO TIPO LOOKER STUDIO ======
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Google+Sans:wght@400;500;700&display=swap');

    html, body, [class*="css"] {
        font-family: 'Google Sans', sans-serif;
    }

    .main {
        background-color: #F5F7FB;
    }

    .block-container {
        padding-top: 0.5rem;
        padding-bottom: 2rem;
        max-width: 1200px;
    }

    /* Top bar estilo Looker Studio */
    .top-bar {
        background-color: #FFFFFF;
        border-bottom: 1px solid #E0E3EB;
        padding: 0.8rem 1.2rem;
        display: flex;
        align-items: center;
        justify-content: space-between;
        box-shadow: 0 1px 3px rgba(0,0,0,0.06);
        border-radius: 0 0 12px 12px;
        margin-bottom: 1.5rem;
    }

    .top-title {
        font-size: 1.1rem;
        font-weight: 600;
        color: #202124;
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }

    .top-title-icon {
        background-color: #E8F0FE;
        color: #1A73E8;
        width: 28px;
        height: 28px;
        border-radius: 6px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 16px;
    }

    .top-subtitle {
        font-size: 0.78rem;
        color: #5F6368;
    }

    .chip {
        background-color: #E8F0FE;
        color: #1A73E8;
        border-radius: 999px;
        padding: 0.15rem 0.7rem;
        font-size: 0.75rem;
        font-weight: 500;
    }

    /* Cards KPIs */
    .metric-card {
        background-color: #FFFFFF;
        padding: 16px 18px;
        border-radius: 12px;
        box-shadow: 0px 1px 4px rgba(0,0,0,0.08);
        border: 1px solid #E0E3EB;
    }
    .metric-label {
        font-size: 0.75rem;
        text-transform: uppercase;
        letter-spacing: 0.06em;
        color: #5F6368;
        margin-bottom: 0.35rem;
    }
    .metric-value {
        font-size: 1.3rem;
        font-weight: 600;
        color: #202124;
    }
    .metric-footnote {
        font-size: 0.75rem;
        color: #5F6368;
        margin-top: 0.2rem;
    }

    /* Títulos de secciones */
    .section-title {
        font-size: 0.95rem;
        font-weight: 600;
        color: #202124;
        margin: 0.8rem 0 0.2rem 0;
    }
    .section-subtitle {
        font-size: 0.78rem;
        color: #5F6368;
        margin-bottom: 0.4rem;
    }

    /* Sidebar estilo Looker */
    section[data-testid="stSidebar"] {
        background-color: #FFFFFF !important;
        border-right: 1px solid #E0E3EB;
    }
    </style>
""", unsafe_allow_html=True)

# =========================
# CARGA Y TRATAMIENTO DE DATOS
# =========================

@st.cache_data
def load_data():
    df = pd.read_csv("desercion.csv")

    # Normalizar nombres de columnas
    df.columns = [c.strip().replace(" ", "_") for c in df.columns]

    # Convertir Año
    try:
        df["Año"] = pd.to_datetime(df["Año"], errors="coerce").dt.year
    except Exception:
        df["Año"] = pd.to_numeric(df["Año"], errors="coerce")

    # Limpiar Tasa_desercion
    df["Tasa_desercion"] = (
        df["Tasa_desercion"]
        .astype(str)
        .str.replace("%", "", regex=False)
        .str.replace(",", ".", regex=False)
    )
    df["Tasa_desercion"] = pd.to_numeric(df["Tasa_desercion"], errors="coerce")

    # Quitar filas sin datos esenciales
    df = df.dropna(subset=["Año", "Tasa_desercion"])

    return df

df = load_data()

# =========================
# TOP BAR (CINTA SUPERIOR)
# =========================

min_year, max_year = int(df["Año"].min()), int(df["Año"].max())

st.markdown(f"""
<div class="top-bar">
  <div>
    <div class="top-title">
      <div class="top-title-icon">📊</div>
      Dashboard Tasa de Deserción – Colombia
    </div>
    <div class="top-subtitle">
      Integración de múltiples tablas, limpieza de campos de año y normalización de la tasa de deserción.
    </div>
  </div>
  <div>
    <span class="chip">Datos {min_year} – {max_year}</span>
  </div>
</div>
""", unsafe_allow_html=True)

# =========================
# SIDEBAR / FILTROS
# =========================

st.sidebar.markdown("### 🔍 Controles de exploración")

niveles = sorted(df["Nivel_formacion"].dropna().unique())
departamentos = sorted(df["Departamento"].dropna().unique())

nivel_sel = st.sidebar.multiselect(
    "Nivel de formación",
    options=niveles,
    default=niveles,
    help="Selecciona uno o varios niveles para filtrar."
)

depto_sel = st.sidebar.multiselect(
    "Departamento",
    options=departamentos,
    default=departamentos,
    help="Puedes concentrarte en uno o varios departamentos."
)

rango_years = st.sidebar.slider(
    "Rango de años",
    min_value=min_year,
    max_value=max_year,
    value=(min_year, max_year),
    step=1
)

st.sidebar.markdown("---")
st.sidebar.caption(
    "Este dashboard replica la lógica de Looker Studio: filtros a la izquierda, panel central de análisis y tarjetas de indicadores."
)

# Aplicar filtros
mask = (
    df["Nivel_formacion"].isin(nivel_sel) &
    df["Departamento"].isin(depto_sel) &
    df["Año"].between(rango_years[0], rango_years[1])
)
dff = df[mask].copy()

# =========================
# INDICADORES (KPIs)
# =========================

st.markdown('<div class="section-title">Indicadores clave</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="section-subtitle">Resumen general de la tasa de deserción según los filtros aplicados.</div>',
    unsafe_allow_html=True
)

col1, col2, col3 = st.columns(3)

if dff.empty:
    prom = max_v = min_v = np.nan
else:
    prom = dff["Tasa_desercion"].mean()
    max_v = dff["Tasa_desercion"].max()
    min_v = dff["Tasa_desercion"].min()

with col1:
    st.markdown("<div class='metric-card'>", unsafe_allow_html=True)
    st.markdown("<div class='metric-label'>Promedio de deserción</div>", unsafe_allow_html=True)
    if np.isnan(prom):
        st.markdown("<div class='metric-value'>–</div>", unsafe_allow_html=True)
    else:
        st.markdown(f"<div class='metric-value'>{prom:,.2f} %</div>", unsafe_allow_html=True)
    st.markdown("<div class='metric-footnote'>Promedio ponderado de la tasa en el rango seleccionado.</div>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

with col2:
    st.markdown("<div class='metric-card'>", unsafe_allow_html=True)
    st.markdown("<div class='metric-label'>Máxima deserción</div>", unsafe_allow_html=True)
    if np.isnan(max_v):
        st.markdown("<div class='metric-value'>–</div>", unsafe_allow_html=True)
    else:
        st.markdown(f"<div class='metric-value'>{max_v:,.2f} %</div>", unsafe_allow_html=True)
    st.markdown("<div class='metric-footnote'>Valor más alto encontrado en el periodo filtrado.</div>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

with col3:
    st.markdown("<div class='metric-card'>", unsafe_allow_html=True)
    st.markdown("<div class='metric-label'>Mínima deserción</div>", unsafe_allow_html=True)
    if np.isnan(min_v):
        st.markdown("<div class='metric-value'>–</div>", unsafe_allow_html=True)
    else:
        st.markdown(f"<div class='metric-value'>{min_v:,.2f} %</div>", unsafe_allow_html=True)
    st.markdown("<div class='metric-footnote'>Valor más bajo reportado en el periodo filtrado.</div>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

st.markdown("---")

# =========================
# GRÁFICOS
# =========================

if dff.empty:
    st.warning("No hay datos para los filtros seleccionados. Ajusta el nivel, departamento o rango de años.")
else:
    # --- Gráfico línea ---
    st.markdown('<div class="section-title">Evolución de la tasa de deserción</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="section-subtitle">Comportamiento de la tasa de deserción a lo largo del tiempo por departamento.</div>',
        unsafe_allow_html=True
    )

    fig_line = px.line(
        dff.sort_values("Año"),
        x="Año",
        y="Tasa_desercion",
        color="Departamento",
        markers=True,
        title=None
    )
    fig_line.update_layout(
        template="plotly_white",
        margin=dict(l=10, r=10, t=10, b=10),
        legend_title="Departamento",
        xaxis_title="Año",
        yaxis_title="Tasa de deserción (%)"
    )
    st.plotly_chart(fig_line, use_container_width=True)

    # --- Gráfico barras ---
    st.markdown('<div class="section-title">Comparación promedio por departamento</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="section-subtitle">Promedio de la tasa de deserción para cada departamento dentro de los filtros actuales.</div>',
        unsafe_allow_html=True
    )

    df_dept = (
        dff.groupby("Departamento", as_index=False)["Tasa_desercion"]
           .mean()
           .sort_values("Tasa_desercion", ascending=False)
    )

    fig_bar = px.bar(
        df_dept,
        x="Departamento",
        y="Tasa_desercion",
        title=None
    )
    fig_bar.update_layout(
        template="plotly_white",
        margin=dict(l=10, r=10, t=10, b=10),
        xaxis_title="Departamento",
        yaxis_title="Tasa de deserción promedio (%)"
    )
    st.plotly_chart(fig_bar, use_container_width=True)

   

# =========================
# TABLA DETALLE
# =========================

st.markdown('<div class="section-title">Detalle de registros</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="section-subtitle">Vista tabular de los datos filtrados, similar a una tabla de Looker Studio.</div>',
    unsafe_allow_html=True
)

st.dataframe(
    dff.sort_values(["Departamento", "Año"]).reset_index(drop=True),
    use_container_width=True,
    height=320
)

st.caption(
    """
    **Notas de tratamiento de datos**  
    - Los datos originales provenían de **diferentes tablas** y se unificaron en una sola estructura.  
    - El campo **Año** se limpió y convirtió a valor numérico para facilitar la comparación temporal.  
    - La **Tasa_desercion** se normalizó eliminando símbolos de `%` y corrigiendo el uso de comas y puntos,
      de modo que pueda interpretarse correctamente como porcentaje.
    """
)
