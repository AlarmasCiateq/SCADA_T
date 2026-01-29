import streamlit as st

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

# HTML+JS completo con proxy CORS y modo pruebas
html_completo = """
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>SCADA Monitor</title>
    <link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css" />
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { font-family: Arial, sans-serif; background: #0e1117; overflow: hidden; }
        #map { position: absolute; top: 0; left: 0; width: 100%; height: 100%; z-index: 1; }
        
        /* Botón de actualización manual */
        #update-btn {
            position: fixed;
            top: 10px;
            left: 10px;
            z-index: 1000;
            background: rgba(52, 152, 219, 0.9);
            color: white;
            border: none;
            padding: 8px 16px;
            border-radius: 6px;
            font-size: 14px;
            cursor: pointer;
            box-shadow: 0 2px 10px rgba(0,0,0,0.3);
        }
        #update-btn:hover {
            background: rgba(41, 128, 185, 0.95);
        }
        #update-btn:active {
            transform: scale(0.98);
        }
        
        /* Estadísticas flotantes */
        #stats-bar {
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
        }
        .stat-value { font-weight: bold; color: #2c3e50; font-size: 16px; }
        .stat-label { font-size: 9px; color: #7f8c8d; }
        .custom-popup { font-family: Arial; padding: 12px; min-width: 280px; background: white; border-radius: 6px; }
        .custom-popup h4 { margin: 0 0 10px 0; color: #2c3e50; font-size: 16px; }
        .custom-popup hr { margin: 8px 0; border-color: #ecf0f1; }
        .custom-popup .var-row { margin: 6px 0; padding: 4px 0; display: flex; justify-content: space-between; font-size: 13px; }
        .custom-popup .var-label { color: #7f8c8d; }
        .custom-popup .var-value { font-weight: bold; color: #2c3e50; }
        .custom-popup .timestamp { font-size: 11px; color: #95a5a6; text-align: center; margin-top: 8px; }
        
        /* Mensaje de estado */
        #status-msg {
            position: fixed;
            bottom: 15px;
            left: 50%;
            transform: translateX(-50%);
            background: rgba(46, 204, 113, 0.9);
            color: white;
            padding: 8px 20px;
            border-radius: 20px;
            font-size: 14px;
            z-index: 999;
            opacity: 0;
            transition: opacity 0.3s;
        }
        #status-msg.error {
            background: rgba(231, 76, 60, 0.9);
        }
    </style>
</head>
<body>
    <div id="map"></div>
    <button id="update-btn" onclick="cargarDatos()">🔄 Actualizar</button>
    <div id="stats-bar">
        <div><div class="stat-value">📡 <span id="stat-total">0</span></div><div class="stat-label">Total</div></div>
        <div><div class="stat-value" style="color:#27ae60">🟢 <span id="stat-activos">0</span></div><div class="stat-label">Activos</div></div>
        <div><div class="stat-value" style="color:#e74c3c">🔴 <span id="stat-inactivos">0</span></div><div class="stat-label">Inactivos</div></div>
        <div><div class="stat-value" style="color:#3498db">🔵 <span id="stat-tanques">0</span></div><div class="stat-label">Tanques</div></div>
        <div><div class="stat-value" style="color:#000">⚫ <span id="stat-offline">0</span></div><div class="stat-label">Offline</div></div>
        <div><div class="stat-value">🕐 <span id="stat-time">--:--</span></div><div class="stat-label">Actualizado</div></div>
    </div>
    <div id="status-msg"></div>

    <script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"></script>
    <script>
        // ════════════════════════════════════════════════════════════════
        // CONFIGURACIÓN - MODIFICA ESTOS VALORES SEGÚN TUS NECESIDADES
        // ════════════════════════════════════════════════════════════════
        
        // Tiempo de actualización en milisegundos:
        // 5000 = 5 segundos (pruebas muy rápidas)
        // 10000 = 10 segundos (pruebas rápidas)
        // 30000 = 30 segundos (pruebas)
        // 300000 = 5 minutos (producción)
        const INTERVALO_ACTUALIZACION = 5000; // ⬅️ CAMBIA ESTE VALOR
        
        // URL del JSON en GitHub (usando proxy CORS)
        const URL_GITHUB_RAW = 'https://raw.githubusercontent.com/AlarmasCiateq/SCADA_T/main/datos_estaciones.json';
        const PROXY_CORS = 'https://corsproxy.io/?'; // Proxy público gratuito
        
        // ════════════════════════════════════════════════════════════════
        
        let map = null;
        let markers = new Map(); // id -> marker
        let primeraCarga = true;
        let timer = null;
        
        // Inicializar mapa
        function initMap() {
            map = L.map('map', {
                zoomControl: true,
                scrollWheelZoom: true,
                dragging: true
            });
            
            // Mapa claro con calles sutiles
            L.tileLayer('https://{s}.basemaps.cartocdn.com/light_all/{z}/{x}/{y}{r}.png', {
                attribution: '',
                subdomains: 'abcd',
                maxZoom: 19
            }).addTo(map);
            
            // Cargar datos iniciales
            cargarDatos();
            
            // Programar actualización automática
            timer = setInterval(cargarDatos, INTERVALO_ACTUALIZACION);
        }
        
        // Cargar datos desde GitHub usando proxy CORS
        async function cargarDatos() {
            try {
                // Mostrar mensaje de carga
                mostrarMensaje('Actualizando datos...', false);
                
                const timestamp = Date.now();
                const urlCompleta = PROXY_CORS + encodeURIComponent(URL_GITHUB_RAW + '?t=' + timestamp);
                
                const response = await fetch(urlCompleta, {
                    method: 'GET',
                    headers: {
                        'Accept': 'application/json'
                    }
                });
                
                if (!response.ok) {
                    throw new Error(`HTTP error! status: ${response.status}`);
                }
                
                const texto = await response.text();
                const datos = JSON.parse(texto);
                
                actualizarMapa(datos);
                actualizarEstadisticas(datos);
                
                // Actualizar timestamp
                document.getElementById('stat-time').textContent = new Date().toLocaleTimeString('es-ES', { 
                    hour: '2-digit', 
                    minute: '2-digit' 
                });
                
                // Mostrar mensaje de éxito
                mostrarMensaje('✓ Datos actualizados', false);
                
                console.log('✓ Datos actualizados:', new Date().toLocaleTimeString());
                
            } catch (error) {
                console.error('✗ Error al cargar datos:', error);
                mostrarMensaje('✗ Error: ' + error.message, true);
            }
        }
        
        // Mostrar mensaje temporal
        function mostrarMensaje(texto, esError) {
            const msg = document.getElementById('status-msg');
            msg.textContent = texto;
            msg.className = esError ? 'error' : '';
            msg.style.opacity = '1';
            
            setTimeout(() => {
                msg.style.opacity = '0';
            }, 3000);
        }
        
        // Actualizar mapa (solo valores y colores, no posiciones)
        function actualizarMapa(datos) {
            if (!datos || !datos.estaciones) return;
            
            const nuevasBounds = [];
            
            datos.estaciones.forEach(estacion => {
                if (!estacion.latitud || !estacion.longitud) return;
                
                const id = estacion.nombre || `${estacion.latitud},${estacion.longitud}`;
                const lat = parseFloat(estacion.latitud);
                const lng = parseFloat(estacion.longitud);
                
                nuevasBounds.push([lat, lng]);
                
                // Si ya existe el marcador, actualizar popup y color
                if (markers.has(id)) {
                    const marker = markers.get(id);
                    
                    // Actualizar popup
                    const popupContent = crearPopupContent(estacion);
                    marker.setPopupContent(popupContent);
                    
                    // Actualizar color si cambió estado
                    const nuevoIcono = crearIcono(estacion.tipo, estacion.estado_bomba, estacion.en_linea);
                    marker.setIcon(nuevoIcono);
                    
                } else {
                    // Crear nuevo marcador
                    const icono = crearIcono(estacion.tipo, estacion.estado_bomba, estacion.en_linea);
                    const popupContent = crearPopupContent(estacion);
                    
                    const marker = L.marker([lat, lng], { icon: icono })
                        .bindPopup(popupContent, { maxWidth: 320 })
                        .addTo(map);
                    
                    markers.set(id, marker);
                }
            });
            
            // Ajustar bounds SOLO en primera carga
            if (primeraCarga && nuevasBounds.length > 0) {
                const bounds = L.latLngBounds(nuevasBounds);
                map.fitBounds(bounds, { padding: [40, 40] });
                primeraCarga = false;
                console.log('✓ Zoom inicial ajustado');
            }
        }
        
        // Crear icono según tipo y estado
        function crearIcono(tipo, estado, enLinea) {
            // Determinar color
            let color = '#000000'; // negro por defecto (offline)
            if (enLinea !== 0) {
                if (tipo === 'pozo' || tipo === 'bomba') {
                    color = estado === 1 ? '#27ae60' : '#e74c3c'; // verde/rojo
                } else if (tipo === 'tanque') {
                    color = estado === 1 ? '#3498db' : '#95a5a6'; // azul/gris
                } else if (tipo === 'sensor') {
                    color = '#9b59b6'; // morado
                } else {
                    color = '#f39c12'; // naranja
                }
            }
            
            // Determinar ícono (siempre el mismo según tipo)
            let iconClass = '💧'; // pozo por defecto
            if (tipo === 'tanque') iconClass = '🌊';
            else if (tipo === 'bomba') iconClass = '⚙️';
            else if (tipo === 'sensor') iconClass = '📡';
            
            return L.divIcon({
                html: `<div style="
                    background: ${color};
                    width: 32px;
                    height: 32px;
                    border-radius: 50%;
                    display: flex;
                    align-items: center;
                    justify-content: center;
                    box-shadow: 0 2px 6px rgba(0,0,0,0.4);
                    font-size: 18px;
                    color: white;
                ">${iconClass}</div>`,
                className: '',
                iconSize: [32, 32],
                iconAnchor: [16, 16],
                popupAnchor: [0, -16]
            });
        }
        
        // Crear contenido del popup
        function crearPopupContent(estacion) {
            let html = `<div class="custom-popup"><h4>${estacion.nombre || 'Estación'}</h4><hr>`;
            
            for (const key in estacion) {
                if (!['nombre', 'latitud', 'longitud', 'tipo', 'estado_bomba', 'en_linea', 'icono'].includes(key)) {
                    const value = typeof estacion[key] === 'number' 
                        ? estacion[key].toLocaleString('es-ES', { minimumFractionDigits: 2, maximumFractionDigits: 2 })
                        : estacion[key];
                    
                    html += `<div class="var-row"><span class="var-label">${key}:</span><span class="var-value">${value}</span></div>`;
                }
            }
            
            html += `<hr><div class="timestamp">📅 ${new Date().toLocaleString('es-ES')}</div></div>`;
            return html;
        }
        
        // Actualizar estadísticas
        function actualizarEstadisticas(datos) {
            if (!datos || !datos.estaciones) return;
            
            const stats = { total:0, activos:0, inactivos:0, tanques:0, offline:0 };
            
            datos.estaciones.forEach(estacion => {
                stats.total++;
                const enLinea = estacion.en_linea || 1;
                const tipo = estacion.tipo || 'otro';
                const estado = estacion.estado_bomba || estacion.estado || 0;
                
                if (enLinea === 0) stats.offline++;
                else if (tipo === 'pozo') {
                    if (estado === 1) stats.activos++;
                    else stats.inactivos++;
                } else if (tipo === 'tanque') stats.tanques++;
            });
            
            document.getElementById('stat-total').textContent = stats.total;
            document.getElementById('stat-activos').textContent = stats.activos;
            document.getElementById('stat-inactivos').textContent = stats.inactivos;
            document.getElementById('stat-tanques').textContent = stats.tanques;
            document.getElementById('stat-offline').textContent = stats.offline;
        }
        
        // Iniciar cuando el DOM esté listo
        document.addEventListener('DOMContentLoaded', initMap);
        
        // Limpiar intervalo al cerrar la página
        window.addEventListener('beforeunload', () => {
            if (timer) clearInterval(timer);
        });
    </script>
</body>
</html>
"""

# Mostrar el HTML+JS en Streamlit
st.components.v1.html(
    html_completo,
    width=1920,
    height=1080,
    scrolling=False
)
