import streamlit as st
import folium
import requests
import json
import time
from datetime import datetime
from streamlit_folium import st_folium

# Configuración de la página
st.set_page_config(
    page_title="SCADA Monitor",
    page_icon="🛢️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# CSS fijo y probado
st.markdown("""
    <style>
    [data-testid="stSidebar"] { display: none; }
    [data-testid="stHeader"] { display: none; }
    .block-container { 
        padding: 0; 
        max-width: 100%; 
        margin: 0; 
    }
    .stApp { background-color: #f8f9fa; }
    
    /* Estadísticas arriba derecha */
    .stats-bar {
        position: fixed;
        top: 10px;
        right: 15px;
        background: rgba(255, 255, 255, 0.92);
        padding: 10px 15px;
        border-radius: 10px;
        z-index: 1000;
        box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        font-family: Arial, sans-serif;
    }
    .stats-grid { display: grid; grid-template-columns: repeat(6, auto); gap: 12px; }
    .stat-value { font-size: 16px; font-weight: bold; color: #2c3e50; }
    .stat-label { font-size: 9px; color: #7f8c8d; }
    
    /* Desplegable con altura fija y scroll */
    div[data-testid="stExpander"] {
        position: fixed !important;
        bottom: 0 !important;
        left: 0 !important;
        right: 0 !important;
        z-index: 999 !important;
        margin: 0 !important;
    }
    .streamlit-expanderHeader {
        background: linear-gradient(135deg, #f39c12, #e67e22) !important;
        color: white !important;
        font-weight: bold !important;
        padding: 12px 20px !important;
        border: 2px solid #f1c40f !important;
    }
    div[data-testid="stExpander"] > div {
        background: white !important;
        max-height: 450px !important;  /* Altura fija con scroll */
        overflow-y: auto !important;
        border-top: 3px solid #3498db !important;
        padding: 12px !important;
    }
    
    /* Estilo de las tarjetas */
    .station-card {
        background: #f8f9fa;
        border-radius: 6px;
        padding: 12px;
        margin: 8px 0;
        border-left: 4px solid #3498db;
    }
    .vars-container { display: grid; grid-template-columns: repeat(4, 1fr); gap: 8px; }
    .var-item { 
        background: #e9ecef; 
        padding: 4px 6px; 
        border-radius: 3px; 
        font-size: 11px; 
    }
    .var-label { color: #6c757d; font-weight: 500; font-size: 10px; }
    .var-value { color: #2c3e50; font-weight: 600; float: right; }
    
    footer, .stDeployButton, .leaflet-control-attribution { display: none !important; }
    </style>
    """, unsafe_allow_html=True)

# Cargar datos SIN cache (actualización en tiempo real)
def cargar_datos():
    try:
        url = "https://raw.githubusercontent.com/AlarmasCiateq/SCADA_T/main/datos_estaciones.json"
        # Forzar actualización con timestamp
        response = requests.get(f"{url}?t={int(time.time()*1000)}", 
                              headers={'Cache-Control': 'no-cache'}, 
                              timeout=5)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        st.error(f"Error: {str(e)[:50]}")
        return None

# Crear icono (mismo ícono, color negro si fuera de línea)
def crear_icono(tipo, estado, en_linea):
    color = 'black' if en_linea == 0 else (
        'green' if (tipo in ['pozo', 'bomba'] and estado == 1) else
        'red' if (tipo in ['pozo', 'bomba'] and estado == 0) else
        'blue' if (tipo == 'tanque' and estado == 1) else
        'gray' if tipo == 'tanque' else
        'purple' if tipo == 'sensor' else
        'orange'
    )
    
    icon_map = {
        'pozo': ('tint', 'fa'),
        'tanque': ('water', 'fa'),
        'bomba': ('cog', 'fa'),
        'sensor': ('microchip', 'fa')
    }
    icon, prefix = icon_map.get(tipo, ('info-sign', 'glyphicon'))
    return folium.Icon(icon=icon, prefix=prefix, color=color, icon_color='white')

# Crear popup
def crear_popup(estacion):
    html = f"<div style='font-family: Arial; padding: 12px; min-width: 280px'><h4 style='margin:0 0 10px 0'>{estacion.get('nombre', '')}</h4><hr>"
    for k, v in estacion.items():
        if k not in ['nombre', 'latitud', 'longitud', 'tipo', 'estado_bomba', 'en_linea']:
            val = f"{v:,.2f}" if isinstance(v, (int, float)) else str(v)
            html += f"<div style='margin:4px 0'><strong>{k}:</strong> {val}</div>"
    html += f"<hr><div style='font-size:11px;color:#999'>{datetime.now().strftime('%H:%M:%S')}</div></div>"
    return folium.Popup(html, max_width=300)

# Crear mapa (solo calcula bounds la primera vez)
def crear_mapa(datos, primera_vez=True):
    if not datos or 'estaciones' not in datos:
        return None, {}
    
    # Calcular bounds solo la primera vez
    if primera_vez:
        bounds = [[e['latitud'], e['longitud']] 
                 for e in datos['estaciones'] 
                 if 'latitud' in e and 'longitud' in e]
        if not bounds:
            return None, {}
        centro = [sum(b[0] for b in bounds)/len(bounds), sum(b[1] for b in bounds)/len(bounds)]
    else:
        # Usar centro de Ciudad de México como fallback
        centro = [19.4326, -99.1332]
    
    mapa = folium.Map(
        location=centro,
        zoom_start=12 if primera_vez else 10,  # Zoom conservador en actualizaciones
        tiles='CartoDB positron',
        control_scale=False,
        prefer_canvas=True
    )
    
    stats = {'total':0, 'pozos_activos':0, 'pozos_inactivos':0, 'tanques':0, 'bombas_activas':0, 'fuera_linea':0}
    
    for e in datos['estaciones']:
        if 'latitud' not in e or 'longitud' not in e:
            continue
            
        stats['total'] += 1
        en_linea = e.get('en_linea', 1)
        tipo = e.get('tipo', 'otro')
        estado = e.get('estado_bomba', e.get('estado', 0))
        
        if en_linea == 0:
            stats['fuera_linea'] += 1
        elif tipo == 'pozo':
            stats['pozos_activos' if estado == 1 else 'pozos_inactivos'] += 1
        elif tipo == 'tanque':
            stats['tanques'] += 1
        elif tipo == 'bomba' and estado == 1:
            stats['bombas_activas'] += 1
        
        folium.Marker(
            location=[e['latitud'], e['longitud']],
            popup=crear_popup(e),
            tooltip=e.get('nombre', ''),
            icon=crear_icono(tipo, estado, en_linea)
        ).add_to(mapa)
    
    # Ajustar bounds SOLO la primera vez
    if primera_vez and bounds:
        mapa.fit_bounds(bounds, padding=(50, 50))
    
    return mapa, stats

# Main app
def main():
    # Estado persistente para primera carga
    if 'primera_carga' not in st.session_state:
        st.session_state.primera_carga = True
    
    datos = cargar_datos()
    if not datos:
        st.warning("Esperando datos...")
        time.sleep(5)
        st.rerun()
        return
    
    # Crear mapa (con ajuste de zoom solo primera vez)
    mapa, stats = crear_mapa(datos, st.session_state.primera_carga)
    st.session_state.primera_carga = False  # Solo primera vez ajusta zoom
    
    # Estadísticas flotantes
    st.markdown(f"""
        <div class="stats-bar">
            <div class="stats-grid">
                <div><div class="stat-value">📡 {stats['total']}</div><div class="stat-label">Total</div></div>
                <div><div class="stat-value" style="color:#27ae60">🟢 {stats['pozos_activos']}</div><div class="stat-label">Activos</div></div>
                <div><div class="stat-value" style="color:#e74c3c">🔴 {stats['pozos_inactivos']}</div><div class="stat-label">Inactivos</div></div>
                <div><div class="stat-value" style="color:#3498db">🔵 {stats['tanques']}</div><div class="stat-label">Tanques</div></div>
                <div><div class="stat-value" style="color:#000">⚫ {stats['fuera_linea']}</div><div class="stat-label">Offline</div></div>
                <div><div class="stat-value">🕐 {datetime.now().strftime('%H:%M')}</div><div class="stat-label">Actualizado</div></div>
            </div>
        </div>
    """, unsafe_allow_html=True)
    
    # Mapa (siempre visible)
    if mapa:
        st_folium(mapa, width=1920, height=1030, key="mapa")
    else:
        st.error("No hay coordenadas válidas")
    
    # Panel de datos con 4 columnas y scroll fijo
    with st.expander("📊 Ver Datos de Estaciones", expanded=False):
        for e in datos['estaciones']:
            nombre = e.get('nombre', 'Sin nombre')
            lat = e.get('latitud', 0)
            lon = e.get('longitud', 0)
            estado = e.get('estado_bomba', e.get('estado', 0))
            en_linea = e.get('en_linea', 1)
            icono = "⚫" if en_linea == 0 else ("🟢" if estado == 1 else "🔴")
            
            # Variables a mostrar
            vars_data = []
            for k, v in e.items():
                if k not in ['nombre', 'latitud', 'longitud', 'tipo', 'estado_bomba', 'en_linea', 'icono']:
                    val = f"{v:,.2f}" if isinstance(v, (int, float)) else str(v)
                    vars_data.append((k, val))
            
            # Tarjeta de estación
            st.markdown(f"""
                <div class="station-card">
                    <div style="display:flex;justify-content:space-between;margin-bottom:8px">
                        <strong>{icono} {nombre}</strong>
                        <span style="font-family:monospace;font-size:12px">{lat:.4f}, {lon:.4f}</span>
                    </div>
                    <div class="vars-container">
            """, unsafe_allow_html=True)
            
            # 4 columnas
            for label, value in vars_data:
                st.markdown(f"""
                    <div class="var-item">
                        <span class="var-label">{label}:</span>
                        <span class="var-value">{value}</span>
                    </div>
                """, unsafe_allow_html=True)
            
            st.markdown("</div></div><hr style='margin:15px 0;border:1px solid #eee'>", unsafe_allow_html=True)
    
    # Actualización automática (sin perder el estado del mapa)
    time.sleep(60)
    st.rerun()

if __name__ == "__main__":
    main()
