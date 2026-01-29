# import streamlit as st
# import requests
# import json
# from datetime import datetime
# from streamlit_autorefresh import st_autorefresh

# # Configuración minimalista
# st.set_page_config(
#     page_title="SCADA Monitor",
#     layout="wide",
#     initial_sidebar_state="collapsed"
# )

# # CSS para ocultar elementos de Streamlit
# st.markdown("""
#     <style>
#     [data-testid="stSidebar"] { display: none; }
#     [data-testid="stHeader"] { display: none; }
#     .block-container { padding: 0; max-width: 100%; margin: 0; }
#     .stApp { background-color: #0e1117; }
#     footer, .stDeployButton { display: none !important; }
#     </style>
#     """, unsafe_allow_html=True)

# # ==============================
# # CARGAR DATOS DESDE GITHUB (Python - SIN CORS)
# # ==============================
# def cargar_datos_github():
#     try:
#         # URL CORRECTA sin espacios
#         url = "https://raw.githubusercontent.com/AlarmasCiateq/SCADA_T/main/datos_estaciones.json"
        
#         # Forzar carga fresca (sin cache)
#         response = requests.get(
#             url + f"?t={int(datetime.now().timestamp() * 1000)}",
#             timeout=10,
#             headers={'Cache-Control': 'no-cache'}
#         )
#         response.raise_for_status()
#         return response.json()
#     except Exception as e:
#         st.error(f"Error al cargar datos: {str(e)[:50]}")
#         return None

# # ==============================
# # AUTO-REFRESH (5 segundos para pruebas)
# # ==============================
# # ⚠️ CAMBIA A 300000 PARA PRODUCCIÓN (5 minutos)
# st_autorefresh(interval=5000, key="auto_refresh")

# # ==============================
# # CARGAR DATOS
# # ==============================
# datos = cargar_datos_github()
# if not datos:
#     st.error("⚠️ No se pudieron cargar los datos de GitHub")
#     st.stop()

# # ==============================
# # GENERAR HTML+JS CON DATOS EMBEBIDOS
# # ==============================
# # Convertir datos a JSON string para embeber en JavaScript
# datos_json = json.dumps(datos)

# html_completo = f"""
# <!DOCTYPE html>
# <html lang="es">
# <head>
#     <meta charset="UTF-8">
#     <meta name="viewport" content="width=device-width, initial-scale=1.0">
#     <title>SCADA Monitor</title>
#     <link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css" />
#     <style>
#         * {{ margin: 0; padding: 0; box-sizing: border-box; }}
#         body {{ font-family: Arial, sans-serif; background: #0e1117; overflow: hidden; }}
#         #map {{ position: absolute; top: 0; left: 0; width: 100%; height: 100%; z-index: 1; }}
        
#         /* Estadísticas flotantes */
#         #stats-bar {{
#             position: fixed;
#             top: 10px;
#             right: 15px;
#             background: rgba(255, 255, 255, 0.95);
#             padding: 8px 15px;
#             border-radius: 8px;
#             box-shadow: 0 2px 10px rgba(0,0,0,0.15);
#             z-index: 1000;
#             display: grid;
#             grid-template-columns: repeat(6, auto);
#             gap: 12px;
#             align-items: center;
#             font-family: Arial, sans-serif;
#             font-size: 13px;
#         }}
#         .stat-value {{ font-weight: bold; color: #2c3e50; font-size: 16px; }}
#         .stat-label {{ font-size: 9px; color: #7f8c8d; }}
#         .custom-popup {{ font-family: Arial; padding: 12px; min-width: 280px; background: white; border-radius: 6px; }}
#         .custom-popup h4 {{ margin: 0 0 10px 0; color: #2c3e50; font-size: 16px; }}
#         .custom-popup hr {{ margin: 8px 0; border-color: #ecf0f1; }}
#         .custom-popup .var-row {{ margin: 6px 0; padding: 4px 0; display: flex; justify-content: space-between; font-size: 13px; }}
#         .custom-popup .var-label {{ color: #7f8c8d; }}
#         .custom-popup .var-value {{ font-weight: bold; color: #2c3e50; }}
#         .custom-popup .timestamp {{ font-size: 11px; color: #95a5a6; text-align: center; margin-top: 8px; }}
#     </style>
# </head>
# <body>
#     <div id="map"></div>
#     <div id="stats-bar">
#         <div><div class="stat-value">📡 <span id="stat-total">0</span></div><div class="stat-label">Total</div></div>
#         <div><div class="stat-value" style="color:#27ae60">🟢 <span id="stat-activos">0</span></div><div class="stat-label">Activos</div></div>
#         <div><div class="stat-value" style="color:#e74c3c">🔴 <span id="stat-inactivos">0</span></div><div class="stat-label">Inactivos</div></div>
#         <div><div class="stat-value" style="color:#3498db">🔵 <span id="stat-tanques">0</span></div><div class="stat-label">Tanques</div></div>
#         <div><div class="stat-value" style="color:#000">⚫ <span id="stat-offline">0</span></div><div class="stat-label">Offline</div></div>
#         <div><div class="stat-value">🕐 <span id="stat-time">--:--</span></div><div class="stat-label">Actualizado</div></div>
#     </div>

#     <script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"></script>
#     <script>
#         // ════════════════════════════════════════════════════════════════
#         // DATOS CARGADOS DESDE PYTHON (embebidos en el HTML)
#         // ════════════════════════════════════════════════════════════════
#         const DATOS_INICIALES = {datos_json};
        
#         // ════════════════════════════════════════════════════════════════
        
#         let map = null;
#         let markers = new Map(); // id -> marker
#         let primeraCarga = true;
        
#         // Inicializar mapa
#         function initMap() {{
#             map = L.map('map', {{
#                 zoomControl: true,
#                 scrollWheelZoom: true,
#                 dragging: true
#             }});
            
#             // Mapa claro con calles sutiles
#             L.tileLayer('https://{{s}}.basemaps.cartocdn.com/light_all/{{z}}/{{x}}/{{y}}{{r}}.png', {{
#                 attribution: '',
#                 subdomains: 'abcd',
#                 maxZoom: 19
#             }}).addTo(map);
            
#             // Cargar datos iniciales
#             actualizarMapa(DATOS_INICIALES);
#             actualizarEstadisticas(DATOS_INICIALES);
            
#             // Actualizar timestamp
#             document.getElementById('stat-time').textContent = new Date().toLocaleTimeString('es-ES', {{ 
#                 hour: '2-digit', 
#                 minute: '2-digit' 
#             }});
#         }}
        
#         // Actualizar mapa (solo valores y colores, no posiciones)
#         function actualizarMapa(datos) {{
#             if (!datos || !datos.estaciones) return;
            
#             const nuevasBounds = [];
            
#             datos.estaciones.forEach(estacion => {{
#                 if (!estacion.latitud || !estacion.longitud) return;
                
#                 const id = estacion.nombre || `${{estacion.latitud}},${{estacion.longitud}}`;
#                 const lat = parseFloat(estacion.latitud);
#                 const lng = parseFloat(estacion.longitud);
                
#                 nuevasBounds.push([lat, lng]);
                
#                 // Si ya existe el marcador, actualizar popup y color
#                 if (markers.has(id)) {{
#                     const marker = markers.get(id);
                    
#                     // Actualizar popup
#                     const popupContent = crearPopupContent(estacion);
#                     marker.setPopupContent(popupContent);
                    
#                     // Actualizar color si cambió estado
#                     const nuevoIcono = crearIcono(estacion.tipo, estacion.estado_bomba, estacion.en_linea);
#                     marker.setIcon(nuevoIcono);
                    
#                 }} else {{
#                     // Crear nuevo marcador
#                     const icono = crearIcono(estacion.tipo, estacion.estado_bomba, estacion.en_linea);
#                     const popupContent = crearPopupContent(estacion);
                    
#                     const marker = L.marker([lat, lng], {{ icon: icono }})
#                         .bindPopup(popupContent, {{ maxWidth: 320 }})
#                         .addTo(map);
                    
#                     markers.set(id, marker);
#                 }}
#             }});
            
#             // Ajustar bounds SOLO en primera carga
#             if (primeraCarga && nuevasBounds.length > 0) {{
#                 const bounds = L.latLngBounds(nuevasBounds);
#                 map.fitBounds(bounds, {{ padding: [40, 40] }});
#                 primeraCarga = false;
#                 console.log('✓ Zoom inicial ajustado');
#             }}
#         }}
        
#         // Crear icono según tipo y estado
#         function crearIcono(tipo, estado, enLinea) {{
#             // Determinar color
#             let color = '#000000'; // negro por defecto (offline)
#             if (enLinea !== 0) {{
#                 if (tipo === 'pozo' || tipo === 'bomba') {{
#                     color = estado === 1 ? '#27ae60' : '#e74c3c'; // verde/rojo
#                 }} else if (tipo === 'tanque') {{
#                     color = estado === 1 ? '#3498db' : '#95a5a6'; // azul/gris
#                 }} else if (tipo === 'sensor') {{
#                     color = '#9b59b6'; // morado
#                 }} else {{
#                     color = '#f39c12'; // naranja
#                 }}
#             }}
            
#             // Determinar ícono (siempre el mismo según tipo)
#             let iconClass = 'fa-tint'; // pozo por defecto
#             if (tipo === 'tanque') iconClass = 'fa-water';
#             else if (tipo === 'bomba') iconClass = 'fa-cog';
#             else if (tipo === 'sensor') iconClass = 'fa-microchip';
            
#             return L.divIcon({{
#                 html: `<div style="
#                     background: ${{color}};
#                     width: 32px;
#                     height: 32px;
#                     border-radius: 50%;
#                     display: flex;
#                     align-items: center;
#                     justify-content: center;
#                     box-shadow: 0 2px 6px rgba(0,0,0,0.4);
#                 ">
#                     <i class="fa ${{iconClass}}" style="color: white; font-size: 16px;"></i>
#                 </div>`,
#                 className: '',
#                 iconSize: [32, 32],
#                 iconAnchor: [16, 16],
#                 popupAnchor: [0, -16]
#             }});
#         }}
        
#         // Crear contenido del popup
#         function crearPopupContent(estacion) {{
#             let html = `<div class="custom-popup"><h4>${{estacion.nombre || 'Estación'}}</h4><hr>`;
            
#             for (const key in estacion) {{
#                 if (!['nombre', 'latitud', 'longitud', 'tipo', 'estado_bomba', 'en_linea', 'icono'].includes(key)) {{
#                     const value = typeof estacion[key] === 'number' 
#                         ? estacion[key].toLocaleString('es-ES', {{ minimumFractionDigits: 2, maximumFractionDigits: 2 }})
#                         : estacion[key];
                    
#                     html += `<div class="var-row"><span class="var-label">${{key}}:</span><span class="var-value">${{value}}</span></div>`;
#                 }}
#             }}
            
#             html += `<hr><div class="timestamp">📅 ${{new Date().toLocaleString('es-ES')}}</div></div>`;
#             return html;
#         }}
        
#         // Actualizar estadísticas
#         function actualizarEstadisticas(datos) {{
#             if (!datos || !datos.estaciones) return;
            
#             const stats = {{ total:0, activos:0, inactivos:0, tanques:0, offline:0 }};
            
#             datos.estaciones.forEach(estacion => {{
#                 stats.total++;
#                 const enLinea = estacion.en_linea || 1;
#                 const tipo = estacion.tipo || 'otro';
#                 const estado = estacion.estado_bomba || estacion.estado || 0;
                
#                 if (enLinea === 0) stats.offline++;
#                 else if (tipo === 'pozo') {{
#                     if (estado === 1) stats.activos++;
#                     else stats.inactivos++;
#                 }} else if (tipo === 'tanque') stats.tanques++;
#             }});
            
#             document.getElementById('stat-total').textContent = stats.total;
#             document.getElementById('stat-activos').textContent = stats.activos;
#             document.getElementById('stat-inactivos').textContent = stats.inactivos;
#             document.getElementById('stat-tanques').textContent = stats.tanques;
#             document.getElementById('stat-offline').textContent = stats.offline;
#         }}
        
#         // Iniciar cuando el DOM esté listo
#         document.addEventListener('DOMContentLoaded', initMap);
#     </script>
    
#     <!-- Font Awesome para íconos -->
#     <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
# </body>
# </html>
# """

# # Mostrar el HTML+JS en Streamlit (se ejecutará en el navegador)
# st.components.v1.html(
#     html_completo,
#     width=1920,
#     height=1080,
#     scrolling=False
# )
# import streamlit as st
# import requests
# import json
# import base64
# from datetime import datetime
# from streamlit_autorefresh import st_autorefresh
# import time

# # Configuración minimalista - SIN TÍTULO NI DECORACIONES
# st.set_page_config(
#     page_title="SCADA Monitor",
#     layout="wide",
#     initial_sidebar_state="collapsed"
# )

# # CSS AGRESIVO para eliminar TODO (header, título, scroll, barras)
# st.markdown("""
#     <style>
#     /* Eliminar TODO */
#     [data-testid="stSidebar"] { display: none !important; }
#     [data-testid="stHeader"] { display: none !important; }
#     [data-testid="stDecoration"] { display: none !important; }
#     header { display: none !important; }
#     #MainMenu { display: none !important; }
#     footer { display: none !important; }
#     .stApp { 
#         background-color: #0e1117; 
#         padding: 0 !important; 
#         margin: 0 !important; 
#         overflow: hidden !important;
#     }
#     .block-container { 
#         padding: 0 !important; 
#         max-width: 100% !important; 
#         margin: 0 !important; 
#         overflow: hidden !important;
#     }
#     .main { 
#         padding: 0 !important; 
#         margin: 0 !important; 
#         overflow: hidden !important;
#     }
#     .block-container > div { 
#         padding: 0 !important; 
#         margin: 0 !important; 
#     }
#     /* Ocultar cualquier scroll */
#     ::-webkit-scrollbar { display: none !important; }
#     body { overflow: hidden !important; }
#     </style>
#     """, unsafe_allow_html=True)

# # ==============================
# # CARGAR DATOS CON REINTENTOS SILENCIOSOS (usa datos anteriores si falla)
# # ==============================
# def cargar_datos_github(datos_anteriores=None, max_intentos=3):
#     for intento in range(max_intentos):
#         try:
#             GITHUB_USER = "AlarmasCiateq"
#             REPO_NAME = "SCADA_T"
#             BRANCH = "main"
#             FILE_PATH = "datos_estaciones.json"
            
#             api_url = f"https://api.github.com/repos/{GITHUB_USER}/{REPO_NAME}/contents/{FILE_PATH}?ref={BRANCH}"
            
#             headers = {
#                 'User-Agent': f'SCADA-Monitor-{datetime.now().timestamp()}',
#                 'Accept': 'application/vnd.github.v3+json'
#             }
            
#             response = requests.get(api_url, headers=headers, timeout=10)
#             response.raise_for_status()
            
#             data = response.json()
#             content_bytes = base64.b64decode(data['content'])
#             content_str = content_bytes.decode('utf-8')
#             datos = json.loads(content_str)
            
#             return datos  # Éxito: devuelve nuevos datos
            
#         except Exception:
#             if intento < max_intentos - 1:
#                 time.sleep(1)  # Espera 1 segundo y reintenta
#                 continue
    
#     # Falló todo: devuelve datos anteriores si existen, sino None
#     return datos_anteriores if datos_anteriores else None

# # ==============================
# # AUTO-REFRESH (5 segundos para pruebas)
# # ==============================
# st_autorefresh(interval=60000, key="auto_refresh")

# # ==============================
# # CARGAR DATOS (usa cache en session_state para mantener estado anterior)
# # ==============================
# if 'datos_cache' not in st.session_state:
#     st.session_state.datos_cache = None

# # Intentar cargar nuevos datos (con reintentos silenciosos)
# nuevos_datos = cargar_datos_github(st.session_state.datos_cache)

# # Si hay nuevos datos válidos, actualizar cache
# if nuevos_datos:
#     st.session_state.datos_cache = nuevos_datos

# # Usar datos del cache (pueden ser nuevos o anteriores si falló la carga)
# datos = st.session_state.datos_cache

# # Si NO hay datos en absoluto (primera carga fallida), mostrar mínimo
# if not datos:
#     st.markdown("""
#         <div style="position:fixed;top:0;left:0;width:100%;height:100%;background:#0e1117;color:white;
#                     display:flex;justify-content:center;align-items:center;font-family:Arial;">
#             <div style="text-align:center;padding:20px;">
#                 <h2>🛢️ SCADA Monitor</h2>
#                 <p>Esperando primera conexión con el sistema...</p>
#             </div>
#         </div>
#         """, unsafe_allow_html=True)
#     st.stop()

# # ==============================
# # GENERAR HTML+JS (tooltip simple + popup completo)
# # ==============================
# datos_json = json.dumps(datos)

# html_completo = f"""
# <!DOCTYPE html>
# <html lang="es">
# <head>
#     <meta charset="UTF-8">
#     <meta name="viewport" content="width=device-width, initial-scale=1.0">
#     <title>SCADA Monitor</title>
#     <link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css" />
#     <style>
#         * {{ margin: 0; padding: 0; box-sizing: border-box; }}
#         body {{ 
#             font-family: Arial, sans-serif; 
#             background: #0e1117; 
#             overflow: hidden; 
#             height: 100vh;
#             width: 100vw;
#         }}
#         #map {{ 
#             position: absolute; 
#             top: 0; 
#             left: 0; 
#             width: 100%; 
#             height: 100%; 
#             z-index: 1; 
#         }}
#         #stats-bar {{
#             position: fixed;
#             top: 10px;
#             right: 15px;
#             background: rgba(255, 255, 255, 0.95);
#             padding: 6px 10px;
#             border-radius: 6px;
#             box-shadow: 0 2px 8px rgba(0,0,0,0.15);
#             z-index: 1000;
#             display: grid;
#             grid-template-columns: repeat(7, auto);
#             gap: 8px;
#             align-items: center;
#             font-family: Arial, sans-serif;
#             font-size: 11px;
#         }}
#         .stat-value {{ font-weight: bold; color: #2c3e50; font-size: 14px; }}
#         .stat-label {{ font-size: 7px; color: #7f8c8d; white-space: nowrap; }}
#         .custom-popup {{ font-family: Arial; padding: 12px; min-width: 280px; background: white; border-radius: 6px; }}
#         .custom-popup h4 {{ margin: 0 0 10px 0; color: #2c3e50; font-size: 16px; }}
#         .custom-popup hr {{ margin: 8px 0; border-color: #ecf0f1; }}
#         .custom-popup .var-row {{ margin: 6px 0; padding: 4px 0; display: flex; justify-content: space-between; font-size: 13px; }}
#         .custom-popup .var-label {{ color: #7f8c8d; }}
#         .custom-popup .var-value {{ font-weight: bold; color: #2c3e50; }}
#         .custom-popup .timestamp {{ font-size: 11px; color: #95a5a6; text-align: center; margin-top: 8px; }}
#     </style>
# </head>
# <body>
#     <div id="map"></div>
#     <div id="stats-bar">
#         <div><div class="stat-value">📡 <span id="stat-total">0</span></div><div class="stat-label">Total</div></div>
#         <div><div class="stat-value" style="color:#27ae60">🟢 <span id="stat-encendidos">0</span></div><div class="stat-label">Pozos Encendidos</div></div>
#         <div><div class="stat-value" style="color:#e74c3c">🔴 <span id="stat-apagados">0</span></div><div class="stat-label">Pozos Apagados</div></div>
#         <div><div class="stat-value" style="color:#3498db">🔵 <span id="stat-tanques">0</span></div><div class="stat-label">Tanques</div></div>
#         <div><div class="stat-value" style="color:#000">⚫ </div></div>
#         <div><div class="stat-value">🕐 <span id="stat-time">--:--</span></div><div class="stat-label">Actualizado</div></div>
#     </div>

#     <script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"></script>
#     <script>
#         const DATOS_INICIALES = {datos_json};
#         let map = null;
#         let markers = new Map();
#         let primeraCarga = true;
        
#         function initMap() {{
#             map = L.map('map', {{
#                 zoomControl: true,
#                 scrollWheelZoom: true,
#                 dragging: true
#             }});
            
#             L.tileLayer('https://{{s}}.basemaps.cartocdn.com/light_all/{{z}}/{{x}}/{{y}}{{r}}.png', {{
#                 attribution: '',
#                 subdomains: 'abcd',
#                 maxZoom: 19
#             }}).addTo(map);
            
#             actualizarMapa(DATOS_INICIALES);
#             actualizarEstadisticas(DATOS_INICIALES);
#             document.getElementById('stat-time').textContent = new Date().toLocaleTimeString('es-ES', {{ hour: '2-digit', minute: '2-digit' }});
#         }}
        
#         function actualizarMapa(datos) {{
#             if (!datos || !datos.estaciones) return;
#             const nuevasBounds = [];
            
#             datos.estaciones.forEach(estacion => {{
#                 if (!estacion.latitud || !estacion.longitud) return;
#                 const id = estacion.nombre || `${{estacion.latitud}},${{estacion.longitud}}`;
#                 const lat = parseFloat(estacion.latitud);
#                 const lng = parseFloat(estacion.longitud);
#                 nuevasBounds.push([lat, lng]);
                
#                 if (markers.has(id)) {{
#                     const marker = markers.get(id);
#                     marker.setPopupContent(crearPopupContent(estacion));
#                     marker.setIcon(crearIcono(estacion.tipo, estacion.estado_bomba, estacion.en_linea));
#                 }} else {{
#                     const marker = L.marker([lat, lng], {{ 
#                         icon: crearIcono(estacion.tipo, estacion.estado_bomba, estacion.en_linea)
#                     }})
#                     .bindPopup(crearPopupContent(estacion), {{ maxWidth: 320 }})
#                     .bindTooltip(estacion.nombre || 'Estación', {{ 
#                         permanent: false, 
#                         direction: 'top',
#                         opacity: 0.9
#                     }})
#                     .addTo(map);
#                     markers.set(id, marker);
#                 }}
#             }});
            
#             if (primeraCarga && nuevasBounds.length > 0) {{
#                 map.fitBounds(nuevasBounds, {{ padding: [40, 40] }});
#                 primeraCarga = false;
#             }}
#         }}
        
#         function crearIcono(tipo, estado, enLinea) {{
#             let color = '#000000';
#             if (enLinea !== 0) {{
#                 if (tipo === 'pozo' || tipo === 'bomba') {{
#                     color = estado === 1 ? '#27ae60' : '#e74c3c';
#                 }} else if (tipo === 'tanque') {{
#                     color = estado === 1 ? '#3498db' : '#95a5a6';
#                 }} else if (tipo === 'sensor') {{
#                     color = '#9b59b6';
#                 }} else {{
#                     color = '#f39c12';
#                 }}
#             }}
            
#             let iconClass = 'fa-tint';
#             if (tipo === 'tanque') iconClass = 'fa-water';
#             else if (tipo === 'bomba') iconClass = 'fa-cog';
#             else if (tipo === 'sensor') iconClass = 'fa-microchip';
            
#             return L.divIcon({{
#                 html: `<div style="background:${{color}};width:32px;height:32px;border-radius:50%;display:flex;align-items:center;justify-content:center;box-shadow:0 2px 6px rgba(0,0,0,0.4);"><i class="fa ${{iconClass}}" style="color:white;font-size:16px;"></i></div>`,
#                 className: '',
#                 iconSize: [32, 32],
#                 iconAnchor: [16, 16],
#                 popupAnchor: [0, -16]
#             }});
#         }}
        
#         function crearPopupContent(estacion) {{
#             let html = `<div class="custom-popup"><h4>${{estacion.nombre || 'Estación'}}</h4><hr>`;
#             for (const key in estacion) {{
#                 if (!['nombre', 'latitud', 'longitud', 'tipo', 'estado_bomba', 'en_linea', 'icono'].includes(key)) {{
#                     const value = typeof estacion[key] === 'number' ? estacion[key].toLocaleString('es-ES', {{ minimumFractionDigits: 2, maximumFractionDigits: 2 }}) : estacion[key];
#                     html += `<div class="var-row"><span class="var-label">${{key}}:</span><span class="var-value">${{value}}</span></div>`;
#                 }}
#             }}
#             html += `<hr><div class="timestamp">📅 ${{new Date().toLocaleString('es-ES')}}</div></div>`;
#             return html;
#         }}
        
#         function actualizarEstadisticas(datos) {{
#             if (!datos || !datos.estaciones) return;
#             const stats = {{ total:0, pozos_encendidos:0, pozos_apagados:0, tanques:0, offline:0, online:0 }};
            
#             datos.estaciones.forEach(estacion => {{
#                 stats.total++;
#                 const enLinea = estacion.en_linea || 1;
#                 const tipo = estacion.tipo || 'otro';
#                 const estado = estacion.estado_bomba || estacion.estado || 0;
                
#                 if (enLinea === 0) stats.offline++;
#                 else stats.online++;
                
#                 if (tipo === 'pozo' && enLinea === 1) {{
#                     if (estado === 1) stats.pozos_encendidos++;
#                     else stats.pozos_apagados++;
#                 }} else if (tipo === 'tanque') stats.tanques++;
#             }});
            
#             document.getElementById('stat-total').textContent = stats.total;
#             document.getElementById('stat-encendidos').textContent = stats.pozos_encendidos;
#             document.getElementById('stat-apagados').textContent = stats.pozos_apagados;
#             document.getElementById('stat-tanques').textContent = stats.tanques;
#             document.getElementById('stat-offline').textContent = stats.offline;
#             document.getElementById('stat-online').textContent = stats.online;
#         }}
        
#         document.addEventListener('DOMContentLoaded', initMap);
#     </script>
#     <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
# </body>
# </html>
# """

# # Mostrar mapa ocupando TODO el espacio (sin scroll)
# st.components.v1.html(
#     html_completo,
#     width=1920,
#     height=1080,
#     scrolling=False
# )

import streamlit as st
import requests
import json
import base64
from datetime import datetime
from streamlit_autorefresh import st_autorefresh
import time
import os

# Configuración minimalista
st.set_page_config(
    page_title="🌎 SCADA Monitor",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# CSS AGRESIVO para eliminar TODO
st.markdown("""
    <style>
    [data-testid="stSidebar"] { display: none !important; }
    [data-testid="stHeader"] { display: none !important; }
    [data-testid="stDecoration"] { display: none !important; }
    header { display: none !important; }
    #MainMenu { display: none !important; }
    footer { display: none !important; }
    .stApp { background-color: #0e1117; padding: 0 !important; margin: 0 !important; overflow: hidden !important; }
    .block-container { padding: 0 !important; max-width: 100% !important; margin: 0 !important; overflow: hidden !important; }
    .main { padding: 0 !important; margin: 0 !important; overflow: hidden !important; }
    .block-container > div { padding: 0 !important; margin: 0 !important; }
    ::-webkit-scrollbar { display: none !important; }
    body { overflow: hidden !important; }
    </style>
    """, unsafe_allow_html=True)

# ==============================
# OBTENER TOKEN DE GITHUB (Streamlit Secrets o Environment Variable)
# ==============================
def obtener_token_github():
    """Obtiene el token de GitHub de Streamlit Secrets o variable de entorno"""
    try:
        # Intentar desde Streamlit Secrets (recomendado para producción)
        if hasattr(st, 'secrets') and "GITHUB_TOKEN" in st.secrets:
            return st.secrets["GITHUB_TOKEN"]
    except:
        pass
    
    # Intentar desde variable de entorno (para desarrollo local)
    return os.getenv("GITHUB_TOKEN", None)

# ==============================
# CARGAR DATOS CON TOKEN Y REINTENTOS SILENCIOSOS
# ==============================
def cargar_datos_github(datos_anteriores=None, max_intentos=3):
    token = obtener_token_github()
    
    for intento in range(max_intentos):
        try:
            GITHUB_USER = "AlarmasCiateq"
            REPO_NAME = "SCADA_T"
            BRANCH = "main"
            FILE_PATH = "datos_estaciones.json"
            
            api_url = f"https://api.github.com/repos/{GITHUB_USER}/{REPO_NAME}/contents/{FILE_PATH}?ref={BRANCH}"
            
            # Headers con token si está disponible
            headers = {
                'User-Agent': f'SCADA-Monitor-{datetime.now().timestamp()}',
                'Accept': 'application/vnd.github.v3+json'
            }
            
            # Agregar token si existe (aumenta límite a 5000 solicitudes/hora)
            if token:
                headers['Authorization'] = f'token {token}'
            
            response = requests.get(api_url, headers=headers, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            content_bytes = base64.b64decode(data['content'])
            content_str = content_bytes.decode('utf-8')
            datos = json.loads(content_str)
            
            return datos
            
        except requests.exceptions.HTTPError as e:
            # Si es error 401 (token inválido) o 403 (rate limit sin token), no reintentar
            if e.response.status_code in [401, 403]:
                # Si no hay token y es 403, es rate limit sin autenticación
                if not token and e.response.status_code == 403:
                    st.warning("⚠️ Sin token de GitHub. Límite de 60 solicitudes/hora alcanzado. Usa un token para 5000 solicitudes/hora.")
                return datos_anteriores if datos_anteriores else None
            # Para otros errores HTTP, reintentar
            if intento < max_intentos - 1:
                time.sleep(1)
                continue
            return datos_anteriores if datos_anteriores else None
        except Exception:
            if intento < max_intentos - 1:
                time.sleep(1)
                continue
            return datos_anteriores if datos_anteriores else None
    
    return datos_anteriores if datos_anteriores else None

# ==============================
# AUTO-REFRESH (5 segundos para pruebas)
# ==============================
st_autorefresh(interval=5000, key="auto_refresh")

# ==============================
# CARGAR DATOS
# ==============================
if 'datos_cache' not in st.session_state:
    st.session_state.datos_cache = None

nuevos_datos = cargar_datos_github(st.session_state.datos_cache)
if nuevos_datos:
    st.session_state.datos_cache = nuevos_datos

datos = st.session_state.datos_cache
if not datos:
    st.markdown("""
        <div style="position:fixed;top:0;left:0;width:100%;height:100%;background:#0e1117;color:white;
                    display:flex;justify-content:center;align-items:center;font-family:Arial;">
            <div style="text-align:center;padding:20px;">
                <h2>🛢️ SCADA Monitor</h2>
                <p>Esperando primera conexión...</p>
                <p style="font-size:12px;margin-top:10px;color:#7f8c8d">
                    {% if not token %}⚠️ Sin token de GitHub - Límite de 60 solicitudes/hora{% endif %}
                </p>
            </div>
        </div>
        """, unsafe_allow_html=True)
    st.stop()

# ==============================
# GENERAR HTML+JS (mismo código corregido anterior)
# ==============================
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
        body {{ font-family: Arial, sans-serif; background: #0e1117; overflow: hidden; height: 100vh; width: 100vw; }}
        #map {{ position: absolute; top: 0; left: 0; width: 100%; height: 100%; z-index: 1; }}
        #stats-bar {{
            position: fixed;
            top: 10px;
            right: 15px;
            background: rgba(255, 255, 255, 0.95);
            padding: 6px 10px;
            border-radius: 6px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.15);
            z-index: 1000;
            display: grid;
            grid-template-columns: repeat(7, auto);
            gap: 8px;
            align-items: center;
            font-family: Arial, sans-serif;
            font-size: 11px;
        }}
        .stat-value {{ font-weight: bold; color: #2c3e50; font-size: 14px; }}
        .stat-label {{ font-size: 7px; color: #7f8c8d; white-space: nowrap; }}
        .custom-popup {{ font-family: Arial; padding: 12px; min-width: 280px; background: white; border-radius: 6px; }}
        .custom-popup h4 {{ margin: 0 0 10px 0; color: #2c3e50; font-size: 16px; }}
        .custom-popup hr {{ margin: 8px 0; border-color: #ecf0f1; }}
        .custom-popup .var-row {{ margin: 6px 0; padding: 4px 0; display: flex; justify-content: space-between; font-size: 13px; }}
        .custom-popup .var-label {{ color: #7f8c8d; }}
        .custom-popup .var-value {{ font-weight: bold; color: #2c3e50; }}
        .custom-popup .timestamp {{ font-size: 11px; color: #95a5a6; text-align: center; margin-top: 8px; }}
        .status-online {{ color: #27ae60; font-weight: bold; }}
        .status-offline {{ color: #e74c3c; font-weight: bold; }}
    </style>
</head>
<body>
    <div id="map"></div>
    <div id="stats-bar">
        <div><div class="stat-value">📡 <span id="stat-total">0</span></div><div class="stat-label">Total Est.</div></div>
        <div><div class="stat-value" style="color:#27ae60">🟢 <span id="stat-encendidos">0</span></div><div class="stat-label">Pzs Off</div></div>
        <div><div class="stat-value" style="color:#e74c3c">🔴 <span id="stat-apagados">0</span></div><div class="stat-label">Pzs On</div></div>
        <div><div class="stat-value" style="color:#3498db">🔵 <span id="stat-tanques">0</span></div><div class="stat-label">Tanques</div></div>
        <div><div class="stat-value" style="color:#000">⚫ <span id="stat-offline">0</span></div><div class="stat-label">Offline</div></div>
        <div><div class="stat-value" style="color:#27ae60">✅ <span id="stat-online">0</span></div><div class="stat-label">Online</div></div>
        <div><div class="stat-value">🕐 <span id="stat-time">--:--</span></div><div class="stat-label">Actualizado</div></div>
    </div>

    <script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"></script>
    <script>
        const DATOS_INICIALES = {datos_json};
        let map = null;
        let markers = new Map();
        let primeraCarga = true;
        
        function initMap() {{
            map = L.map('map', {{
                zoomControl: true,
                scrollWheelZoom: true,
                dragging: true
            }});
            
            L.tileLayer('https://{{s}}.basemaps.cartocdn.com/light_all/{{z}}/{{x}}/{{y}}{{r}}.png', {{
                attribution: '',
                subdomains: 'abcd',
                maxZoom: 19
            }}).addTo(map);
            
            actualizarMapa(DATOS_INICIALES);
            actualizarEstadisticas(DATOS_INICIALES);
            document.getElementById('stat-time').textContent = new Date().toLocaleTimeString('es-ES', {{ hour: '2-digit', minute: '2-digit' }});
        }}
        
        function actualizarMapa(datos) {{
            if (!datos || !datos.estaciones) return;
            const nuevasBounds = [];
            
            datos.estaciones.forEach(estacion => {{
                if (!estacion.latitud || !estacion.longitud) return;
                const id = estacion.nombre || `${{estacion.latitud}},${{estacion.longitud}}`;
                const lat = parseFloat(estacion.latitud);
                const lng = parseFloat(estacion.longitud);
                nuevasBounds.push([lat, lng]);
                
                if (markers.has(id)) {{
                    const marker = markers.get(id);
                    marker.setPopupContent(crearPopupContent(estacion));
                    marker.setIcon(crearIcono(estacion.tipo, estacion.estado_bomba, estacion.en_linea));
                }} else {{
                    const marker = L.marker([lat, lng], {{ 
                        icon: crearIcono(estacion.tipo, estacion.estado_bomba, estacion.en_linea)
                    }})
                    .bindPopup(crearPopupContent(estacion), {{ maxWidth: 320 }})
                    .bindTooltip(estacion.nombre || 'Estación', {{ 
                        permanent: false, 
                        direction: 'top',
                        opacity: 0.9
                    }})
                    .addTo(map);
                    markers.set(id, marker);
                }}
            }});
            
            if (primeraCarga && nuevasBounds.length > 0) {{
                map.fitBounds(nuevasBounds, {{ padding: [40, 40] }});
                primeraCarga = false;
            }}
        }}
        
        function crearIcono(tipo, estado, enLinea) {{
            let color = '#000000';
            if (enLinea !== 0) {{
                if (tipo === 'pozo' || tipo === 'bomba') {{
                    color = estado === 1 ? '#27ae60' : '#e74c3c';
                }} else if (tipo === 'tanque') {{
                    color = estado === 1 ? '#3498db' : '#95a5a6';
                }} else if (tipo === 'sensor') {{
                    color = '#9b59b6';
                }} else {{
                    color = '#f39c12';
                }}
            }}
            
            let iconClass = 'fa-tint';
            if (tipo === 'tanque') iconClass = 'fa-water';
            else if (tipo === 'bomba') iconClass = 'fa-cog';
            else if (tipo === 'sensor') iconClass = 'fa-microchip';
            
            return L.divIcon({{
                html: `<div style="background:${{color}};width:32px;height:32px;border-radius:50%;display:flex;align-items:center;justify-content:center;box-shadow:0 2px 6px rgba(0,0,0,0.4);"><i class="fa ${{iconClass}}" style="color:white;font-size:16px;"></i></div>`,
                className: '',
                iconSize: [32, 32],
                iconAnchor: [16, 16],
                popupAnchor: [0, -16]
            }});
        }}
        
        function crearPopupContent(estacion) {{
            let html = `<div class="custom-popup"><h4>${{estacion.nombre || 'Estación'}}</h4><hr>`;
            
            const enLinea = estacion.en_linea !== undefined ? parseInt(estacion.en_linea) : 1;
            const estadoLinea = enLinea === 1 ? '<span class="status-online">En línea</span>' : '<span class="status-offline">Fuera de línea</span>';
            html += `<div class="var-row"><span class="var-label">Estado conexión:</span><span class="var-value">${{estadoLinea}}</span></div>`;
            
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
        
        function actualizarEstadisticas(datos) {{
            if (!datos || !datos.estaciones) return;
            
            let total = 0;
            let pozos_encendidos = 0;
            let pozos_apagados = 0;
            let tanques = 0;
            let offline = 0;
            let online = 0;
            
            datos.estaciones.forEach(estacion => {{
                total++;
                const enLinea = estacion.en_linea !== undefined ? parseInt(estacion.en_linea) : 1;
                const tipo = estacion.tipo || 'otro';
                const estado = estacion.estado_bomba !== undefined ? parseInt(estacion.estado_bomba) : (estacion.estado !== undefined ? parseInt(estacion.estado) : 0);
                
                if (enLinea === 0) {{
                    offline++;
                }} else {{
                    online++;
                    if (tipo === 'pozo') {{
                        if (estado === 1) {{
                            pozos_encendidos++;
                        }} else {{
                            pozos_apagados++;
                        }}
                    }} else if (tipo === 'tanque') {{
                        tanques++;
                    }}
                }}
            }});
            
            document.getElementById('stat-total').textContent = total;
            document.getElementById('stat-encendidos').textContent = pozos_encendidos;
            document.getElementById('stat-apagados').textContent = pozos_apagados;
            document.getElementById('stat-tanques').textContent = tanques;
            document.getElementById('stat-offline').textContent = offline;
            document.getElementById('stat-online').textContent = online;
        }}
        
        document.addEventListener('DOMContentLoaded', initMap);
    </script>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
</body>
</html>
"""

st.components.v1.html(
    html_completo,
    width=1920,
    height=1080,
    scrolling=False
)
