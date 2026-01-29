import streamlit as st
import folium
import requests
import json
import time
from datetime import datetime
from streamlit_folium import st_folium
import hashlib

# Configuración de la página
st.set_page_config(
    page_title="SCADA Monitor",
    page_icon="🛢️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# CSS y JavaScript para panel personalizado
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
    
    /* Estadísticas flotantes en la parte superior derecha */
    .stats-bar {
        position: fixed;
        top: 10px;
        right: 15px;
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
        grid-template-columns: repeat(6, auto);
        gap: 12px;
        align-items: center;
    }
    
    .stat-item {
        text-align: center;
    }
    
    .stat-value {
        font-size: 16px;
        font-weight: bold;
        color: #2c3e50;
        line-height: 1.2;
    }
    
    .stat-label {
        font-size: 9px;
        color: #7f8c8d;
        margin-top: 1px;
    }
    
    /* Panel de datos personalizado - NO USAR st.expander */
    #data-panel {
        position: fixed;
        bottom: 0;
        left: 0;
        right: 0;
        background: white;
        border-top: 3px solid #3498db;
        z-index: 1001;
        box-shadow: 0 -4px 20px rgba(0, 0, 0, 0.15);
        transition: all 0.3s ease;
        max-height: 50px;
        overflow: hidden;
    }
    
    #data-panel-header {
        background: linear-gradient(135deg, #f39c12 0%, #e67e22 100%);
        color: white;
        padding: 12px 20px;
        font-weight: bold;
        font-size: 16px;
        cursor: pointer;
        display: flex;
        justify-content: space-between;
        align-items: center;
        border: 2px solid #f1c40f;
    }
    
    #data-panel-content {
        padding: 12px;
        max-height: 450px;
        overflow-y: auto;
    }
    
    /* Contenido del panel */
    .station-card {
        background: #f8f9fa;
        border-radius: 6px;
        padding: 12px;
        margin: 10px 0;
        border-left: 4px solid #3498db;
        box-shadow: 0 1px 4px rgba(0, 0, 0, 0.05);
    }
    
    .station-header {
        display: flex;
        align-items: center;
        gap: 10px;
        margin-bottom: 10px;
        padding-bottom: 8px;
        border-bottom: 1px solid #e9ecef;
    }
    
    .station-name {
        font-weight: bold;
        color: #2c3e50;
        font-size: 15px;
    }
    
    .station-coords {
        color: #6c757d;
        font-size: 12px;
        margin-left: auto;
        font-family: monospace;
    }
    
    /* Columnas para variables */
    .vars-container {
        display: grid;
        grid-template-columns: repeat(4, 1fr);
        gap: 10px;
    }
    
    .var-item {
        background: #e9ecef;
        padding: 5px 8px;
        border-radius: 4px;
        font-size: 12px;
    }
    
    .var-label {
        color: #6c757d;
        font-weight: 500;
        font-size: 11px;
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
    
    /* Ocultar info de Streamlit y Folium */
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
    
    /* Scroll suave */
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
    
    <script>
    // JavaScript para controlar el panel de datos
    function togglePanel() {
        const panel = document.getElementById('data-panel');
        if (panel.style.maxHeight === '500px' || panel.style.maxHeight === '') {
            panel.style.maxHeight = '50px';
        } else {
            panel.style.maxHeight = '500px';
        }
    }
    
    // Inicializar panel cerrado
    document.addEventListener('DOMContentLoaded', function() {
        const panel = document.getElementById('data-panel');
        if (panel) {
            panel.style.maxHeight = '50px';
        }
    });
    </script>
    """, unsafe_allow_html=True)

# Función para cargar datos desde GitHub - SIN CACHE
def cargar_datos_github(url_github):
    try:
        timestamp = int(time.time() * 1000)
        url_con_timestamp = f"{url_github}?t={timestamp}"
        
        headers = {
            'User-Agent': 'Mozilla/5.0',
            'Cache-Control': 'no-cache, no-store, must-revalidate',
            'Pragma': 'no-cache',
            'Expires': '0'
        }
        
        response = requests.get(url_con_timestamp, headers=headers, timeout=10)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        print(f"Error al cargar datos: {e}")
        return None

# Función para crear iconos según el estado y conexión
def crear_icono(tipo, estado, en_linea):
    # Determinar color
    if en_linea == 0:
        color = 'black'  # Solo color negro, mismo ícono
    elif tipo == "pozo":
        color = 'green' if estado == 1 else 'red'
    elif tipo == "tanque":
        color = 'blue' if estado == 1 else 'gray'
    elif tipo == "bomba":
        color = 'green' if estado == 1 else 'red'
    elif tipo == "sensor":
        color = 'purple'
    else:
        color = 'orange'
    
    # Determinar ícono según tipo (siempre el mismo, solo cambia color)
    if tipo == "pozo":
        return folium.Icon(icon='tint', prefix='fa', color=color, icon_color='white')
    elif tipo == "tanque":
        return folium.Icon(icon='water', prefix='fa', color=color, icon_color='white')
    elif tipo == "bomba":
        return folium.Icon(icon='cog', prefix='fa', color=color, icon_color='white')
    elif tipo == "sensor":
        return folium.Icon(icon='microchip', prefix='fa', color=color, icon_color='white')
    else:
        return folium.Icon(icon='info-sign', prefix='glyphicon', color=color)

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
        if key not in ['nombre', 'latitud', 'longitud', 'tipo', 'estado', 'estado_bomba', 'icono', 'en_linea']:
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

# Función para crear el mapa (solo primera vez)
def crear_mapa_inicial(datos):
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
        'bombas_activas': 0,
        'fuera_linea': 0
    }
    
    # Marcadores individuales SIN cluster
    for estacion in datos['estaciones']:
        try:
            nombre = estacion.get('nombre', 'Estación')
            lat = estacion.get('latitud')
            lon = estacion.get('longitud')
            tipo = estacion.get('tipo', 'otro')
            estado = estacion.get('estado_bomba', estacion.get('estado', 0))
            en_linea = estacion.get('en_linea', 1)
            
            if lat is None or lon is None:
                continue
            
            stats['total'] += 1
            
            if en_linea == 0:
                stats['fuera_linea'] += 1
            
            if tipo == 'pozo':
                if estado == 1 and en_linea == 1:
                    stats['pozos_activos'] += 1
                elif en_linea == 1:
                    stats['pozos_inactivos'] += 1
            elif tipo == 'tanque':
                stats['tanques'] += 1
            elif tipo == 'bomba':
                if estado == 1 and en_linea == 1:
                    stats['bombas_activas'] += 1
            
            icono = crear_icono(tipo, estado, en_linea)
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

# Función para generar HTML del panel de datos
def generar_html_panel(datos):
    html = """
    <div id="data-panel">
        <div id="data-panel-header" onclick="togglePanel()">
            <span>📊 Ver Datos de Estaciones</span>
            <span id="panel-toggle-icon">▼</span>
        </div>
        <div id="data-panel-content">
    """
    
    for idx, estacion in enumerate(datos['estaciones'], 1):
        nombre = estacion.get('nombre', f'Estación {idx}')
        lat = estacion.get('latitud', 'N/A')
        lon = estacion.get('longitud', 'N/A')
        estado = estacion.get('estado_bomba', estacion.get('estado', 0))
        en_linea = estacion.get('en_linea', 1)
        estado_icon = "🟢" if estado == 1 else "🔴"
        if en_linea == 0:
            estado_icon = "⚫"
        
        # Crear lista de variables
        variables = []
        for key, value in estacion.items():
            if key not in ['nombre', 'latitud', 'longitud', 'tipo', 'estado', 'estado_bomba', 'icono', 'en_linea']:
                if isinstance(value, (int, float)):
                    formatted_value = f"{value:,.2f}"
                else:
                    formatted_value = str(value)
                variables.append({'label': key, 'value': formatted_value})
        
        # Tarjeta de estación
        html += f"""
            <div class="station-card">
                <div class="station-header">
                    <span class="station-name">{estado_icon} {nombre}</span>
                    <span class="station-coords">{lat:.5f}, {lon:.5f}</span>
                </div>
                <div class="vars-container">
        """
        
        # Variables en 4 columnas
        for i, var in enumerate(variables):
            html += f"""
                <div class="var-item">
                    <span class="var-label">{var['label']}:</span>
                    <span class="var-value">{var['value']}</span>
                </div>
            """
        
        html += """
                </div>
            </div>
            <hr style='margin: 15px 0; border: 1px solid #dee2e6;'>
        """
    
    html += """
        </div>
    </div>
    <script>
    function togglePanel() {
        const panel = document.getElementById('data-panel');
        const icon = document.getElementById('panel-toggle-icon');
        if (panel.style.maxHeight === '50px') {
            panel.style.maxHeight = '500px';
            icon.textContent = '▲';
        } else {
            panel.style.maxHeight = '50px';
            icon.textContent = '▼';
        }
    }
    </script>
    """
    
    return html

# Interfaz principal
def main():
    # URL del repositorio
    URL_GITHUB = "https://raw.githubusercontent.com/AlarmasCiateq/SCADA_T/main/datos_estaciones.json"
    
    # Inicializar session_state
    if 'mapa_creado' not in st.session_state:
        st.session_state.mapa_creado = False
        st.session_state.datos_hash = None
        st.session_state.ultima_actualizacion = None
    
    # Cargar datos
    datos = cargar_datos_github(URL_GITHUB)
    
    if datos:
        # Calcular hash de los datos para detectar cambios
        datos_str = json.dumps(datos, sort_keys=True)
        datos_hash = hashlib.md5(datos_str.encode()).hexdigest()
        
        # Primera carga: crear mapa completo
        if not st.session_state.mapa_creado:
            mapa, stats = crear_mapa_inicial(datos)
            st.session_state.mapa_creado = True
            st.session_state.datos_hash = datos_hash
        else:
            # Subsecuentes: solo actualizar panel de datos si hay cambios
            mapa = None
            # Recalcular estadísticas
            stats = {
                'total': 0,
                'pozos_activos': 0,
                'pozos_inactivos': 0,
                'tanques': 0,
                'bombas_activas': 0,
                'fuera_linea': 0
            }
            
            for estacion in datos['estaciones']:
                stats['total'] += 1
                en_linea = estacion.get('en_linea', 1)
                tipo = estacion.get('tipo', 'otro')
                estado = estacion.get('estado_bomba', estacion.get('estado', 0))
                
                if en_linea == 0:
                    stats['fuera_linea'] += 1
                elif tipo == 'pozo':
                    if estado == 1:
                        stats['pozos_activos'] += 1
                    else:
                        stats['pozos_inactivos'] += 1
                elif tipo == 'tanque':
                    stats['tanques'] += 1
                elif tipo == 'bomba' and estado == 1:
                    stats['bombas_activas'] += 1
        
        # Mostrar estadísticas
        st.markdown(f"""
            <div class="stats-bar">
                <div class="stats-grid">
                    <div class="stat-item">
                        <div class="stat-value">📡 {stats['total']}</div>
                        <div class="stat-label">Total</div>
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
                        <div class="stat-value" style="color: #000000;">⚫ {stats['fuera_linea']}</div>
                        <div class="stat-label">Offline</div>
                    </div>
                    <div class="stat-item">
                        <div class="stat-value">🕐 {datetime.now().strftime('%H:%M:%S')}</div>
                        <div class="stat-label">Actualizado</div>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        # Mostrar mapa (solo primera vez)
        if st.session_state.mapa_creado and 'mapa' in locals() and mapa is not None:
            st_folium(
                mapa, 
                width=1920,
                height=1030,
                returned_objects=[],
                key="mapa_scada"
            )
        else:
            # Mantener el espacio del mapa
            st.empty()
        
        # Mostrar panel de datos personalizado
        panel_html = generar_html_panel(datos)
        st.markdown(panel_html, unsafe_allow_html=True)
        
        # Auto-actualización cada 60 segundos
        time.sleep(60)
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
        
        time.sleep(5)
        st.rerun()

if __name__ == "__main__":
    main()
