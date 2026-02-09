# # import streamlit as st
# # import requests
# # import json
# # from datetime import datetime
# # from streamlit_autorefresh import st_autorefresh

# # # Configuración minimalista
# # st.set_page_config(
# #     page_title="SCADA Monitor",
# #     layout="wide",
# #     initial_sidebar_state="collapsed"
# # )

# # # CSS para ocultar elementos de Streamlit
# # st.markdown("""
# #     <style>
# #     [data-testid="stSidebar"] { display: none; }
# #     [data-testid="stHeader"] { display: none; }
# #     .block-container { padding: 0; max-width: 100%; margin: 0; }
# #     .stApp { background-color: #0e1117; }
# #     footer, .stDeployButton { display: none !important; }
# #     </style>
# #     """, unsafe_allow_html=True)

# # # ==============================
# # # CARGAR DATOS DESDE GITHUB (Python - SIN CORS)
# # # ==============================
# # def cargar_datos_github():
# #     try:
# #         # URL CORRECTA sin espacios
# #         url = "https://raw.githubusercontent.com/AlarmasCiateq/SCADA_T/main/datos_estaciones.json"
        
# #         # Forzar carga fresca (sin cache)
# #         response = requests.get(
# #             url + f"?t={int(datetime.now().timestamp() * 1000)}",
# #             timeout=10,
# #             headers={'Cache-Control': 'no-cache'}
# #         )
# #         response.raise_for_status()
# #         return response.json()
# #     except Exception as e:
# #         st.error(f"Error al cargar datos: {str(e)[:50]}")
# #         return None

# # # ==============================
# # # AUTO-REFRESH (5 segundos para pruebas)
# # # ==============================
# # # ⚠️ CAMBIA A 300000 PARA PRODUCCIÓN (5 minutos)
# # st_autorefresh(interval=5000, key="auto_refresh")

# # # ==============================
# # # CARGAR DATOS
# # # ==============================
# # datos = cargar_datos_github()
# # if not datos:
# #     st.error("⚠️ No se pudieron cargar los datos de GitHub")
# #     st.stop()

# # # ==============================
# # # GENERAR HTML+JS CON DATOS EMBEBIDOS
# # # ==============================
# # # Convertir datos a JSON string para embeber en JavaScript
# # datos_json = json.dumps(datos)

# # html_completo = f"""
# # <!DOCTYPE html>
# # <html lang="es">
# # <head>
# #     <meta charset="UTF-8">
# #     <meta name="viewport" content="width=device-width, initial-scale=1.0">
# #     <title>SCADA Monitor</title>
# #     <link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css" />
# #     <style>
# #         * {{ margin: 0; padding: 0; box-sizing: border-box; }}
# #         body {{ font-family: Arial, sans-serif; background: #0e1117; overflow: hidden; }}
# #         #map {{ position: absolute; top: 0; left: 0; width: 100%; height: 100%; z-index: 1; }}
        
# #         /* Estadísticas flotantes */
# #         #stats-bar {{
# #             position: fixed;
# #             top: 10px;
# #             right: 15px;
# #             background: rgba(255, 255, 255, 0.95);
# #             padding: 8px 15px;
# #             border-radius: 8px;
# #             box-shadow: 0 2px 10px rgba(0,0,0,0.15);
# #             z-index: 1000;
# #             display: grid;
# #             grid-template-columns: repeat(6, auto);
# #             gap: 12px;
# #             align-items: center;
# #             font-family: Arial, sans-serif;
# #             font-size: 13px;
# #         }}
# #         .stat-value {{ font-weight: bold; color: #2c3e50; font-size: 16px; }}
# #         .stat-label {{ font-size: 9px; color: #7f8c8d; }}
# #         .custom-popup {{ font-family: Arial; padding: 12px; min-width: 280px; background: white; border-radius: 6px; }}
# #         .custom-popup h4 {{ margin: 0 0 10px 0; color: #2c3e50; font-size: 16px; }}
# #         .custom-popup hr {{ margin: 8px 0; border-color: #ecf0f1; }}
# #         .custom-popup .var-row {{ margin: 6px 0; padding: 4px 0; display: flex; justify-content: space-between; font-size: 13px; }}
# #         .custom-popup .var-label {{ color: #7f8c8d; }}
# #         .custom-popup .var-value {{ font-weight: bold; color: #2c3e50; }}
# #         .custom-popup .timestamp {{ font-size: 11px; color: #95a5a6; text-align: center; margin-top: 8px; }}
# #     </style>
# # </head>
# # <body>
# #     <div id="map"></div>
# #     <div id="stats-bar">
# #         <div><div class="stat-value">📡 <span id="stat-total">0</span></div><div class="stat-label">Total</div></div>
# #         <div><div class="stat-value" style="color:#27ae60">🟢 <span id="stat-activos">0</span></div><div class="stat-label">Activos</div></div>
# #         <div><div class="stat-value" style="color:#e74c3c">🔴 <span id="stat-inactivos">0</span></div><div class="stat-label">Inactivos</div></div>
# #         <div><div class="stat-value" style="color:#3498db">🔵 <span id="stat-tanques">0</span></div><div class="stat-label">Tanques</div></div>
# #         <div><div class="stat-value" style="color:#000">⚫ <span id="stat-offline">0</span></div><div class="stat-label">Offline</div></div>
# #         <div><div class="stat-value">🕐 <span id="stat-time">--:--</span></div><div class="stat-label">Actualizado</div></div>
# #     </div>

# #     <script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"></script>
# #     <script>
# #         // ════════════════════════════════════════════════════════════════
# #         // DATOS CARGADOS DESDE PYTHON (embebidos en el HTML)
# #         // ════════════════════════════════════════════════════════════════
# #         const DATOS_INICIALES = {datos_json};
        
# #         // ════════════════════════════════════════════════════════════════
        
# #         let map = null;
# #         let markers = new Map(); // id -> marker
# #         let primeraCarga = true;
        
# #         // Inicializar mapa
# #         function initMap() {{
# #             map = L.map('map', {{
# #                 zoomControl: true,
# #                 scrollWheelZoom: true,
# #                 dragging: true
# #             }});
            
# #             // Mapa claro con calles sutiles
# #             L.tileLayer('https://{{s}}.basemaps.cartocdn.com/light_all/{{z}}/{{x}}/{{y}}{{r}}.png', {{
# #                 attribution: '',
# #                 subdomains: 'abcd',
# #                 maxZoom: 19
# #             }}).addTo(map);
            
# #             // Cargar datos iniciales
# #             actualizarMapa(DATOS_INICIALES);
# #             actualizarEstadisticas(DATOS_INICIALES);
            
# #             // Actualizar timestamp
# #             document.getElementById('stat-time').textContent = new Date().toLocaleTimeString('es-ES', {{ 
# #                 hour: '2-digit', 
# #                 minute: '2-digit' 
# #             }});
# #         }}
        
# #         // Actualizar mapa (solo valores y colores, no posiciones)
# #         function actualizarMapa(datos) {{
# #             if (!datos || !datos.estaciones) return;
            
# #             const nuevasBounds = [];
            
# #             datos.estaciones.forEach(estacion => {{
# #                 if (!estacion.latitud || !estacion.longitud) return;
                
# #                 const id = estacion.nombre || `${{estacion.latitud}},${{estacion.longitud}}`;
# #                 const lat = parseFloat(estacion.latitud);
# #                 const lng = parseFloat(estacion.longitud);
                
# #                 nuevasBounds.push([lat, lng]);
                
# #                 // Si ya existe el marcador, actualizar popup y color
# #                 if (markers.has(id)) {{
# #                     const marker = markers.get(id);
                    
# #                     // Actualizar popup
# #                     const popupContent = crearPopupContent(estacion);
# #                     marker.setPopupContent(popupContent);
                    
# #                     // Actualizar color si cambió estado
# #                     const nuevoIcono = crearIcono(estacion.tipo, estacion.estado_bomba, estacion.en_linea);
# #                     marker.setIcon(nuevoIcono);
                    
# #                 }} else {{
# #                     // Crear nuevo marcador
# #                     const icono = crearIcono(estacion.tipo, estacion.estado_bomba, estacion.en_linea);
# #                     const popupContent = crearPopupContent(estacion);
                    
# #                     const marker = L.marker([lat, lng], {{ icon: icono }})
# #                         .bindPopup(popupContent, {{ maxWidth: 320 }})
# #                         .addTo(map);
                    
# #                     markers.set(id, marker);
# #                 }}
# #             }});
            
# #             // Ajustar bounds SOLO en primera carga
# #             if (primeraCarga && nuevasBounds.length > 0) {{
# #                 const bounds = L.latLngBounds(nuevasBounds);
# #                 map.fitBounds(bounds, {{ padding: [40, 40] }});
# #                 primeraCarga = false;
# #                 console.log('✓ Zoom inicial ajustado');
# #             }}
# #         }}
        
# #         // Crear icono según tipo y estado
# #         function crearIcono(tipo, estado, enLinea) {{
# #             // Determinar color
# #             let color = '#000000'; // negro por defecto (offline)
# #             if (enLinea !== 0) {{
# #                 if (tipo === 'pozo' || tipo === 'bomba') {{
# #                     color = estado === 1 ? '#27ae60' : '#e74c3c'; // verde/rojo
# #                 }} else if (tipo === 'tanque') {{
# #                     color = estado === 1 ? '#3498db' : '#95a5a6'; // azul/gris
# #                 }} else if (tipo === 'sensor') {{
# #                     color = '#9b59b6'; // morado
# #                 }} else {{
# #                     color = '#f39c12'; // naranja
# #                 }}
# #             }}
            
# #             // Determinar ícono (siempre el mismo según tipo)
# #             let iconClass = 'fa-tint'; // pozo por defecto
# #             if (tipo === 'tanque') iconClass = 'fa-water';
# #             else if (tipo === 'bomba') iconClass = 'fa-cog';
# #             else if (tipo === 'sensor') iconClass = 'fa-microchip';
            
# #             return L.divIcon({{
# #                 html: `<div style="
# #                     background: ${{color}};
# #                     width: 32px;
# #                     height: 32px;
# #                     border-radius: 50%;
# #                     display: flex;
# #                     align-items: center;
# #                     justify-content: center;
# #                     box-shadow: 0 2px 6px rgba(0,0,0,0.4);
# #                 ">
# #                     <i class="fa ${{iconClass}}" style="color: white; font-size: 16px;"></i>
# #                 </div>`,
# #                 className: '',
# #                 iconSize: [32, 32],
# #                 iconAnchor: [16, 16],
# #                 popupAnchor: [0, -16]
# #             }});
# #         }}
        
# #         // Crear contenido del popup
# #         function crearPopupContent(estacion) {{
# #             let html = `<div class="custom-popup"><h4>${{estacion.nombre || 'Estación'}}</h4><hr>`;
            
# #             for (const key in estacion) {{
# #                 if (!['nombre', 'latitud', 'longitud', 'tipo', 'estado_bomba', 'en_linea', 'icono'].includes(key)) {{
# #                     const value = typeof estacion[key] === 'number' 
# #                         ? estacion[key].toLocaleString('es-ES', {{ minimumFractionDigits: 2, maximumFractionDigits: 2 }})
# #                         : estacion[key];
                    
# #                     html += `<div class="var-row"><span class="var-label">${{key}}:</span><span class="var-value">${{value}}</span></div>`;
# #                 }}
# #             }}
            
# #             html += `<hr><div class="timestamp">📅 ${{new Date().toLocaleString('es-ES')}}</div></div>`;
# #             return html;
# #         }}
        
# #         // Actualizar estadísticas
# #         function actualizarEstadisticas(datos) {{
# #             if (!datos || !datos.estaciones) return;
            
# #             const stats = {{ total:0, activos:0, inactivos:0, tanques:0, offline:0 }};
            
# #             datos.estaciones.forEach(estacion => {{
# #                 stats.total++;
# #                 const enLinea = estacion.en_linea || 1;
# #                 const tipo = estacion.tipo || 'otro';
# #                 const estado = estacion.estado_bomba || estacion.estado || 0;
                
# #                 if (enLinea === 0) stats.offline++;
# #                 else if (tipo === 'pozo') {{
# #                     if (estado === 1) stats.activos++;
# #                     else stats.inactivos++;
# #                 }} else if (tipo === 'tanque') stats.tanques++;
# #             }});
            
# #             document.getElementById('stat-total').textContent = stats.total;
# #             document.getElementById('stat-activos').textContent = stats.activos;
# #             document.getElementById('stat-inactivos').textContent = stats.inactivos;
# #             document.getElementById('stat-tanques').textContent = stats.tanques;
# #             document.getElementById('stat-offline').textContent = stats.offline;
# #         }}
        
# #         // Iniciar cuando el DOM esté listo
# #         document.addEventListener('DOMContentLoaded', initMap);
# #     </script>
    
# #     <!-- Font Awesome para íconos -->
# #     <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
# # </body>
# # </html>
# # """

# # # Mostrar el HTML+JS en Streamlit (se ejecutará en el navegador)
# # st.components.v1.html(
# #     html_completo,
# #     width=1920,
# #     height=1080,
# #     scrolling=False
# # )
# # import streamlit as st
# # import requests
# # import json
# # import base64
# # from datetime import datetime
# # from streamlit_autorefresh import st_autorefresh
# # import time

# # # Configuración minimalista - SIN TÍTULO NI DECORACIONES
# # st.set_page_config(
# #     page_title="SCADA Monitor",
# #     layout="wide",
# #     initial_sidebar_state="collapsed"
# # )

# # # CSS AGRESIVO para eliminar TODO (header, título, scroll, barras)
# # st.markdown("""
# #     <style>
# #     /* Eliminar TODO */
# #     [data-testid="stSidebar"] { display: none !important; }
# #     [data-testid="stHeader"] { display: none !important; }
# #     [data-testid="stDecoration"] { display: none !important; }
# #     header { display: none !important; }
# #     #MainMenu { display: none !important; }
# #     footer { display: none !important; }
# #     .stApp { 
# #         background-color: #0e1117; 
# #         padding: 0 !important; 
# #         margin: 0 !important; 
# #         overflow: hidden !important;
# #     }
# #     .block-container { 
# #         padding: 0 !important; 
# #         max-width: 100% !important; 
# #         margin: 0 !important; 
# #         overflow: hidden !important;
# #     }
# #     .main { 
# #         padding: 0 !important; 
# #         margin: 0 !important; 
# #         overflow: hidden !important;
# #     }
# #     .block-container > div { 
# #         padding: 0 !important; 
# #         margin: 0 !important; 
# #     }
# #     /* Ocultar cualquier scroll */
# #     ::-webkit-scrollbar { display: none !important; }
# #     body { overflow: hidden !important; }
# #     </style>
# #     """, unsafe_allow_html=True)

# # # ==============================
# # # CARGAR DATOS CON REINTENTOS SILENCIOSOS (usa datos anteriores si falla)
# # # ==============================
# # def cargar_datos_github(datos_anteriores=None, max_intentos=3):
# #     for intento in range(max_intentos):
# #         try:
# #             GITHUB_USER = "AlarmasCiateq"
# #             REPO_NAME = "SCADA_T"
# #             BRANCH = "main"
# #             FILE_PATH = "datos_estaciones.json"
            
# #             api_url = f"https://api.github.com/repos/{GITHUB_USER}/{REPO_NAME}/contents/{FILE_PATH}?ref={BRANCH}"
            
# #             headers = {
# #                 'User-Agent': f'SCADA-Monitor-{datetime.now().timestamp()}',
# #                 'Accept': 'application/vnd.github.v3+json'
# #             }
            
# #             response = requests.get(api_url, headers=headers, timeout=10)
# #             response.raise_for_status()
            
# #             data = response.json()
# #             content_bytes = base64.b64decode(data['content'])
# #             content_str = content_bytes.decode('utf-8')
# #             datos = json.loads(content_str)
            
# #             return datos  # Éxito: devuelve nuevos datos
            
# #         except Exception:
# #             if intento < max_intentos - 1:
# #                 time.sleep(1)  # Espera 1 segundo y reintenta
# #                 continue
    
# #     # Falló todo: devuelve datos anteriores si existen, sino None
# #     return datos_anteriores if datos_anteriores else None

# # # ==============================
# # # AUTO-REFRESH (5 segundos para pruebas)
# # # ==============================
# # st_autorefresh(interval=60000, key="auto_refresh")

# # # ==============================
# # # CARGAR DATOS (usa cache en session_state para mantener estado anterior)
# # # ==============================
# # if 'datos_cache' not in st.session_state:
# #     st.session_state.datos_cache = None

# # # Intentar cargar nuevos datos (con reintentos silenciosos)
# # nuevos_datos = cargar_datos_github(st.session_state.datos_cache)

# # # Si hay nuevos datos válidos, actualizar cache
# # if nuevos_datos:
# #     st.session_state.datos_cache = nuevos_datos

# # # Usar datos del cache (pueden ser nuevos o anteriores si falló la carga)
# # datos = st.session_state.datos_cache

# # # Si NO hay datos en absoluto (primera carga fallida), mostrar mínimo
# # if not datos:
# #     st.markdown("""
# #         <div style="position:fixed;top:0;left:0;width:100%;height:100%;background:#0e1117;color:white;
# #                     display:flex;justify-content:center;align-items:center;font-family:Arial;">
# #             <div style="text-align:center;padding:20px;">
# #                 <h2>🛢️ SCADA Monitor</h2>
# #                 <p>Esperando primera conexión con el sistema...</p>
# #             </div>
# #         </div>
# #         """, unsafe_allow_html=True)
# #     st.stop()

# # # ==============================
# # # GENERAR HTML+JS (tooltip simple + popup completo)
# # # ==============================
# # datos_json = json.dumps(datos)

# # html_completo = f"""
# # <!DOCTYPE html>
# # <html lang="es">
# # <head>
# #     <meta charset="UTF-8">
# #     <meta name="viewport" content="width=device-width, initial-scale=1.0">
# #     <title>SCADA Monitor</title>
# #     <link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css" />
# #     <style>
# #         * {{ margin: 0; padding: 0; box-sizing: border-box; }}
# #         body {{ 
# #             font-family: Arial, sans-serif; 
# #             background: #0e1117; 
# #             overflow: hidden; 
# #             height: 100vh;
# #             width: 100vw;
# #         }}
# #         #map {{ 
# #             position: absolute; 
# #             top: 0; 
# #             left: 0; 
# #             width: 100%; 
# #             height: 100%; 
# #             z-index: 1; 
# #         }}
# #         #stats-bar {{
# #             position: fixed;
# #             top: 10px;
# #             right: 15px;
# #             background: rgba(255, 255, 255, 0.95);
# #             padding: 6px 10px;
# #             border-radius: 6px;
# #             box-shadow: 0 2px 8px rgba(0,0,0,0.15);
# #             z-index: 1000;
# #             display: grid;
# #             grid-template-columns: repeat(7, auto);
# #             gap: 8px;
# #             align-items: center;
# #             font-family: Arial, sans-serif;
# #             font-size: 11px;
# #         }}
# #         .stat-value {{ font-weight: bold; color: #2c3e50; font-size: 14px; }}
# #         .stat-label {{ font-size: 7px; color: #7f8c8d; white-space: nowrap; }}
# #         .custom-popup {{ font-family: Arial; padding: 12px; min-width: 280px; background: white; border-radius: 6px; }}
# #         .custom-popup h4 {{ margin: 0 0 10px 0; color: #2c3e50; font-size: 16px; }}
# #         .custom-popup hr {{ margin: 8px 0; border-color: #ecf0f1; }}
# #         .custom-popup .var-row {{ margin: 6px 0; padding: 4px 0; display: flex; justify-content: space-between; font-size: 13px; }}
# #         .custom-popup .var-label {{ color: #7f8c8d; }}
# #         .custom-popup .var-value {{ font-weight: bold; color: #2c3e50; }}
# #         .custom-popup .timestamp {{ font-size: 11px; color: #95a5a6; text-align: center; margin-top: 8px; }}
# #     </style>
# # </head>
# # <body>
# #     <div id="map"></div>
# #     <div id="stats-bar">
# #         <div><div class="stat-value">📡 <span id="stat-total">0</span></div><div class="stat-label">Total</div></div>
# #         <div><div class="stat-value" style="color:#27ae60">🟢 <span id="stat-encendidos">0</span></div><div class="stat-label">Pozos Encendidos</div></div>
# #         <div><div class="stat-value" style="color:#e74c3c">🔴 <span id="stat-apagados">0</span></div><div class="stat-label">Pozos Apagados</div></div>
# #         <div><div class="stat-value" style="color:#3498db">🔵 <span id="stat-tanques">0</span></div><div class="stat-label">Tanques</div></div>
# #         <div><div class="stat-value" style="color:#000">⚫ </div></div>
# #         <div><div class="stat-value">🕐 <span id="stat-time">--:--</span></div><div class="stat-label">Actualizado</div></div>
# #     </div>

# #     <script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"></script>
# #     <script>
# #         const DATOS_INICIALES = {datos_json};
# #         let map = null;
# #         let markers = new Map();
# #         let primeraCarga = true;
        
# #         function initMap() {{
# #             map = L.map('map', {{
# #                 zoomControl: true,
# #                 scrollWheelZoom: true,
# #                 dragging: true
# #             }});
            
# #             L.tileLayer('https://{{s}}.basemaps.cartocdn.com/light_all/{{z}}/{{x}}/{{y}}{{r}}.png', {{
# #                 attribution: '',
# #                 subdomains: 'abcd',
# #                 maxZoom: 19
# #             }}).addTo(map);
            
# #             actualizarMapa(DATOS_INICIALES);
# #             actualizarEstadisticas(DATOS_INICIALES);
# #             document.getElementById('stat-time').textContent = new Date().toLocaleTimeString('es-ES', {{ hour: '2-digit', minute: '2-digit' }});
# #         }}
        
# #         function actualizarMapa(datos) {{
# #             if (!datos || !datos.estaciones) return;
# #             const nuevasBounds = [];
            
# #             datos.estaciones.forEach(estacion => {{
# #                 if (!estacion.latitud || !estacion.longitud) return;
# #                 const id = estacion.nombre || `${{estacion.latitud}},${{estacion.longitud}}`;
# #                 const lat = parseFloat(estacion.latitud);
# #                 const lng = parseFloat(estacion.longitud);
# #                 nuevasBounds.push([lat, lng]);
                
# #                 if (markers.has(id)) {{
# #                     const marker = markers.get(id);
# #                     marker.setPopupContent(crearPopupContent(estacion));
# #                     marker.setIcon(crearIcono(estacion.tipo, estacion.estado_bomba, estacion.en_linea));
# #                 }} else {{
# #                     const marker = L.marker([lat, lng], {{ 
# #                         icon: crearIcono(estacion.tipo, estacion.estado_bomba, estacion.en_linea)
# #                     }})
# #                     .bindPopup(crearPopupContent(estacion), {{ maxWidth: 320 }})
# #                     .bindTooltip(estacion.nombre || 'Estación', {{ 
# #                         permanent: false, 
# #                         direction: 'top',
# #                         opacity: 0.9
# #                     }})
# #                     .addTo(map);
# #                     markers.set(id, marker);
# #                 }}
# #             }});
            
# #             if (primeraCarga && nuevasBounds.length > 0) {{
# #                 map.fitBounds(nuevasBounds, {{ padding: [40, 40] }});
# #                 primeraCarga = false;
# #             }}
# #         }}
        
# #         function crearIcono(tipo, estado, enLinea) {{
# #             let color = '#000000';
# #             if (enLinea !== 0) {{
# #                 if (tipo === 'pozo' || tipo === 'bomba') {{
# #                     color = estado === 1 ? '#27ae60' : '#e74c3c';
# #                 }} else if (tipo === 'tanque') {{
# #                     color = estado === 1 ? '#3498db' : '#95a5a6';
# #                 }} else if (tipo === 'sensor') {{
# #                     color = '#9b59b6';
# #                 }} else {{
# #                     color = '#f39c12';
# #                 }}
# #             }}
            
# #             let iconClass = 'fa-tint';
# #             if (tipo === 'tanque') iconClass = 'fa-water';
# #             else if (tipo === 'bomba') iconClass = 'fa-cog';
# #             else if (tipo === 'sensor') iconClass = 'fa-microchip';
            
# #             return L.divIcon({{
# #                 html: `<div style="background:${{color}};width:32px;height:32px;border-radius:50%;display:flex;align-items:center;justify-content:center;box-shadow:0 2px 6px rgba(0,0,0,0.4);"><i class="fa ${{iconClass}}" style="color:white;font-size:16px;"></i></div>`,
# #                 className: '',
# #                 iconSize: [32, 32],
# #                 iconAnchor: [16, 16],
# #                 popupAnchor: [0, -16]
# #             }});
# #         }}
        
# #         function crearPopupContent(estacion) {{
# #             let html = `<div class="custom-popup"><h4>${{estacion.nombre || 'Estación'}}</h4><hr>`;
# #             for (const key in estacion) {{
# #                 if (!['nombre', 'latitud', 'longitud', 'tipo', 'estado_bomba', 'en_linea', 'icono'].includes(key)) {{
# #                     const value = typeof estacion[key] === 'number' ? estacion[key].toLocaleString('es-ES', {{ minimumFractionDigits: 2, maximumFractionDigits: 2 }}) : estacion[key];
# #                     html += `<div class="var-row"><span class="var-label">${{key}}:</span><span class="var-value">${{value}}</span></div>`;
# #                 }}
# #             }}
# #             html += `<hr><div class="timestamp">📅 ${{new Date().toLocaleString('es-ES')}}</div></div>`;
# #             return html;
# #         }}
        
# #         function actualizarEstadisticas(datos) {{
# #             if (!datos || !datos.estaciones) return;
# #             const stats = {{ total:0, pozos_encendidos:0, pozos_apagados:0, tanques:0, offline:0, online:0 }};
            
# #             datos.estaciones.forEach(estacion => {{
# #                 stats.total++;
# #                 const enLinea = estacion.en_linea || 1;
# #                 const tipo = estacion.tipo || 'otro';
# #                 const estado = estacion.estado_bomba || estacion.estado || 0;
                
# #                 if (enLinea === 0) stats.offline++;
# #                 else stats.online++;
                
# #                 if (tipo === 'pozo' && enLinea === 1) {{
# #                     if (estado === 1) stats.pozos_encendidos++;
# #                     else stats.pozos_apagados++;
# #                 }} else if (tipo === 'tanque') stats.tanques++;
# #             }});
            
# #             document.getElementById('stat-total').textContent = stats.total;
# #             document.getElementById('stat-encendidos').textContent = stats.pozos_encendidos;
# #             document.getElementById('stat-apagados').textContent = stats.pozos_apagados;
# #             document.getElementById('stat-tanques').textContent = stats.tanques;
# #             document.getElementById('stat-offline').textContent = stats.offline;
# #             document.getElementById('stat-online').textContent = stats.online;
# #         }}
        
# #         document.addEventListener('DOMContentLoaded', initMap);
# #     </script>
# #     <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
# # </body>
# # </html>
# # """

# # # Mostrar mapa ocupando TODO el espacio (sin scroll)
# # st.components.v1.html(
# #     html_completo,
# #     width=1920,
# #     height=1080,
# #     scrolling=False
# # )

# import streamlit as st
# import requests
# import json
# import base64
# from datetime import datetime
# from streamlit_autorefresh import st_autorefresh
# import time
# import os

# # Configuración minimalista
# st.set_page_config(
#     page_title="🌎 SCADA Monitor",
#     layout="wide",
#     initial_sidebar_state="collapsed"
# )

# # CSS AGRESIVO para eliminar TODO
# st.markdown("""
#     <style>
#     [data-testid="stSidebar"] { display: none !important; }
#     [data-testid="stHeader"] { display: none !important; }
#     [data-testid="stDecoration"] { display: none !important; }
#     header { display: none !important; }
#     #MainMenu { display: none !important; }
#     footer { display: none !important; }
#     .stApp { background-color: #0e1117; padding: 0 !important; margin: 0 !important; overflow: hidden !important; }
#     .block-container { padding: 0 !important; max-width: 100% !important; margin: 0 !important; overflow: hidden !important; }
#     .main { padding: 0 !important; margin: 0 !important; overflow: hidden !important; }
#     .block-container > div { padding: 0 !important; margin: 0 !important; }
#     ::-webkit-scrollbar { display: none !important; }
#     body { overflow: hidden !important; }
#     </style>
#     """, unsafe_allow_html=True)

# # ==============================
# # OBTENER TOKEN DE GITHUB (Streamlit Secrets o Environment Variable)
# # ==============================
# def obtener_token_github():
#     """Obtiene el token de GitHub de Streamlit Secrets o variable de entorno"""
#     try:
#         # Intentar desde Streamlit Secrets (recomendado para producción)
#         if hasattr(st, 'secrets') and "GITHUB_TOKEN" in st.secrets:
#             return st.secrets["GITHUB_TOKEN"]
#     except:
#         pass
    
#     # Intentar desde variable de entorno (para desarrollo local)
#     return os.getenv("GITHUB_TOKEN", None)

# # ==============================
# # CARGAR DATOS CON TOKEN Y REINTENTOS SILENCIOSOS
# # ==============================
# def cargar_datos_github(datos_anteriores=None, max_intentos=3):
#     token = obtener_token_github()
    
#     for intento in range(max_intentos):
#         try:
#             GITHUB_USER = "AlarmasCiateq"
#             REPO_NAME = "SCADA_T"
#             BRANCH = "main"
#             FILE_PATH = "datos_estaciones.json"
            
#             api_url = f"https://api.github.com/repos/{GITHUB_USER}/{REPO_NAME}/contents/{FILE_PATH}?ref={BRANCH}"
            
#             # Headers con token si está disponible
#             headers = {
#                 'User-Agent': f'SCADA-Monitor-{datetime.now().timestamp()}',
#                 'Accept': 'application/vnd.github.v3+json'
#             }
            
#             # Agregar token si existe (aumenta límite a 5000 solicitudes/hora)
#             if token:
#                 headers['Authorization'] = f'token {token}'
            
#             response = requests.get(api_url, headers=headers, timeout=10)
#             response.raise_for_status()
            
#             data = response.json()
#             content_bytes = base64.b64decode(data['content'])
#             content_str = content_bytes.decode('utf-8')
#             datos = json.loads(content_str)
            
#             return datos
            
#         except requests.exceptions.HTTPError as e:
#             # Si es error 401 (token inválido) o 403 (rate limit sin token), no reintentar
#             if e.response.status_code in [401, 403]:
#                 # Si no hay token y es 403, es rate limit sin autenticación
#                 if not token and e.response.status_code == 403:
#                     st.warning("⚠️ Sin token de GitHub. Límite de 60 solicitudes/hora alcanzado. Usa un token para 5000 solicitudes/hora.")
#                 return datos_anteriores if datos_anteriores else None
#             # Para otros errores HTTP, reintentar
#             if intento < max_intentos - 1:
#                 time.sleep(1)
#                 continue
#             return datos_anteriores if datos_anteriores else None
#         except Exception:
#             if intento < max_intentos - 1:
#                 time.sleep(1)
#                 continue
#             return datos_anteriores if datos_anteriores else None
    
#     return datos_anteriores if datos_anteriores else None

# # ==============================
# # AUTO-REFRESH (5 segundos para pruebas)
# # ==============================
# st_autorefresh(interval=5000, key="auto_refresh")

# # ==============================
# # CARGAR DATOS
# # ==============================
# if 'datos_cache' not in st.session_state:
#     st.session_state.datos_cache = None

# nuevos_datos = cargar_datos_github(st.session_state.datos_cache)
# if nuevos_datos:
#     st.session_state.datos_cache = nuevos_datos

# datos = st.session_state.datos_cache
# if not datos:
#     st.markdown("""
#         <div style="position:fixed;top:0;left:0;width:100%;height:100%;background:#0e1117;color:white;
#                     display:flex;justify-content:center;align-items:center;font-family:Arial;">
#             <div style="text-align:center;padding:20px;">
#                 <h2>🛢️ SCADA Monitor</h2>
#                 <p>Esperando primera conexión...</p>
#                 <p style="font-size:12px;margin-top:10px;color:#7f8c8d">
#                     {% if not token %}⚠️ Sin token de GitHub - Límite de 60 solicitudes/hora{% endif %}
#                 </p>
#             </div>
#         </div>
#         """, unsafe_allow_html=True)
#     st.stop()

# # ==============================
# # GENERAR HTML+JS (mismo código corregido anterior)
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
#         body {{ font-family: Arial, sans-serif; background: #0e1117; overflow: hidden; height: 100vh; width: 100vw; }}
#         #map {{ position: absolute; top: 0; left: 0; width: 100%; height: 100%; z-index: 1; }}
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
#         .status-online {{ color: #27ae60; font-weight: bold; }}
#         .status-offline {{ color: #e74c3c; font-weight: bold; }}
#     </style>
# </head>
# <body>
#     <div id="map"></div>
#     <div id="stats-bar">
#         <div><div class="stat-value">📡 <span id="stat-total">0</span></div><div class="stat-label">Total Est.</div></div>
#         <div><div class="stat-value" style="color:#27ae60">🟢 <span id="stat-encendidos">0</span></div><div class="stat-label">Pzs Off</div></div>
#         <div><div class="stat-value" style="color:#e74c3c">🔴 <span id="stat-apagados">0</span></div><div class="stat-label">Pzs On</div></div>
#         <div><div class="stat-value" style="color:#3498db">🔵 <span id="stat-tanques">0</span></div><div class="stat-label">Tanques</div></div>
#         <div><div class="stat-value" style="color:#000">⚫ <span id="stat-offline">0</span></div><div class="stat-label">Offline</div></div>
#         <div><div class="stat-value" style="color:#27ae60">✅ <span id="stat-online">0</span></div><div class="stat-label">Online</div></div>
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
            
#             const enLinea = estacion.en_linea !== undefined ? parseInt(estacion.en_linea) : 1;
#             const estadoLinea = enLinea === 1 ? '<span class="status-online">En línea</span>' : '<span class="status-offline">Fuera de línea</span>';
#             html += `<div class="var-row"><span class="var-label">Estado conexión:</span><span class="var-value">${{estadoLinea}}</span></div>`;
            
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
        
#         function actualizarEstadisticas(datos) {{
#             if (!datos || !datos.estaciones) return;
            
#             let total = 0;
#             let pozos_encendidos = 0;
#             let pozos_apagados = 0;
#             let tanques = 0;
#             let offline = 0;
#             let online = 0;
            
#             datos.estaciones.forEach(estacion => {{
#                 total++;
#                 const enLinea = estacion.en_linea !== undefined ? parseInt(estacion.en_linea) : 1;
#                 const tipo = estacion.tipo || 'otro';
#                 const estado = estacion.estado_bomba !== undefined ? parseInt(estacion.estado_bomba) : (estacion.estado !== undefined ? parseInt(estacion.estado) : 0);
                
#                 if (enLinea === 0) {{
#                     offline++;
#                 }} else {{
#                     online++;
#                     if (tipo === 'pozo') {{
#                         if (estado === 1) {{
#                             pozos_encendidos++;
#                         }} else {{
#                             pozos_apagados++;
#                         }}
#                     }} else if (tipo === 'tanque') {{
#                         tanques++;
#                     }}
#                 }}
#             }});
            
#             document.getElementById('stat-total').textContent = total;
#             document.getElementById('stat-encendidos').textContent = pozos_encendidos;
#             document.getElementById('stat-apagados').textContent = pozos_apagados;
#             document.getElementById('stat-tanques').textContent = tanques;
#             document.getElementById('stat-offline').textContent = offline;
#             document.getElementById('stat-online').textContent = online;
#         }}
        
#         document.addEventListener('DOMContentLoaded', initMap);
#     </script>
#     <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
# </body>
# </html>
# """

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
    page_title="SCADA Monitor",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# CSS AGRESIVO - VALORES EN NEGRITA
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
    
    /* Popup con valores en NEGRITA */
    .custom-popup .var-label { 
        color: #2c3e50 !important; 
        font-weight: 600 !important; 
        font-size: 13px !important;
    }
    .custom-popup .var-value { 
        color: #2c3e50 !important; 
        font-weight: bold !important; 
        font-size: 14px !important;
        text-align: right !important;
    }
    
    /* Mensaje de error */
    .error-container {
        position: fixed;
        top: 50%;
        left: 50%;
        transform: translate(-50%, -50%);
        background: rgba(231, 76, 60, 0.95);
        color: white;
        padding: 30px;
        border-radius: 15px;
        box-shadow: 0 10px 40px rgba(0,0,0,0.5);
        max-width: 600px;
        text-align: center;
        z-index: 9999;
        border: 3px solid white;
    }
    .error-title { font-size: 28px; font-weight: bold; margin-bottom: 15px; }
    .error-message { font-size: 16px; margin-bottom: 20px; line-height: 1.5; }
    .error-fix { background: rgba(0,0,0,0.3); padding: 15px; border-radius: 8px; margin-top: 15px; font-family: monospace; font-size: 14px; text-align: left; }
    .error-footer { font-size: 12px; margin-top: 20px; opacity: 0.9; }
    </style>
    """, unsafe_allow_html=True)

# ==============================
# OBTENER TOKEN DE GITHUB
# ==============================
def obtener_token_github():
    try:
        if hasattr(st, 'secrets') and "GITHUB_TOKEN" in st.secrets:
            return st.secrets["GITHUB_TOKEN"]
    except:
        pass
    return os.getenv("GITHUB_TOKEN", None)

# ==============================
# CARGAR DATOS CON VALIDACIÓN DE JSON
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
            
            headers = {
                'User-Agent': f'SCADA-Monitor-{datetime.now().timestamp()}',
                'Accept': 'application/vnd.github.v3+json'
            }
            
            if token:
                headers['Authorization'] = f'token {token}'
            
            response = requests.get(api_url, headers=headers, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            content_bytes = base64.b64decode(data['content'])
            content_str = content_bytes.decode('utf-8')
            
            try:
                datos = json.loads(content_str)
                return datos
            except json.JSONDecodeError as e:
                st.markdown(f"""
                    <div class="error-container">
                        <div class="error-title">⚠️ ERROR EN ARCHIVO JSON</div>
                        <div class="error-message">
                            El archivo <strong>datos_estaciones.json</strong> tiene formato incorrecto.<br>
                            <strong>Línea {e.lineno}, Columna {e.colno}:</strong> {str(e.msg)[:50]}
                        </div>
                        <div class="error-fix">
<strong>Solución:</strong><br>
1. Corrige el JSON en GitHub<br>
2. Usa validador: <a href="https://jsonlint.com" target="_blank" style="color:#3498db;text-decoration:underline">jsonlint.com</a><br>
3. Verifica comas y comillas
                        </div>
                        <div class="error-footer">
                            ⏳ Reintentando en 10 segundos... | {datetime.now().strftime('%H:%M:%S')}
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                time.sleep(10)
                st.rerun()
                return datos_anteriores if datos_anteriores else None
                
        except requests.exceptions.HTTPError as e:
            if e.response.status_code in [401, 403]:
                return datos_anteriores if datos_anteriores else None
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
# AUTO-REFRESH
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
                <p>Conectando con el sistema...</p>
                <p style="font-size:12px;margin-top:10px;color:#7f8c8d">
                    Verificando datos en GitHub...
                </p>
            </div>
        </div>
        """, unsafe_allow_html=True)
    st.stop()

# ==============================
# GENERAR HTML+JS DEFINITIVO (OFFLINE = MISMO ICONO + FONDO NEGRO + BORDE ROJO)
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
        .custom-popup h4 {{ margin: 0 0 10px 0; color: #2c3e50; font-size: 16px; font-weight: bold; }}
        .custom-popup hr {{ margin: 8px 0; border-color: #ecf0f1; }}
        .custom-popup .var-row {{ margin: 6px 0; padding: 4px 0; display: flex; justify-content: space-between; }}
        .custom-popup .var-label {{ 
            color: #2c3e50; 
            font-weight: 600; 
            font-size: 13px; 
            min-width: 120px;
        }}
        .custom-popup .var-value {{ 
            color: #2c3e50; 
            font-weight: bold; 
            font-size: 14px; 
            text-align: right;
            min-width: 80px;
        }}
        .custom-popup .timestamp {{ font-size: 11px; color: #95a5a6; text-align: center; margin-top: 8px; }}
        .status-online {{ color: #27ae60; font-weight: bold; }}
        .status-offline {{ color: #e74c3c; font-weight: bold; }}
    </style>
</head>
<body>
    <div id="map"></div>
    <div id="stats-bar">
        <div><div class="stat-value">📡 <span id="stat-total">0</span></div><div class="stat-label">Total</div></div>
        <div><div class="stat-value" style="color:#27ae60">🟢 <span id="stat-encendidos">0</span></div><div class="stat-label">Pozos Encendidos</div></div>
        <div><div class="stat-value" style="color:#e74c3c">🔴 <span id="stat-apagados">0</span></div><div class="stat-label">Pozos Apagados</div></div>
        <div><div class="stat-value" style="color:#3498db">🔵 <span id="stat-tanques">0</span></div><div class="stat-label">Tanques</div></div>
        <div><div class="stat-value" style="color:#000">⚫ <span id="stat-offline">0</span></div><div class="stat-label">Offline</div></div>
        <div><div class="stat-value" style="color:#27ae60">🟢 <span id="stat-online">0</span></div><div class="stat-label">Online</div></div>
        <div><div class="stat-value">🕐 <span id="stat-time">--:--</span></div><div class="stat-label">Actualizado</div></div>
    </div>

    <script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"></script>
    <script>
        const DATOS_INICIALES = {datos_json};
        let map = null;
        let markers = new Map();
        let primeraCarga = true;
        
        // LIMPIAR URL
        function limpiarUrl(url) {{
            if (!url) return null;
            return url.trim().replace(/\\s+/g, '%20');
        }}
        
        // SVG predeterminados por tipo (sin cambios)
        function getDefaultSvg(tipo, color) {{
            switch(tipo) {{
                case 'pozo': return `<svg xmlns="http://www.w3.org/2000/svg" height="32" viewBox="0 -960 960 960" width="32" fill="${{color}}"><path d="M480-120q-108 0-196.5-54T132-300q-3-5-4.5-10t-1.5-11q0-12 7.5-23.5T160-364q8-8 18-11.5t21-3.5q11 0 21 3.5t18 11.5q5 5 8 10.5t5 12.5q0 11-6 21t-16 17q-56 44-94 102t-38 126q0 83 58.5 141.5T480-120Zm0-360q-33 0-56.5-23.5T400-560q0-33 23.5-56.5T480-640q33 0 56.5 23.5T560-560q0 33-23.5 56.5T480-480Z"/></svg>`;
                case 'tanque': return `<svg xmlns="http://www.w3.org/2000/svg" height="32" viewBox="0 -960 960 960" width="32" fill="${{color}}"><path d="M120-200v-560h160v-80h400v80h160v560H120Zm280-440Zm0 320q50 0 85-35t35-85q0-50-35-85t-85-35q-50 0-85 35t-35 85q0 50 35 85t85 35Zm0-160q21 0 35.5-14.5T480-440q0-21-14.5-35.5T430-490q-21 0-35.5 14.5T380-440q0 21 14.5 35.5T430-390Zm280 160v-80H600v80h110Zm0-160v-80H600v80h110Zm-440 160v-80H260v80h110Zm0-160v-80H260v80h110Z"/></svg>`;
                case 'bomba': return `<svg xmlns="http://www.w3.org/2000/svg" height="32" viewBox="0 -960 960 960" width="32" fill="${{color}}"><path d="M120-280h164q-17-17-31.5-37T227-360H120v80Zm360 0q83 0 141.5-58.5T680-480q0-83-58.5-141.5T480-680q-83 0-141.5 58.5T280-480q0 83 58.5 141.5T480-280Zm253-320h107v-80H676q17 17 31.5 37t25.5 43ZM40-160v-320h80v40h83q-2-10-2.5-19.5T200-480q0-117 81.5-198.5T480-760h360v-40h80v320h-80v-40h-83q2 10 2.5 19.5t.5 20.5q0 117-81.5 198.5T480-200H120v40H40Zm80-120v-80 80Zm720-320v-80 80ZM480-480Zm0 120q-33 0-56.5-23.5T400-440q0-23 9.5-45.5T446-550l34-50 34 50q27 42 36.5 64.5T560-440q0 33-23.5 56.5T480-360Z"/></svg>`;
                case 'sensor': return `<svg xmlns="http://www.w3.org/2000/svg" height="32" viewBox="0 -960 960 960" width="32" fill="${{color}}"><path d="M480-80q-83 0-156-31.5T197-197q-54-54-85.5-127T80-480q0-83 31.5-156T197-763q54-54 127-85.5T480-880q83 0 156 31.5T763-763q54 54 85.5 127T880-480q0 83-31.5 156T763-197q-54 54-127 85.5T480-80Zm0-80q134 0 227-93t93-227q0-134-93-227t-227-93q-134 0-227 93t-93 227q0 134 93 227t227 93Zm0-320Z"/></svg>`;
                default: return `<svg xmlns="http://www.w3.org/2000/svg" height="32" viewBox="0 -960 960 960" width="32" fill="${{color}}"><path d="M480-280q17 0 28.5-11.5T520-320q0-17-11.5-28.5T480-360q-17 0-28.5 11.5T440-320q0 17 11.5 28.5T480-280Zm-40-160h80v-320h-80v320Zm40 240q-83 0-156-31.5T197-287q-54-54-85.5-127T80-560q0-83 31.5-156T197-843q54-54 127-85.5T480-960q83 0 156 31.5T763-843q54 54 85.5 127T880-560q0 83-31.5 156T763-287q-54 54-127 85.5T480-170Zm0-80q116 0 198-82t82-198q0-116-82-198t-198-82q-116 0-198 82t-82 198q0 116 82 198t198 82Zm0-280Z"/></svg>`;
            }}
        }}
        
        // Detecta campo de porcentaje
        function obtenerNivelTanque(estacion) {{
            const campos = ['Porcentaje (%)', 'Porcentaje', 'Nivel (%)', 'nivel_%', 'Nivel', 'nivel'];
            for (let campo of campos) {{
                if (estacion[campo] !== undefined) {{
                    let v = parseFloat(estacion[campo]);
                    return Math.max(0, Math.min(100, isNaN(v) ? 0 : v));
                }}
            }}
            return 0;
        }}
        
        // Lógica robusta para offline
        function esOffline(enLinea) {{
            if (enLinea === undefined || enLinea === null) return false;
            const valor = String(enLinea).trim().toLowerCase();
            return valor === '0' || valor === 'false' || valor === 'off' || valor === 'no';
        }}
        
        // BARRA DE LLENADO VERTICAL SIN BORDES
        function crearIconoTanque(iconoUrl, nivel) {{
            const alturaLlenado = Math.round((nivel / 100) * 24);
            
            if (iconoUrl) {{
                return L.divIcon({{
                    html: `<div style="position:relative;width:32px;height:32px;">
                        <img src="${{iconoUrl}}" width="32" height="32" style="position:absolute;top:0;left:0;opacity:0.3;">
                        <div style="
                            position:absolute;
                            bottom:4px;
                            left:2px;
                            width:28px;
                            height:${{alturaLlenado}}px;
                            background:rgba(52,152,219,0.95);
                            border-radius:2px 2px 0 0;
                        "></div>
                        <div style="
                            position:absolute;
                            bottom:6px;
                            width:32px;
                            text-align:center;
                            font-size:9px;
                            color:white;
                            font-weight:bold;
                            text-shadow:0 1px 2px rgba(0,0,0,0.8);
                        ">${{Math.round(nivel)}}%</div>
                    </div>`,
                    iconSize: [32, 32],
                    iconAnchor: [16, 16],
                    popupAnchor: [0, -16]
                }});
            }} else {{
                const yInicio = 28 - alturaLlenado;
                const svg = `<svg xmlns="http://www.w3.org/2000/svg" width="32" height="32" viewBox="0 0 32 32">
                    <rect x="2" y="4" width="28" height="24" fill="#ecf0f1" rx="2"/>
                    <rect x="3" y="${{yInicio}}" width="26" height="${{alturaLlenado}}" fill="#3498db" rx="1"/>
                    <text x="16" y="20" font-family="Arial" font-size="9" fill="#2c3e50" text-anchor="middle" font-weight="bold">${{Math.round(nivel)}}%</text>
                </svg>`;
                return L.divIcon({{
                    html: svg,
                    iconSize: [32, 32],
                    iconAnchor: [16, 16],
                    popupAnchor: [0, -16]
                }});
            }}
        }}
        
        // CORREGIDO DEFINITIVO: OFFLINE = MISMO ICONO + FONDO NEGRO + BORDE ROJO (3px)
        function crearIcono(estacion) {{
            const tipo = estacion.tipo || 'otro';
            const enLineaRaw = estacion.en_linea;
            const offline = esOffline(enLineaRaw);
            const estado = parseInt(estacion.estado_bomba || estacion.estado || 0);
            const icono_url_on = limpiarUrl(estacion.icono_url_on);
            const icono_url_off = limpiarUrl(estacion.icono_url_off);
            const nivel = obtenerNivelTanque(estacion);
            
            // OFFLINE: MISMO ICONO QUE TENDRÍA ONLINE + FONDO NEGRO + BORDE ROJO (3px)
            if (offline) {{
                let iconContent;
                
                // Determinar qué icono usaría si estuviera online (mismo color y tipo)
                if (tipo === 'tanque') {{
                    // Para tanque offline, usar barra de llenado con nivel actual (sin icono personalizado)
                    const alturaLlenado = Math.round((nivel / 100) * 24);
                    const yInicio = 28 - alturaLlenado;
                    iconContent = `<svg xmlns="http://www.w3.org/2000/svg" width="28" height="28" viewBox="0 0 32 32">
                        <rect x="2" y="4" width="28" height="24" fill="#ecf0f1" rx="2"/>
                        <rect x="3" y="${{yInicio}}" width="26" height="${{alturaLlenado}}" fill="#3498db" rx="1"/>
                        <text x="16" y="20" font-family="Arial" font-size="8" fill="#2c3e50" text-anchor="middle">${{Math.round(nivel)}}%</text>
                    </svg>`;
                }} else if (estado === 1 && icono_url_on) {{
                    // Icono personalizado ON (pero offline)
                    iconContent = `<img src="${{icono_url_on}}" width="28" height="28" style="opacity:0.7;">`;
                }} else if (estado === 0 && icono_url_off) {{
                    // Icono personalizado OFF (pero offline)
                    iconContent = `<img src="${{icono_url_off}}" width="28" height="28" style="opacity:0.7;">`;
                }} else {{
                    // SVG predeterminado con color según estado (pero offline)
                    let color = '#f39c12';
                    if (tipo === 'pozo' || tipo === 'bomba') {{
                        color = estado === 1 ? '#27ae60' : '#e74c3c';
                    }} else if (tipo === 'sensor') {{
                        color = '#9b59b6';
                    }}
                    // Obtener SVG y reducir a 28x28
                    let svg = getDefaultSvg(tipo, color);
                    svg = svg.replace('width="32"', 'width="28"').replace('height="32"', 'height="28"');
                    iconContent = svg;
                }}
                
                // Contenedor: FONDO NEGRO + BORDE ROJO (3px) + MISMO ICONO QUE ONLINE
                return L.divIcon({{
                    html: `<div style="
                        width: 32px;
                        height: 32px;
                        //background: #000;
                        border: 3px solid #e74c3c;
                        border-radius: 4px;
                        display: flex;
                        align-items: center;
                        justify-content: center;
                        box-sizing: border-box;
                        box-shadow: 0 2px 8px rgba(0,0,0,0.5);
                    ">${{iconContent}}</div>`,
                    iconSize: [32, 32],
                    iconAnchor: [16, 16],
                    popupAnchor: [0, -16]
                }});
            }}
            
            // ONLINE: SIN FONDOS NI BORDES (solo el icono)
            if (tipo === 'tanque') {{
                const iconoUrl = estado === 1 ? icono_url_on : icono_url_off;
                return crearIconoTanque(iconoUrl, nivel);
            }}
            
            if (estado === 1 && icono_url_on) {{
                return L.icon({{
                    iconUrl: icono_url_on,
                    iconSize: [32, 32],
                    iconAnchor: [16, 16],
                    popupAnchor: [0, -16]
                }});
            }} else if (estado === 0 && icono_url_off) {{
                return L.icon({{
                    iconUrl: icono_url_off,
                    iconSize: [32, 32],
                    iconAnchor: [16, 16],
                    popupAnchor: [0, -16]
                }});
            }}
            
            // SVG predeterminado sin círculo
            let color = '#f39c12';
            if (tipo === 'pozo' || tipo === 'bomba') {{
                color = estado === 1 ? '#27ae60' : '#e74c3c';
            }} else if (tipo === 'sensor') {{
                color = '#9b59b6';
            }} else if (tipo === 'tanque') {{
                color = nivel >= 50 ? '#3498db' : '#95a5a6';
            }}
            
            const svg = getDefaultSvg(tipo, color);
            return L.divIcon({{
                html: svg,
                iconSize: [32, 32],
                iconAnchor: [16, 16],
                popupAnchor: [0, -16]
            }});
        }}
        
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
                    marker.setIcon(crearIcono(estacion));
                }} else {{
                    const marker = L.marker([lat, lng], {{ icon: crearIcono(estacion) }})
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
        
        function crearPopupContent(estacion) {{
            let html = `<div class="custom-popup"><h4>${{estacion.nombre || 'Estación'}}</h4><hr>`;
            
            const offline = esOffline(estacion.en_linea);
            const estadoLinea = offline ? '<span class="status-offline">Fuera de línea</span>' : '<span class="status-online">En línea</span>';
            html += `<div class="var-row"><span class="var-label">Estado:</span><span class="var-value">${{estadoLinea}}</span></div>`;
            
            if (estacion.tipo === 'tanque') {{
                html += `<div class="var-row"><span class="var-label">Nivel:</span><span class="var-value">${{obtenerNivelTanque(estacion)}}%</span></div>`;
            }}
            
            for (const key in estacion) {{
                if (!['nombre', 'latitud', 'longitud', 'tipo', 'estado_bomba', 'en_linea', 'icono', 'icono_url', 'icono_url_on', 'icono_url_off', 'Nivel', 'nivel', 'Porcentaje (%)', 'Porcentaje'].includes(key)) {{
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
            
            let total = 0, pozos_encendidos = 0, pozos_apagados = 0, tanques = 0, offline = 0, online = 0;
            
            datos.estaciones.forEach(estacion => {{
                total++;
                const offline = esOffline(estacion.en_linea);
                
                if (offline) {{
                    offline++;
                }} else {{
                    online++;
                    const tipo = estacion.tipo || 'otro';
                    const estado = parseInt(estacion.estado_bomba || estacion.estado || 0);
                    
                    if (tipo === 'pozo') {{
                        if (estado === 1) pozos_encendidos++;
                        else pozos_apagados++;
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
</body>
</html>
"""

st.components.v1.html(
    html_completo,
    width=1920,
    height=1080,
    scrolling=False
)
