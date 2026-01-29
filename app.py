import streamlit as st
import folium
import requests
import json
from datetime import datetime
from streamlit_folium import st_folium

# Configuración minimalista
st.set_page_config(
    page_title="SCADA Monitor",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# CSS limpio y funcional
st.markdown("""
    <style>
    [data-testid="stSidebar"] { display: none; }
    [data-testid="stHeader"] { display: none; }
    .block-container { padding: 0; max-width: 100%; margin: 0; }
    .stApp { background-color: #f8f9fa; }
    
    /* Estadísticas arriba derecha */
    .stats-bar {
        position: fixed;
        top: 10px;
        right: 15px;
        background: rgba(255, 255, 255, 0.95);
        padding: 8px 15px;
        border-radius: 8px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.15);
        z-index: 1000;
        font-family: Arial, sans-serif;
        font-size: 13px;
    }
    .stats-grid { display: grid; grid-template-columns: repeat(6, auto); gap: 10px; }
    .stat-value { font-weight: bold; color: #2c3e50; }
    .stat-label { font-size: 9px; color: #7f8c8d; }
    
    footer, .stDeployButton, .leaflet-control-attribution { display: none !important; }
    </style>
    """, unsafe_allow_html=True)

# Cargar datos (sin cache para actualización manual)
def cargar_datos():
    try:
        url = "https://raw.githubusercontent.com/AlarmasCiateq/SCADA_T/main/datos_estaciones.json"
        response = requests.get(f"{url}?t={int(datetime.now().timestamp()*1000)}", timeout=5)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        st.error(f"Error al cargar datos: {str(e)[:50]}")
        return None

# Crear icono (mismo ícono, color según estado)
def crear_icono(tipo, estado, en_linea):
    # Color: negro si fuera de línea, sino según estado
    color = 'black' if en_linea == 0 else (
        'green' if (tipo in ['pozo', 'bomba'] and estado == 1) else
        'red' if (tipo in ['pozo', 'bomba'] and estado == 0) else
        'blue' if (tipo == 'tanque' and estado == 1) else
        'gray' if tipo == 'tanque' else
        'purple' if tipo == 'sensor' else
        'orange'
    )
    
    # Ícono según tipo (siempre el mismo)
    iconos = {
        'pozo': ('tint', 'fa'),
        'tanque': ('water', 'fa'),
        'bomba': ('cog', 'fa'),
        'sensor': ('microchip', 'fa')
    }
    icon, prefix = iconos.get(tipo, ('info-sign', 'glyphicon'))
    return folium.Icon(icon=icon, prefix=prefix, color=color, icon_color='white')

# Crear popup con datos
def crear_popup(estacion):
    html = f"<div style='font-family: Arial; padding: 12px; min-width: 280px'><h4 style='margin:0 0 8px 0; color:#2c3e50'>{estacion.get('nombre', '')}</h4><hr style='margin:8px 0'>"
    for k, v in estacion.items():
        if k not in ['nombre', 'latitud', 'longitud', 'tipo', 'estado_bomba', 'en_linea', 'icono']:
            val = f"{v:,.2f}" if isinstance(v, (float, int)) else str(v)
            html += f"<div style='margin:5px 0; padding:3px 0'><span style='color:#7f8c8d; font-size:12px'>{k}:</span> <span style='float:right; font-weight:bold'>{val}</span><div style='clear:both'></div></div>"
    html += f"<hr style='margin:8px 0'><div style='font-size:11px; color:#95a5a6; text-align:center'>{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</div></div>"
    return folium.Popup(html, max_width=320)

# Crear mapa con zoom óptimo
def crear_mapa(datos):
    if not datos or 'estaciones' not in datos:
        return None, {}
    
    # Calcular bounds para ajustar zoom
    bounds = []
    for e in datos['estaciones']:
        if 'latitud' in e and 'longitud' in e:
            bounds.append([e['latitud'], e['longitud']])
    
    if not bounds:
        return None, {}
    
    # Centro y mapa
    centro = [sum(b[0] for b in bounds)/len(bounds), sum(b[1] for b in bounds)/len(bounds)]
    mapa = folium.Map(
        location=centro,
        zoom_start=10,
        tiles='CartoDB positron',  # Mapa claro con calles sutiles
        control_scale=False,
        prefer_canvas=True
    )
    
    # Estadísticas
    stats = {'total':0, 'activos':0, 'inactivos':0, 'tanques':0, 'offline':0}
    
    # Marcadores
    for e in datos['estaciones']:
        if 'latitud' not in e or 'longitud' not in e:
            continue
        
        stats['total'] += 1
        en_linea = e.get('en_linea', 1)
        tipo = e.get('tipo', 'otro')
        estado = e.get('estado_bomba', e.get('estado', 0))
        
        if en_linea == 0:
            stats['offline'] += 1
        elif tipo == 'pozo':
            stats['activos' if estado == 1 else 'inactivos'] += 1
        elif tipo == 'tanque':
            stats['tanques'] += 1
        
        folium.Marker(
            location=[e['latitud'], e['longitud']],
            popup=crear_popup(e),
            tooltip=e.get('nombre', ''),
            icon=crear_icono(tipo, estado, en_linea)
        ).add_to(mapa)
    
    # Ajustar zoom para mostrar todas las estaciones
    mapa.fit_bounds(bounds, padding=(40, 40))
    
    return mapa, stats

# Interfaz principal
def main():
    # Botón de actualización manual (arriba izquierda)
    col1, col2 = st.columns([1, 20])
    with col1:
        if st.button("🔄", key="btn_actualizar", help="Actualizar datos"):
            st.cache_data.clear()
            st.rerun()
    
    # Cargar datos
    datos = cargar_datos()
    if not datos:
        st.warning("Esperando datos del sistema SCADA...")
        return
    
    # Crear mapa
    mapa, stats = crear_mapa(datos)
    if not mapa:
        st.error("No hay coordenadas válidas en los datos")
        return
    
    # Estadísticas flotantes
    st.markdown(f"""
        <div class="stats-bar">
            <div class="stats-grid">
                <div><div class="stat-value">📡 {stats['total']}</div><div class="stat-label">Total</div></div>
                <div><div class="stat-value" style="color:#27ae60">🟢 {stats['activos']}</div><div class="stat-label">Activos</div></div>
                <div><div class="stat-value" style="color:#e74c3c">🔴 {stats['inactivos']}</div><div class="stat-label">Inactivos</div></div>
                <div><div class="stat-value" style="color:#3498db">🔵 {stats['tanques']}</div><div class="stat-label">Tanques</div></div>
                <div><div class="stat-value" style="color:#000">⚫ {stats['offline']}</div><div class="stat-label">Offline</div></div>
                <div><div class="stat-value">🕐 {datetime.now().strftime('%H:%M')}</div><div class="stat-label">Actualizado</div></div>
            </div>
        </div>
    """, unsafe_allow_html=True)
    
    # Mostrar mapa (FullHD)
    st_folium(
        mapa,
        width=1920,
        height=1080,
        key="mapa_scada"
    )

if __name__ == "__main__":
    main()
