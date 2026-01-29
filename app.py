import streamlit as st
import requests
import json
from datetime import datetime
from streamlit_autorefresh import st_autorefresh

# Configuración minimalista
st.set_page_config(
    page_title="SCADA Monitor",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# CSS para ocultar elementos de Streamlit
st.markdown("""
    <style>
    [data-testid="stSidebar"] { display: none; }
    [data-testid="stHeader"] { display: none; }
    .block-container { padding: 0; max-width: 100%; margin: 0; }
    .stApp { background-color: #0e1117; }
    footer, .stDeployButton { display: none !important; }
    </style>
    """, unsafe_allow_html=True)

# ==============================
# CARGAR DATOS DESDE GITHUB (Python - SIN CORS)
# ==============================
def cargar_datos_github():
    try:
        # URL CORRECTA sin espacios
        url = "https://raw.githubusercontent.com/AlarmasCiateq/SCADA_T/main/datos_estaciones.json"
        
        # Forzar carga fresca (sin cache)
        response = requests.get(
            url + f"?t={int(datetime.now().timestamp() * 1000)}",
            timeout=10,
            headers={'Cache-Control': 'no-cache'}
        )
        response.raise_for_status()
        return response.json()
    except Exception as e:
        st.error(f"Error al cargar datos: {str(e)[:50]}")
        return None

# ==============================
# AUTO-REFRESH (5 segundos para pruebas)
# ==============================
# ⚠️ CAMBIA A 300000 PARA PRODUCCIÓN (5 minutos)
st_autorefresh(interval=5000, key="auto_refresh")

# ==============================
# CARGAR DATOS
# ==============================
datos = cargar_datos_github()
if not datos:
    st.error("⚠️ No se pudieron cargar los datos de GitHub")
    st.stop()

# ==============================
# GENERAR HTML+JS CON DATOS EMBEBIDOS
# ==============================
# Convertir datos a JSON string para embeber en JavaScript
datos_json = json.dumps(datos)

html_completo = f"""
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>SCADA Monitor</title>
    <link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css" />
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{ font-family: Arial, sans-serif; background: #0e1117; overflow: hidden; }}
        #map {{ position: absolute; top: 0; left: 0; width: 100%; height: 100%; z-index: 1; }}
        
        /* Estadísticas flotantes */
        #stats-bar {{
            position: fixed;
            top: 10px;
            right: 15px;
            background: rgba(255, 255, 255, 0.95);
            padding: 8px 15px;
            border-radius: 8px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.15);
            z-index: 1000;
            display: grid;
            grid-template-columns: repeat(6, auto);
            gap: 12px;
            align-items: center;
            font-family: Arial, sans-serif;
            font-size: 13px;
        }}
        .stat-value {{ font-weight: bold; color: #2c3e50; font-size: 16px; }}
        .stat-label {{ font-size: 9px; color: #7f8c8d; }}
        .custom-popup {{ font-family: Arial; padding: 12px; min-width: 280px; background: white; border-radius: 6px; }}
        .custom-popup h4 {{ margin: 0 0 10px 0; color: #2c3e50; font-size: 16px; }}
        .custom-popup hr {{ margin: 8px 0; border-color: #ecf0f1; }}
        .custom-popup .var-row {{ margin: 6px 0; padding: 4px 0; display: flex; justify-content: space-between; font-size: 13px; }}
        .custom-popup .var-label {{ color: #7f8c8d; }}
        .custom-popup .var-value {{ font-weight: bold; color: #2c3e50; }}
        .custom-popup .timestamp {{ font-size: 11px; color: #95a5a6; text-align: center; margin-top: 8px; }}
    </style>
</head>
<body>
    <div id="map"></div>
    <div id="stats-bar">
        <div><div class="stat-value">📡 <span id="stat-total">0</span></div><div class="stat-label">Total</div></div>
        <div><div class="stat-value" style="color:#27ae60">🟢 <span id="stat-activos">0</span></div><div class="stat-label">Activos</div></div>
        <div><div class="stat-value" style="color:#e74c3c">🔴 <span id="stat-inactivos">0</span></div><div class="stat-label">Inactivos</div></div>
        <div><div class="stat-value" style="color:#3498db">🔵 <span id="stat-tanques">0</span></div><div class="stat-label">Tanques</div></div>
        <div><div class="stat-value" style="color:#000">⚫ <span id="stat-offline">0</span></div><div class="stat-label">Offline</div></div>
        <div><div class="stat-value">🕐 <span id="stat-time">--:--</span></div><div class="stat-label">Actualizado</div></div>
    </div>

    <script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"></script>
    <script>
        // ════════════════════════════════════════════════════════════════
        // DATOS CARGADOS DESDE PYTHON (embebidos en el HTML)
        // ════════════════════════════════════════════════════════════════
        const DATOS_INICIALES = {datos_json};
        
        // ════════════════════════════════════════════════════════════════
        
        let map = null;
        let markers = new Map(); // id -> marker
        let primeraCarga = true;
        
        // Inicializar mapa
        function initMap() {{
            map = L.map('map', {{
                zoomControl: true,
                scrollWheelZoom: true,
                dragging: true
            }});
            
            // Mapa claro con calles sutiles
            L.tileLayer('https://{{s}}.basemaps.cartocdn.com/light_all/{{z}}/{{x}}/{{y}}{{r}}.png', {{
                attribution: '',
                subdomains: 'abcd',
                maxZoom: 19
            }}).addTo(map);
            
            // Cargar datos iniciales
            actualizarMapa(DATOS_INICIALES);
            actualizarEstadisticas(DATOS_INICIALES);
            
            // Actualizar timestamp
            document.getElementById('stat-time').textContent = new Date().toLocaleTimeString('es-ES', {{ 
                hour: '2-digit', 
                minute: '2-digit' 
            }});
        }}
        
        // Actualizar mapa (solo valores y colores, no posiciones)
        function actualizarMapa(datos) {{
            if (!datos || !datos.estaciones) return;
            
            const nuevasBounds = [];
            
            datos.estaciones.forEach(estacion => {{
                if (!estacion.latitud || !estacion.longitud) return;
                
                const id = estacion.nombre || `${{estacion.latitud}},${{estacion.longitud}}`;
                const lat = parseFloat(estacion.latitud);
                const lng = parseFloat(estacion.longitud);
                
                nuevasBounds.push([lat, lng]);
                
                // Si ya existe el marcador, actualizar popup y color
                if (markers.has(id)) {{
                    const marker = markers.get(id);
                    
                    // Actualizar popup
                    const popupContent = crearPopupContent(estacion);
                    marker.setPopupContent(popupContent);
                    
                    // Actualizar color si cambió estado
                    const nuevoIcono = crearIcono(estacion.tipo, estacion.estado_bomba, estacion.en_linea);
                    marker.setIcon(nuevoIcono);
                    
                }} else {{
                    // Crear nuevo marcador
                    const icono = crearIcono(estacion.tipo, estacion.estado_bomba, estacion.en_linea);
                    const popupContent = crearPopupContent(estacion);
                    
                    const marker = L.marker([lat, lng], {{ icon: icono }})
                        .bindPopup(popupContent, {{ maxWidth: 320 }})
                        .addTo(map);
                    
                    markers.set(id, marker);
                }}
            }});
            
            // Ajustar bounds SOLO en primera carga
            if (primeraCarga && nuevasBounds.length > 0) {{
                const bounds = L.latLngBounds(nuevasBounds);
                map.fitBounds(bounds, {{ padding: [40, 40] }});
                primeraCarga = false;
                console.log('✓ Zoom inicial ajustado');
            }}
        }}
        
        // Crear icono según tipo y estado
        function crearIcono(tipo, estado, enLinea) {{
            // Determinar color
            let color = '#000000'; // negro por defecto (offline)
            if (enLinea !== 0) {{
                if (tipo === 'pozo' || tipo === 'bomba') {{
                    color = estado === 1 ? '#27ae60' : '#e74c3c'; // verde/rojo
                }} else if (tipo === 'tanque') {{
                    color = estado === 1 ? '#3498db' : '#95a5a6'; // azul/gris
                }} else if (tipo === 'sensor') {{
                    color = '#9b59b6'; // morado
                }} else {{
                    color = '#f39c12'; // naranja
                }}
            }}
            
            // Determinar ícono (siempre el mismo según tipo)
            let iconClass = 'fa-tint'; // pozo por defecto
            if (tipo === 'tanque') iconClass = 'fa-water';
            else if (tipo === 'bomba') iconClass = 'fa-cog';
            else if (tipo === 'sensor') iconClass = 'fa-microchip';
            
            return L.divIcon({{
                html: `<div style="
                    background: ${{color}};
                    width: 32px;
                    height: 32px;
                    border-radius: 50%;
                    display: flex;
                    align-items: center;
                    justify-content: center;
                    box-shadow: 0 2px 6px rgba(0,0,0,0.4);
                ">
                    <i class="fa ${{iconClass}}" style="color: white; font-size: 16px;"></i>
                </div>`,
                className: '',
                iconSize: [32, 32],
                iconAnchor: [16, 16],
                popupAnchor: [0, -16]
            }});
        }}
        
        // Crear contenido del popup
        function crearPopupContent(estacion) {{
            let html = `<div class="custom-popup"><h4>${{estacion.nombre || 'Estación'}}</h4><hr>`;
            
            for (const key in estacion) {{
                if (!['nombre', 'latitud', 'longitud', 'tipo', 'estado_bomba', 'en_linea', 'icono'].includes(key)) {{
                    const value = typeof estacion[key] === 'number' 
                        ? estacion[key].toLocaleString('es-ES', {{ minimumFractionDigits: 2, maximumFractionDigits: 2 }})
                        : estacion[key];
                    
                    html += `<div class="var-row"><span class="var-label">${{key}}:</span><span class="var-value">${{value}}</span></div>`;
                }}
            }}
            
            html += `<hr><div class="timestamp">📅 ${{new Date().toLocaleString('es-ES')}}</div></div>`;
            return html;
        }}
        
        // Actualizar estadísticas
        function actualizarEstadisticas(datos) {{
            if (!datos || !datos.estaciones) return;
            
            const stats = {{ total:0, activos:0, inactivos:0, tanques:0, offline:0 }};
            
            datos.estaciones.forEach(estacion => {{
                stats.total++;
                const enLinea = estacion.en_linea || 1;
                const tipo = estacion.tipo || 'otro';
                const estado = estacion.estado_bomba || estacion.estado || 0;
                
                if (enLinea === 0) stats.offline++;
                else if (tipo === 'pozo') {{
                    if (estado === 1) stats.activos++;
                    else stats.inactivos++;
                }} else if (tipo === 'tanque') stats.tanques++;
            }});
            
            document.getElementById('stat-total').textContent = stats.total;
            document.getElementById('stat-activos').textContent = stats.activos;
            document.getElementById('stat-inactivos').textContent = stats.inactivos;
            document.getElementById('stat-tanques').textContent = stats.tanques;
            document.getElementById('stat-offline').textContent = stats.offline;
        }}
        
        // Iniciar cuando el DOM esté listo
        document.addEventListener('DOMContentLoaded', initMap);
    </script>
    
    <!-- Font Awesome para íconos -->
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
</body>
</html>
"""

# Mostrar el HTML+JS en Streamlit (se ejecutará en el navegador)
st.components.v1.html(
    html_completo,
    width=1920,
    height=1080,
    scrolling=False
)
