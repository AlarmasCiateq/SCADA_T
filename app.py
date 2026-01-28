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

# CSS ultra minimalista
st.markdown("""
    <style>
    /* Eliminar todo */
    [data-testid="stSidebar"] {
        display: none;
    }
    
    [data-testid="stHeader"] {
        display: none;
    }
    
    .block-container {
        padding-top: 0px;
        padding-bottom: 0px;
        padding-left: 0px;
        padding-right: 0px;
        max-width: 100%;
        margin: 0;
    }
    
    /* Fondo del mapa */
    .stApp {
        background-color: #f8f9fa;
        color: #000000;
    }
    
    /* Estadísticas en la parte superior izquierda */
    .stats-bar {
        position: absolute;
        top: 15px;
        left: 15px;
        background: rgba(255, 255, 255, 0.92);
        backdrop-filter: blur(10px);
        padding: 10px 15px;
        border-radius: 10px;
        z-index: 1000;
        box-shadow: 0 2px 15px rgba(0, 0, 0, 0.15);
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }
    
    .stats-grid {
        display: grid;
        grid-template-columns: repeat(5, auto);
        gap: 15px;
        align-items: center;
    }
    
    .stat-item {
        text-align: center;
    }
    
    .stat-value {
        font-size: 18px;
        font-weight: bold;
        color: #2c3e50;
        line-height: 1.2;
    }
    
    .stat-label {
        font-size: 10px;
        color: #7f8c8d;
        margin-top: 2px;
    }
    
    /* Panel de datos inferior */
    .data-panel {
        position: fixed;
        bottom: 0;
        left: 0;
        right: 0;
        background: rgba(255, 255, 255, 0.95);
        backdrop-filter: blur(10px);
        border-top: 2px solid #3498db;
        z-index: 999;
        max-height: 250px;
        overflow-y: auto;
        padding: 10px;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }
    
    .data-panel h3 {
        color: #2c3e50;
        margin: 5px 0;
        font-size: 16px;
        display: flex;
        align-items: center;
        gap: 8px;
    }
    
    .station-row {
        display: flex;
        padding: 8px;
        border-bottom: 1px solid #ecf0f1;
        font-size: 12px;
    }
    
    .station-name {
        font-weight: bold;
        color: #2c3e50;
        min-width: 200px;
        padding-right: 10px;
    }
    
    .station-coords {
        color: #7f8c8d;
        min-width: 150px;
        padding-right: 10px;
    }
    
    .station-vars {
        flex: 1;
        display: flex;
        flex-wrap: wrap;
        gap: 10px;
    }
    
    .var-item {
        background: rgba(236, 240, 241, 0.7);
        padding: 3px 6px;
        border-radius: 4px;
        font-size: 11px;
        min-width: 120px;
    }
    
    .var-label {
        color: #7f8c8d;
        font-weight: 500;
    }
    
    .var-value {
        color: #2c3e50;
        font-weight: 600;
        float: right;
    }
    
    /* Ocultar footer y botones */
    footer {
        display: none !important;
    }
    
    .stDeployButton {
        display: none !important;
    }
    
    /* Ocultar info de Streamlit */
    .leaflet-control-attribution {
        display: none !important;
    }
    
    /* Popup estilo claro */
    .leaflet-popup-content-wrapper {
        background: rgba(255, 255, 255, 0.98);
        border-radius: 8px;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.3);
    }
    
    .leaflet-popup-content {
        color: #2c3e50;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }
    
    /* Scroll suave para el panel */
    ::-webkit-scrollbar {
        width: 6px;
    }
    ::-webkit-scrollbar-track {
        background: #f1f1f1;
    }
    ::-webkit-scrollbar-thumb {
        background: #c0c0c0;
        border-radius: 3px;
    }
    </style>
    """, unsafe_allow_html=True)

# Función para cargar datos desde GitHub
@st.cache_data(ttl=300)
def cargar_datos_github(url_github):
    try:
        headers = {'User-Agent': 'Mozilla/5.0'}
        response = requests.get(url_github, headers=headers, timeout=10)
        response.raise_for_status()
        return response.json()
    except:
        return None

# Función para crear iconos según el estado
def crear_icono(tipo, estado):
    if tipo == "pozo":
        if estado == 1:
            return folium.Icon(icon='tint', prefix='fa', color='green', icon_color='white')
        else:
            return folium.Icon(icon='tint', prefix='fa', color='red', icon_color='white')
    elif tipo == "tanque":
        if estado == 1:
            return folium.Icon(icon='water', prefix='fa', color='blue', icon_color='white')
        else:
            return folium.Icon(icon='water', prefix='fa', color='gray', icon_color='white')
    elif tipo == "bomba":
        if estado == 1:
            return folium.Icon(icon='cog', prefix='fa', color='green', icon_color='white')
        else:
            return folium.Icon(icon='cog', prefix='fa', color='red', icon_color='white')
    elif tipo == "sensor":
        return folium.Icon(icon='microchip', prefix='fa', color='purple', icon_color='white')
    else:
        return folium.Icon(icon='info-sign', prefix='glyphicon', color='orange')

# Función para crear popup
def crear_popup(estacion):
    popup_html = f"""
    <div style="font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; 
                padding: 15px; min-width: 320px; background: rgba(255, 255, 255, 0.98); 
                color: #2c3e50; border-radius: 8px;">
        <h3 style="color: #2c3e50; margin-top: 0; font-size: 18px; margin-bottom: 12px;">
            📍 {estacion.get('nombre', 'Estación')}
        </h3>
        <hr style="border: 1px solid #ecf0f1; margin: 10px 0;">
    """
    
    for key, value in estacion.items():
        if key not in ['nombre', 'latitud', 'longitud', 'tipo', 'estado', 'estado_bomba', 'icono']:
            if isinstance(value, (int, float)):
                formatted_value = f"{value:,.2f}"
            else:
                formatted_value = str(value)
            
            popup_html += f"""
            <div style="margin: 8px 0; padding: 6px 8px; background: rgba(236, 240, 241, 0.5); 
                        border-radius: 4px; border-left: 3px solid #3498db;">
                <strong style="color: #7f8c8d; font-size: 13px;">{key}:</strong> 
                <span style="color: #2c3e50; font-weight: 600; float: right;">
                    {formatted_value}
                </span>
                <div style="clear: both;"></div>
            </div>
            """
    
    popup_html += f"""
        <hr style="border: 1px solid #ecf0f1; margin: 10px 0;">
        <div style="font-size: 11px; color: #95a5a6; text-align: center; margin-top: 8px;">
            📅 {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
        </div>
    </div>
    """
    
    return folium.Popup(popup_html, max_width=400)

# Función para crear el mapa
def crear_mapa(datos):
    if not datos or 'estaciones' not in datos:
        return None, {}
    
    latitudes = []
    longitudes = []
    bounds = []
    
    for estacion in datos['estaciones']:
        lat = estacion.get('latitud')
        lon = estacion.get('longitud')
        if lat is not None and lon is not None:
            latitudes.append(lat)
            longitudes.append(lon)
            bounds.append([lat, lon])
    
    if not latitudes or not longitudes:
        return None, {}
    
    centro_mapa = [sum(latitudes)/len(latitudes), sum(longitudes)/len(longitudes)]
    
    # Mapa con estilo claro minimalista
    mapa = folium.Map(
        location=centro_mapa,
        zoom_start=12,
        tiles='CartoDB positron',
        control_scale=False,
        prefer_canvas=True,
        zoom_control=True,
        scrollWheelZoom=True,
        dragging=True
    )
    
    stats = {
        'total': 0,
        'pozos_activos': 0,
        'pozos_inactivos': 0,
        'tanques': 0,
        'bombas_activas': 0
    }
    
    # Marcadores individuales SIN cluster
    for estacion in datos['estaciones']:
        try:
            nombre = estacion.get('nombre', 'Estación')
            lat = estacion.get('latitud')
            lon = estacion.get('longitud')
            tipo = estacion.get('tipo', 'otro')
            estado = estacion.get('estado_bomba', estacion.get('estado', 0))
            
            if lat is None or lon is None:
                continue
            
            stats['total'] += 1
            
            if tipo == 'pozo':
                if estado == 1:
                    stats['pozos_activos'] += 1
                else:
                    stats['pozos_inactivos'] += 1
            elif tipo == 'tanque':
                stats['tanques'] += 1
            elif tipo == 'bomba':
                if estado == 1:
                    stats['bombas_activas'] += 1
            
            icono = crear_icono(tipo, estado)
            popup = crear_popup(estacion)
            
            folium.Marker(
                location=[lat, lon],
                popup=popup,
                tooltip=f"📍 {nombre}",
                icon=icono
            ).add_to(mapa)
            
        except:
            continue
    
    # Ajustar zoom automáticamente para todas las estaciones
    if bounds:
        mapa.fit_bounds(bounds, padding=(50, 50))
    
    return mapa, stats

# Interfaz principal
def main():
    # URL del repositorio
    URL_GITHUB = "https://raw.githubusercontent.com/AlarmasCiateq/SCADA_T/main/datos_estaciones.json"
    
    datos = cargar_datos_github(URL_GITHUB)
    
    if datos:
        mapa, stats = crear_mapa(datos)
        
        if mapa:
            # Mostrar mapa ocupando casi toda la pantalla
            st_folium(
                mapa, 
                width=1920,
                height=830,  # Dejamos espacio para el panel inferior
                returned_objects=[],
                key="mapa_scada"
            )
            
            # Estadísticas flotando en esquina superior izquierda
            st.markdown(f"""
                <div class="stats-bar">
                    <div class="stats-grid">
                        <div class="stat-item">
                            <div class="stat-value">📡 {stats['total']}</div>
                            <div class="stat-label">Estaciones</div>
                        </div>
                        <div class="stat-item">
                            <div class="stat-value" style="color: #27ae60;">🟢 {stats['pozos_activos']}</div>
                            <div class="stat-label">Activos</div>
                        </div>
                        <div class="stat-item">
                            <div class="stat-value" style="color: #e74c3c;">🔴 {stats['pozos_inactivos']}</div>
                            <div class="stat-label">Inactivos</div>
                        </div>
                        <div class="stat-item">
                            <div class="stat-value" style="color: #3498db;">🔵 {stats['tanques']}</div>
                            <div class="stat-label">Tanques</div>
                        </div>
                        <div class="stat-item">
                            <div class="stat-value">🕐 {datetime.now().strftime('%H:%M:%S')}</div>
                            <div class="stat-label">Actualizado</div>
                        </div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
            
            # Panel de datos en la parte inferior
            st.markdown('<div class="data-panel">', unsafe_allow_html=True)
            st.markdown("### 📊 Variables de Estaciones")
            
            for idx, estacion in enumerate(datos['estaciones'], 1):
                nombre = estacion.get('nombre', f'Estación {idx}')
                lat = estacion.get('latitud', 'N/A')
                lon = estacion.get('longitud', 'N/A')
                estado = estacion.get('estado_bomba', estacion.get('estado', 0))
                estado_icon = "🟢" if estado == 1 else "🔴"
                
                st.markdown(f'<div class="station-row">', unsafe_allow_html=True)
                st.markdown(f'<div class="station-name">{estado_icon} {nombre}</div>', unsafe_allow_html=True)
                st.markdown(f'<div class="station-coords">📍 {lat:.5f}, {lon:.5f}</div>', unsafe_allow_html=True)
                
                # Variables
                st.markdown('<div class="station-vars">', unsafe_allow_html=True)
                for key, value in estacion.items():
                    if key not in ['nombre', 'latitud', 'longitud', 'tipo', 'estado', 'estado_bomba', 'icono']:
                        if isinstance(value, (int, float)):
                            formatted_value = f"{value:,.2f}"
                        else:
                            formatted_value = str(value)
                        st.markdown(f'<div class="var-item"><span class="var-label">{key}:</span> <span class="var-value">{formatted_value}</span></div>', unsafe_allow_html=True)
                st.markdown('</div>', unsafe_allow_html=True)
                st.markdown('</div>', unsafe_allow_html=True)
            
            st.markdown('</div>', unsafe_allow_html=True)
        
        # Auto-actualización silenciosa
        time.sleep(300)
        st.cache_data.clear()
        st.rerun()
    else:
        # Pantalla de carga
        st.markdown("""
            <div style="position: fixed; top: 0; left: 0; right: 0; bottom: 0; 
                        background: linear-gradient(135deg, #ecf0f1 0%, #bdc3c7 100%); 
                        display: flex; flex-direction: column; justify-content: center; 
                        align-items: center; z-index: 9999;">
                <div style="text-align: center; padding: 40px; background: rgba(255, 255, 255, 0.9); 
                            border-radius: 20px; box-shadow: 0 10px 40px rgba(0, 0, 0, 0.2);">
                    <h1 style="color: #2c3e50; font-size: 48px; margin-bottom: 20px;">🛢️ SCADA Monitor</h1>
                    <p style="color: #7f8c8d; font-size: 18px; margin-bottom: 30px;">
                        Cargando datos del sistema...
                    </p>
                    <div style="font-size: 14px; color: #95a5a6;">
                        ⏳ Esperando actualización desde SCADA
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        time.sleep(10)
        st.cache_data.clear()
        st.rerun()

if __name__ == "__main__":
    main()
