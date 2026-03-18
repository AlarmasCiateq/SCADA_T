# # # # # # # # # import streamlit as st
# # # # # # # # # import requests
# # # # # # # # # import json
# # # # # # # # # from datetime import datetime
# # # # # # # # # from streamlit_autorefresh import st_autorefresh

# # # # # # # # # # Configuración minimalista
# # # # # # # # # st.set_page_config(
# # # # # # # # #     page_title="SCADA Monitor",
# # # # # # # # #     layout="wide",
# # # # # # # # #     initial_sidebar_state="collapsed"
# # # # # # # # # )

# # # # # # # # # # CSS para ocultar elementos de Streamlit
# # # # # # # # # st.markdown("""
# # # # # # # # #     <style>
# # # # # # # # #     [data-testid="stSidebar"] { display: none; }
# # # # # # # # #     [data-testid="stHeader"] { display: none; }
# # # # # # # # #     .block-container { padding: 0; max-width: 100%; margin: 0; }
# # # # # # # # #     .stApp { background-color: #0e1117; }
# # # # # # # # #     footer, .stDeployButton { display: none !important; }
# # # # # # # # #     </style>
# # # # # # # # #     """, unsafe_allow_html=True)

# # # # # # # # # # ==============================
# # # # # # # # # # CARGAR DATOS DESDE GITHUB (Python - SIN CORS)
# # # # # # # # # # ==============================
# # # # # # # # # def cargar_datos_github():
# # # # # # # # #     try:
# # # # # # # # #         # URL CORRECTA sin espacios
# # # # # # # # #         url = "https://raw.githubusercontent.com/AlarmasCiateq/SCADA_T/main/datos_estaciones.json"
        
# # # # # # # # #         # Forzar carga fresca (sin cache)
# # # # # # # # #         response = requests.get(
# # # # # # # # #             url + f"?t={int(datetime.now().timestamp() * 1000)}",
# # # # # # # # #             timeout=10,
# # # # # # # # #             headers={'Cache-Control': 'no-cache'}
# # # # # # # # #         )
# # # # # # # # #         response.raise_for_status()
# # # # # # # # #         return response.json()
# # # # # # # # #     except Exception as e:
# # # # # # # # #         st.error(f"Error al cargar datos: {str(e)[:50]}")
# # # # # # # # #         return None

# # # # # # # # # # ==============================
# # # # # # # # # # AUTO-REFRESH (5 segundos para pruebas)
# # # # # # # # # # ==============================
# # # # # # # # # # ⚠️ CAMBIA A 300000 PARA PRODUCCIÓN (5 minutos)
# # # # # # # # # st_autorefresh(interval=5000, key="auto_refresh")

# # # # # # # # # # ==============================
# # # # # # # # # # CARGAR DATOS
# # # # # # # # # # ==============================
# # # # # # # # # datos = cargar_datos_github()
# # # # # # # # # if not datos:
# # # # # # # # #     st.error("⚠️ No se pudieron cargar los datos de GitHub")
# # # # # # # # #     st.stop()

# # # # # # # # # # ==============================
# # # # # # # # # # GENERAR HTML+JS CON DATOS EMBEBIDOS
# # # # # # # # # # ==============================
# # # # # # # # # # Convertir datos a JSON string para embeber en JavaScript
# # # # # # # # # datos_json = json.dumps(datos)

# # # # # # # # # html_completo = f"""
# # # # # # # # # <!DOCTYPE html>
# # # # # # # # # <html lang="es">
# # # # # # # # # <head>
# # # # # # # # #     <meta charset="UTF-8">
# # # # # # # # #     <meta name="viewport" content="width=device-width, initial-scale=1.0">
# # # # # # # # #     <title>SCADA Monitor</title>
# # # # # # # # #     <link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css" />
# # # # # # # # #     <style>
# # # # # # # # #         * {{ margin: 0; padding: 0; box-sizing: border-box; }}
# # # # # # # # #         body {{ font-family: Arial, sans-serif; background: #0e1117; overflow: hidden; }}
# # # # # # # # #         #map {{ position: absolute; top: 0; left: 0; width: 100%; height: 100%; z-index: 1; }}
        
# # # # # # # # #         /* Estadísticas flotantes */
# # # # # # # # #         #stats-bar {{
# # # # # # # # #             position: fixed;
# # # # # # # # #             top: 10px;
# # # # # # # # #             right: 15px;
# # # # # # # # #             background: rgba(255, 255, 255, 0.95);
# # # # # # # # #             padding: 8px 15px;
# # # # # # # # #             border-radius: 8px;
# # # # # # # # #             box-shadow: 0 2px 10px rgba(0,0,0,0.15);
# # # # # # # # #             z-index: 1000;
# # # # # # # # #             display: grid;
# # # # # # # # #             grid-template-columns: repeat(6, auto);
# # # # # # # # #             gap: 12px;
# # # # # # # # #             align-items: center;
# # # # # # # # #             font-family: Arial, sans-serif;
# # # # # # # # #             font-size: 13px;
# # # # # # # # #         }}
# # # # # # # # #         .stat-value {{ font-weight: bold; color: #2c3e50; font-size: 16px; }}
# # # # # # # # #         .stat-label {{ font-size: 9px; color: #7f8c8d; }}
# # # # # # # # #         .custom-popup {{ font-family: Arial; padding: 12px; min-width: 280px; background: white; border-radius: 6px; }}
# # # # # # # # #         .custom-popup h4 {{ margin: 0 0 10px 0; color: #2c3e50; font-size: 16px; }}
# # # # # # # # #         .custom-popup hr {{ margin: 8px 0; border-color: #ecf0f1; }}
# # # # # # # # #         .custom-popup .var-row {{ margin: 6px 0; padding: 4px 0; display: flex; justify-content: space-between; font-size: 13px; }}
# # # # # # # # #         .custom-popup .var-label {{ color: #7f8c8d; }}
# # # # # # # # #         .custom-popup .var-value {{ font-weight: bold; color: #2c3e50; }}
# # # # # # # # #         .custom-popup .timestamp {{ font-size: 11px; color: #95a5a6; text-align: center; margin-top: 8px; }}
# # # # # # # # #     </style>
# # # # # # # # # </head>
# # # # # # # # # <body>
# # # # # # # # #     <div id="map"></div>
# # # # # # # # #     <div id="stats-bar">
# # # # # # # # #         <div><div class="stat-value">📡 <span id="stat-total">0</span></div><div class="stat-label">Total</div></div>
# # # # # # # # #         <div><div class="stat-value" style="color:#27ae60">🟢 <span id="stat-activos">0</span></div><div class="stat-label">Activos</div></div>
# # # # # # # # #         <div><div class="stat-value" style="color:#e74c3c">🔴 <span id="stat-inactivos">0</span></div><div class="stat-label">Inactivos</div></div>
# # # # # # # # #         <div><div class="stat-value" style="color:#3498db">🔵 <span id="stat-tanques">0</span></div><div class="stat-label">Tanques</div></div>
# # # # # # # # #         <div><div class="stat-value" style="color:#000">⚫ <span id="stat-offline">0</span></div><div class="stat-label">Offline</div></div>
# # # # # # # # #         <div><div class="stat-value">🕐 <span id="stat-time">--:--</span></div><div class="stat-label">Actualizado</div></div>
# # # # # # # # #     </div>

# # # # # # # # #     <script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"></script>
# # # # # # # # #     <script>
# # # # # # # # #         // ════════════════════════════════════════════════════════════════
# # # # # # # # #         // DATOS CARGADOS DESDE PYTHON (embebidos en el HTML)
# # # # # # # # #         // ════════════════════════════════════════════════════════════════
# # # # # # # # #         const DATOS_INICIALES = {datos_json};
        
# # # # # # # # #         // ════════════════════════════════════════════════════════════════
        
# # # # # # # # #         let map = null;
# # # # # # # # #         let markers = new Map(); // id -> marker
# # # # # # # # #         let primeraCarga = true;
        
# # # # # # # # #         // Inicializar mapa
# # # # # # # # #         function initMap() {{
# # # # # # # # #             map = L.map('map', {{
# # # # # # # # #                 zoomControl: true,
# # # # # # # # #                 scrollWheelZoom: true,
# # # # # # # # #                 dragging: true
# # # # # # # # #             }});
            
# # # # # # # # #             // Mapa claro con calles sutiles
# # # # # # # # #             L.tileLayer('https://{{s}}.basemaps.cartocdn.com/light_all/{{z}}/{{x}}/{{y}}{{r}}.png', {{
# # # # # # # # #                 attribution: '',
# # # # # # # # #                 subdomains: 'abcd',
# # # # # # # # #                 maxZoom: 19
# # # # # # # # #             }}).addTo(map);
            
# # # # # # # # #             // Cargar datos iniciales
# # # # # # # # #             actualizarMapa(DATOS_INICIALES);
# # # # # # # # #             actualizarEstadisticas(DATOS_INICIALES);
            
# # # # # # # # #             // Actualizar timestamp
# # # # # # # # #             document.getElementById('stat-time').textContent = new Date().toLocaleTimeString('es-ES', {{ 
# # # # # # # # #                 hour: '2-digit', 
# # # # # # # # #                 minute: '2-digit' 
# # # # # # # # #             }});
# # # # # # # # #         }}
        
# # # # # # # # #         // Actualizar mapa (solo valores y colores, no posiciones)
# # # # # # # # #         function actualizarMapa(datos) {{
# # # # # # # # #             if (!datos || !datos.estaciones) return;
            
# # # # # # # # #             const nuevasBounds = [];
            
# # # # # # # # #             datos.estaciones.forEach(estacion => {{
# # # # # # # # #                 if (!estacion.latitud || !estacion.longitud) return;
                
# # # # # # # # #                 const id = estacion.nombre || `${{estacion.latitud}},${{estacion.longitud}}`;
# # # # # # # # #                 const lat = parseFloat(estacion.latitud);
# # # # # # # # #                 const lng = parseFloat(estacion.longitud);
                
# # # # # # # # #                 nuevasBounds.push([lat, lng]);
                
# # # # # # # # #                 // Si ya existe el marcador, actualizar popup y color
# # # # # # # # #                 if (markers.has(id)) {{
# # # # # # # # #                     const marker = markers.get(id);
                    
# # # # # # # # #                     // Actualizar popup
# # # # # # # # #                     const popupContent = crearPopupContent(estacion);
# # # # # # # # #                     marker.setPopupContent(popupContent);
                    
# # # # # # # # #                     // Actualizar color si cambió estado
# # # # # # # # #                     const nuevoIcono = crearIcono(estacion.tipo, estacion.estado_bomba, estacion.en_linea);
# # # # # # # # #                     marker.setIcon(nuevoIcono);
                    
# # # # # # # # #                 }} else {{
# # # # # # # # #                     // Crear nuevo marcador
# # # # # # # # #                     const icono = crearIcono(estacion.tipo, estacion.estado_bomba, estacion.en_linea);
# # # # # # # # #                     const popupContent = crearPopupContent(estacion);
                    
# # # # # # # # #                     const marker = L.marker([lat, lng], {{ icon: icono }})
# # # # # # # # #                         .bindPopup(popupContent, {{ maxWidth: 320 }})
# # # # # # # # #                         .addTo(map);
                    
# # # # # # # # #                     markers.set(id, marker);
# # # # # # # # #                 }}
# # # # # # # # #             }});
            
# # # # # # # # #             // Ajustar bounds SOLO en primera carga
# # # # # # # # #             if (primeraCarga && nuevasBounds.length > 0) {{
# # # # # # # # #                 const bounds = L.latLngBounds(nuevasBounds);
# # # # # # # # #                 map.fitBounds(bounds, {{ padding: [40, 40] }});
# # # # # # # # #                 primeraCarga = false;
# # # # # # # # #                 console.log('✓ Zoom inicial ajustado');
# # # # # # # # #             }}
# # # # # # # # #         }}
        
# # # # # # # # #         // Crear icono según tipo y estado
# # # # # # # # #         function crearIcono(tipo, estado, enLinea) {{
# # # # # # # # #             // Determinar color
# # # # # # # # #             let color = '#000000'; // negro por defecto (offline)
# # # # # # # # #             if (enLinea !== 0) {{
# # # # # # # # #                 if (tipo === 'pozo' || tipo === 'bomba') {{
# # # # # # # # #                     color = estado === 1 ? '#27ae60' : '#e74c3c'; // verde/rojo
# # # # # # # # #                 }} else if (tipo === 'tanque') {{
# # # # # # # # #                     color = estado === 1 ? '#3498db' : '#95a5a6'; // azul/gris
# # # # # # # # #                 }} else if (tipo === 'sensor') {{
# # # # # # # # #                     color = '#9b59b6'; // morado
# # # # # # # # #                 }} else {{
# # # # # # # # #                     color = '#f39c12'; // naranja
# # # # # # # # #                 }}
# # # # # # # # #             }}
            
# # # # # # # # #             // Determinar ícono (siempre el mismo según tipo)
# # # # # # # # #             let iconClass = 'fa-tint'; // pozo por defecto
# # # # # # # # #             if (tipo === 'tanque') iconClass = 'fa-water';
# # # # # # # # #             else if (tipo === 'bomba') iconClass = 'fa-cog';
# # # # # # # # #             else if (tipo === 'sensor') iconClass = 'fa-microchip';
            
# # # # # # # # #             return L.divIcon({{
# # # # # # # # #                 html: `<div style="
# # # # # # # # #                     background: ${{color}};
# # # # # # # # #                     width: 32px;
# # # # # # # # #                     height: 32px;
# # # # # # # # #                     border-radius: 50%;
# # # # # # # # #                     display: flex;
# # # # # # # # #                     align-items: center;
# # # # # # # # #                     justify-content: center;
# # # # # # # # #                     box-shadow: 0 2px 6px rgba(0,0,0,0.4);
# # # # # # # # #                 ">
# # # # # # # # #                     <i class="fa ${{iconClass}}" style="color: white; font-size: 16px;"></i>
# # # # # # # # #                 </div>`,
# # # # # # # # #                 className: '',
# # # # # # # # #                 iconSize: [32, 32],
# # # # # # # # #                 iconAnchor: [16, 16],
# # # # # # # # #                 popupAnchor: [0, -16]
# # # # # # # # #             }});
# # # # # # # # #         }}
        
# # # # # # # # #         // Crear contenido del popup
# # # # # # # # #         function crearPopupContent(estacion) {{
# # # # # # # # #             let html = `<div class="custom-popup"><h4>${{estacion.nombre || 'Estación'}}</h4><hr>`;
            
# # # # # # # # #             for (const key in estacion) {{
# # # # # # # # #                 if (!['nombre', 'latitud', 'longitud', 'tipo', 'estado_bomba', 'en_linea', 'icono'].includes(key)) {{
# # # # # # # # #                     const value = typeof estacion[key] === 'number' 
# # # # # # # # #                         ? estacion[key].toLocaleString('es-ES', {{ minimumFractionDigits: 2, maximumFractionDigits: 2 }})
# # # # # # # # #                         : estacion[key];
                    
# # # # # # # # #                     html += `<div class="var-row"><span class="var-label">${{key}}:</span><span class="var-value">${{value}}</span></div>`;
# # # # # # # # #                 }}
# # # # # # # # #             }}
            
# # # # # # # # #             html += `<hr><div class="timestamp">📅 ${{new Date().toLocaleString('es-ES')}}</div></div>`;
# # # # # # # # #             return html;
# # # # # # # # #         }}
        
# # # # # # # # #         // Actualizar estadísticas
# # # # # # # # #         function actualizarEstadisticas(datos) {{
# # # # # # # # #             if (!datos || !datos.estaciones) return;
            
# # # # # # # # #             const stats = {{ total:0, activos:0, inactivos:0, tanques:0, offline:0 }};
            
# # # # # # # # #             datos.estaciones.forEach(estacion => {{
# # # # # # # # #                 stats.total++;
# # # # # # # # #                 const enLinea = estacion.en_linea || 1;
# # # # # # # # #                 const tipo = estacion.tipo || 'otro';
# # # # # # # # #                 const estado = estacion.estado_bomba || estacion.estado || 0;
                
# # # # # # # # #                 if (enLinea === 0) stats.offline++;
# # # # # # # # #                 else if (tipo === 'pozo') {{
# # # # # # # # #                     if (estado === 1) stats.activos++;
# # # # # # # # #                     else stats.inactivos++;
# # # # # # # # #                 }} else if (tipo === 'tanque') stats.tanques++;
# # # # # # # # #             }});
            
# # # # # # # # #             document.getElementById('stat-total').textContent = stats.total;
# # # # # # # # #             document.getElementById('stat-activos').textContent = stats.activos;
# # # # # # # # #             document.getElementById('stat-inactivos').textContent = stats.inactivos;
# # # # # # # # #             document.getElementById('stat-tanques').textContent = stats.tanques;
# # # # # # # # #             document.getElementById('stat-offline').textContent = stats.offline;
# # # # # # # # #         }}
        
# # # # # # # # #         // Iniciar cuando el DOM esté listo
# # # # # # # # #         document.addEventListener('DOMContentLoaded', initMap);
# # # # # # # # #     </script>
    
# # # # # # # # #     <!-- Font Awesome para íconos -->
# # # # # # # # #     <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
# # # # # # # # # </body>
# # # # # # # # # </html>
# # # # # # # # # """

# # # # # # # # # # Mostrar el HTML+JS en Streamlit (se ejecutará en el navegador)
# # # # # # # # # st.components.v1.html(
# # # # # # # # #     html_completo,
# # # # # # # # #     width=1920,
# # # # # # # # #     height=1080,
# # # # # # # # #     scrolling=False
# # # # # # # # # )
# # # # # # # # # import streamlit as st
# # # # # # # # # import requests
# # # # # # # # # import json
# # # # # # # # # import base64
# # # # # # # # # from datetime import datetime
# # # # # # # # # from streamlit_autorefresh import st_autorefresh
# # # # # # # # # import time

# # # # # # # # # # Configuración minimalista - SIN TÍTULO NI DECORACIONES
# # # # # # # # # st.set_page_config(
# # # # # # # # #     page_title="SCADA Monitor",
# # # # # # # # #     layout="wide",
# # # # # # # # #     initial_sidebar_state="collapsed"
# # # # # # # # # )

# # # # # # # # # # CSS AGRESIVO para eliminar TODO (header, título, scroll, barras)
# # # # # # # # # st.markdown("""
# # # # # # # # #     <style>
# # # # # # # # #     /* Eliminar TODO */
# # # # # # # # #     [data-testid="stSidebar"] { display: none !important; }
# # # # # # # # #     [data-testid="stHeader"] { display: none !important; }
# # # # # # # # #     [data-testid="stDecoration"] { display: none !important; }
# # # # # # # # #     header { display: none !important; }
# # # # # # # # #     #MainMenu { display: none !important; }
# # # # # # # # #     footer { display: none !important; }
# # # # # # # # #     .stApp { 
# # # # # # # # #         background-color: #0e1117; 
# # # # # # # # #         padding: 0 !important; 
# # # # # # # # #         margin: 0 !important; 
# # # # # # # # #         overflow: hidden !important;
# # # # # # # # #     }
# # # # # # # # #     .block-container { 
# # # # # # # # #         padding: 0 !important; 
# # # # # # # # #         max-width: 100% !important; 
# # # # # # # # #         margin: 0 !important; 
# # # # # # # # #         overflow: hidden !important;
# # # # # # # # #     }
# # # # # # # # #     .main { 
# # # # # # # # #         padding: 0 !important; 
# # # # # # # # #         margin: 0 !important; 
# # # # # # # # #         overflow: hidden !important;
# # # # # # # # #     }
# # # # # # # # #     .block-container > div { 
# # # # # # # # #         padding: 0 !important; 
# # # # # # # # #         margin: 0 !important; 
# # # # # # # # #     }
# # # # # # # # #     /* Ocultar cualquier scroll */
# # # # # # # # #     ::-webkit-scrollbar { display: none !important; }
# # # # # # # # #     body { overflow: hidden !important; }
# # # # # # # # #     </style>
# # # # # # # # #     """, unsafe_allow_html=True)

# # # # # # # # # # ==============================
# # # # # # # # # # CARGAR DATOS CON REINTENTOS SILENCIOSOS (usa datos anteriores si falla)
# # # # # # # # # # ==============================
# # # # # # # # # def cargar_datos_github(datos_anteriores=None, max_intentos=3):
# # # # # # # # #     for intento in range(max_intentos):
# # # # # # # # #         try:
# # # # # # # # #             GITHUB_USER = "AlarmasCiateq"
# # # # # # # # #             REPO_NAME = "SCADA_T"
# # # # # # # # #             BRANCH = "main"
# # # # # # # # #             FILE_PATH = "datos_estaciones.json"
            
# # # # # # # # #             api_url = f"https://api.github.com/repos/{GITHUB_USER}/{REPO_NAME}/contents/{FILE_PATH}?ref={BRANCH}"
            
# # # # # # # # #             headers = {
# # # # # # # # #                 'User-Agent': f'SCADA-Monitor-{datetime.now().timestamp()}',
# # # # # # # # #                 'Accept': 'application/vnd.github.v3+json'
# # # # # # # # #             }
            
# # # # # # # # #             response = requests.get(api_url, headers=headers, timeout=10)
# # # # # # # # #             response.raise_for_status()
            
# # # # # # # # #             data = response.json()
# # # # # # # # #             content_bytes = base64.b64decode(data['content'])
# # # # # # # # #             content_str = content_bytes.decode('utf-8')
# # # # # # # # #             datos = json.loads(content_str)
            
# # # # # # # # #             return datos  # Éxito: devuelve nuevos datos
            
# # # # # # # # #         except Exception:
# # # # # # # # #             if intento < max_intentos - 1:
# # # # # # # # #                 time.sleep(1)  # Espera 1 segundo y reintenta
# # # # # # # # #                 continue
    
# # # # # # # # #     # Falló todo: devuelve datos anteriores si existen, sino None
# # # # # # # # #     return datos_anteriores if datos_anteriores else None

# # # # # # # # # # ==============================
# # # # # # # # # # AUTO-REFRESH (5 segundos para pruebas)
# # # # # # # # # # ==============================
# # # # # # # # # st_autorefresh(interval=60000, key="auto_refresh")

# # # # # # # # # # ==============================
# # # # # # # # # # CARGAR DATOS (usa cache en session_state para mantener estado anterior)
# # # # # # # # # # ==============================
# # # # # # # # # if 'datos_cache' not in st.session_state:
# # # # # # # # #     st.session_state.datos_cache = None

# # # # # # # # # # Intentar cargar nuevos datos (con reintentos silenciosos)
# # # # # # # # # nuevos_datos = cargar_datos_github(st.session_state.datos_cache)

# # # # # # # # # # Si hay nuevos datos válidos, actualizar cache
# # # # # # # # # if nuevos_datos:
# # # # # # # # #     st.session_state.datos_cache = nuevos_datos

# # # # # # # # # # Usar datos del cache (pueden ser nuevos o anteriores si falló la carga)
# # # # # # # # # datos = st.session_state.datos_cache

# # # # # # # # # # Si NO hay datos en absoluto (primera carga fallida), mostrar mínimo
# # # # # # # # # if not datos:
# # # # # # # # #     st.markdown("""
# # # # # # # # #         <div style="position:fixed;top:0;left:0;width:100%;height:100%;background:#0e1117;color:white;
# # # # # # # # #                     display:flex;justify-content:center;align-items:center;font-family:Arial;">
# # # # # # # # #             <div style="text-align:center;padding:20px;">
# # # # # # # # #                 <h2>🛢️ SCADA Monitor</h2>
# # # # # # # # #                 <p>Esperando primera conexión con el sistema...</p>
# # # # # # # # #             </div>
# # # # # # # # #         </div>
# # # # # # # # #         """, unsafe_allow_html=True)
# # # # # # # # #     st.stop()

# # # # # # # # # # ==============================
# # # # # # # # # # GENERAR HTML+JS (tooltip simple + popup completo)
# # # # # # # # # # ==============================
# # # # # # # # # datos_json = json.dumps(datos)

# # # # # # # # # html_completo = f"""
# # # # # # # # # <!DOCTYPE html>
# # # # # # # # # <html lang="es">
# # # # # # # # # <head>
# # # # # # # # #     <meta charset="UTF-8">
# # # # # # # # #     <meta name="viewport" content="width=device-width, initial-scale=1.0">
# # # # # # # # #     <title>SCADA Monitor</title>
# # # # # # # # #     <link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css" />
# # # # # # # # #     <style>
# # # # # # # # #         * {{ margin: 0; padding: 0; box-sizing: border-box; }}
# # # # # # # # #         body {{ 
# # # # # # # # #             font-family: Arial, sans-serif; 
# # # # # # # # #             background: #0e1117; 
# # # # # # # # #             overflow: hidden; 
# # # # # # # # #             height: 100vh;
# # # # # # # # #             width: 100vw;
# # # # # # # # #         }}
# # # # # # # # #         #map {{ 
# # # # # # # # #             position: absolute; 
# # # # # # # # #             top: 0; 
# # # # # # # # #             left: 0; 
# # # # # # # # #             width: 100%; 
# # # # # # # # #             height: 100%; 
# # # # # # # # #             z-index: 1; 
# # # # # # # # #         }}
# # # # # # # # #         #stats-bar {{
# # # # # # # # #             position: fixed;
# # # # # # # # #             top: 10px;
# # # # # # # # #             right: 15px;
# # # # # # # # #             background: rgba(255, 255, 255, 0.95);
# # # # # # # # #             padding: 6px 10px;
# # # # # # # # #             border-radius: 6px;
# # # # # # # # #             box-shadow: 0 2px 8px rgba(0,0,0,0.15);
# # # # # # # # #             z-index: 1000;
# # # # # # # # #             display: grid;
# # # # # # # # #             grid-template-columns: repeat(7, auto);
# # # # # # # # #             gap: 8px;
# # # # # # # # #             align-items: center;
# # # # # # # # #             font-family: Arial, sans-serif;
# # # # # # # # #             font-size: 11px;
# # # # # # # # #         }}
# # # # # # # # #         .stat-value {{ font-weight: bold; color: #2c3e50; font-size: 14px; }}
# # # # # # # # #         .stat-label {{ font-size: 7px; color: #7f8c8d; white-space: nowrap; }}
# # # # # # # # #         .custom-popup {{ font-family: Arial; padding: 12px; min-width: 280px; background: white; border-radius: 6px; }}
# # # # # # # # #         .custom-popup h4 {{ margin: 0 0 10px 0; color: #2c3e50; font-size: 16px; }}
# # # # # # # # #         .custom-popup hr {{ margin: 8px 0; border-color: #ecf0f1; }}
# # # # # # # # #         .custom-popup .var-row {{ margin: 6px 0; padding: 4px 0; display: flex; justify-content: space-between; font-size: 13px; }}
# # # # # # # # #         .custom-popup .var-label {{ color: #7f8c8d; }}
# # # # # # # # #         .custom-popup .var-value {{ font-weight: bold; color: #2c3e50; }}
# # # # # # # # #         .custom-popup .timestamp {{ font-size: 11px; color: #95a5a6; text-align: center; margin-top: 8px; }}
# # # # # # # # #     </style>
# # # # # # # # # </head>
# # # # # # # # # <body>
# # # # # # # # #     <div id="map"></div>
# # # # # # # # #     <div id="stats-bar">
# # # # # # # # #         <div><div class="stat-value">📡 <span id="stat-total">0</span></div><div class="stat-label">Total</div></div>
# # # # # # # # #         <div><div class="stat-value" style="color:#27ae60">🟢 <span id="stat-encendidos">0</span></div><div class="stat-label">Pozos Encendidos</div></div>
# # # # # # # # #         <div><div class="stat-value" style="color:#e74c3c">🔴 <span id="stat-apagados">0</span></div><div class="stat-label">Pozos Apagados</div></div>
# # # # # # # # #         <div><div class="stat-value" style="color:#3498db">🔵 <span id="stat-tanques">0</span></div><div class="stat-label">Tanques</div></div>
# # # # # # # # #         <div><div class="stat-value" style="color:#000">⚫ </div></div>
# # # # # # # # #         <div><div class="stat-value">🕐 <span id="stat-time">--:--</span></div><div class="stat-label">Actualizado</div></div>
# # # # # # # # #     </div>

# # # # # # # # #     <script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"></script>
# # # # # # # # #     <script>
# # # # # # # # #         const DATOS_INICIALES = {datos_json};
# # # # # # # # #         let map = null;
# # # # # # # # #         let markers = new Map();
# # # # # # # # #         let primeraCarga = true;
        
# # # # # # # # #         function initMap() {{
# # # # # # # # #             map = L.map('map', {{
# # # # # # # # #                 zoomControl: true,
# # # # # # # # #                 scrollWheelZoom: true,
# # # # # # # # #                 dragging: true
# # # # # # # # #             }});
            
# # # # # # # # #             L.tileLayer('https://{{s}}.basemaps.cartocdn.com/light_all/{{z}}/{{x}}/{{y}}{{r}}.png', {{
# # # # # # # # #                 attribution: '',
# # # # # # # # #                 subdomains: 'abcd',
# # # # # # # # #                 maxZoom: 19
# # # # # # # # #             }}).addTo(map);
            
# # # # # # # # #             actualizarMapa(DATOS_INICIALES);
# # # # # # # # #             actualizarEstadisticas(DATOS_INICIALES);
# # # # # # # # #             document.getElementById('stat-time').textContent = new Date().toLocaleTimeString('es-ES', {{ hour: '2-digit', minute: '2-digit' }});
# # # # # # # # #         }}
        
# # # # # # # # #         function actualizarMapa(datos) {{
# # # # # # # # #             if (!datos || !datos.estaciones) return;
# # # # # # # # #             const nuevasBounds = [];
            
# # # # # # # # #             datos.estaciones.forEach(estacion => {{
# # # # # # # # #                 if (!estacion.latitud || !estacion.longitud) return;
# # # # # # # # #                 const id = estacion.nombre || `${{estacion.latitud}},${{estacion.longitud}}`;
# # # # # # # # #                 const lat = parseFloat(estacion.latitud);
# # # # # # # # #                 const lng = parseFloat(estacion.longitud);
# # # # # # # # #                 nuevasBounds.push([lat, lng]);
                
# # # # # # # # #                 if (markers.has(id)) {{
# # # # # # # # #                     const marker = markers.get(id);
# # # # # # # # #                     marker.setPopupContent(crearPopupContent(estacion));
# # # # # # # # #                     marker.setIcon(crearIcono(estacion.tipo, estacion.estado_bomba, estacion.en_linea));
# # # # # # # # #                 }} else {{
# # # # # # # # #                     const marker = L.marker([lat, lng], {{ 
# # # # # # # # #                         icon: crearIcono(estacion.tipo, estacion.estado_bomba, estacion.en_linea)
# # # # # # # # #                     }})
# # # # # # # # #                     .bindPopup(crearPopupContent(estacion), {{ maxWidth: 320 }})
# # # # # # # # #                     .bindTooltip(estacion.nombre || 'Estación', {{ 
# # # # # # # # #                         permanent: false, 
# # # # # # # # #                         direction: 'top',
# # # # # # # # #                         opacity: 0.9
# # # # # # # # #                     }})
# # # # # # # # #                     .addTo(map);
# # # # # # # # #                     markers.set(id, marker);
# # # # # # # # #                 }}
# # # # # # # # #             }});
            
# # # # # # # # #             if (primeraCarga && nuevasBounds.length > 0) {{
# # # # # # # # #                 map.fitBounds(nuevasBounds, {{ padding: [40, 40] }});
# # # # # # # # #                 primeraCarga = false;
# # # # # # # # #             }}
# # # # # # # # #         }}
        
# # # # # # # # #         function crearIcono(tipo, estado, enLinea) {{
# # # # # # # # #             let color = '#000000';
# # # # # # # # #             if (enLinea !== 0) {{
# # # # # # # # #                 if (tipo === 'pozo' || tipo === 'bomba') {{
# # # # # # # # #                     color = estado === 1 ? '#27ae60' : '#e74c3c';
# # # # # # # # #                 }} else if (tipo === 'tanque') {{
# # # # # # # # #                     color = estado === 1 ? '#3498db' : '#95a5a6';
# # # # # # # # #                 }} else if (tipo === 'sensor') {{
# # # # # # # # #                     color = '#9b59b6';
# # # # # # # # #                 }} else {{
# # # # # # # # #                     color = '#f39c12';
# # # # # # # # #                 }}
# # # # # # # # #             }}
            
# # # # # # # # #             let iconClass = 'fa-tint';
# # # # # # # # #             if (tipo === 'tanque') iconClass = 'fa-water';
# # # # # # # # #             else if (tipo === 'bomba') iconClass = 'fa-cog';
# # # # # # # # #             else if (tipo === 'sensor') iconClass = 'fa-microchip';
            
# # # # # # # # #             return L.divIcon({{
# # # # # # # # #                 html: `<div style="background:${{color}};width:32px;height:32px;border-radius:50%;display:flex;align-items:center;justify-content:center;box-shadow:0 2px 6px rgba(0,0,0,0.4);"><i class="fa ${{iconClass}}" style="color:white;font-size:16px;"></i></div>`,
# # # # # # # # #                 className: '',
# # # # # # # # #                 iconSize: [32, 32],
# # # # # # # # #                 iconAnchor: [16, 16],
# # # # # # # # #                 popupAnchor: [0, -16]
# # # # # # # # #             }});
# # # # # # # # #         }}
        
# # # # # # # # #         function crearPopupContent(estacion) {{
# # # # # # # # #             let html = `<div class="custom-popup"><h4>${{estacion.nombre || 'Estación'}}</h4><hr>`;
# # # # # # # # #             for (const key in estacion) {{
# # # # # # # # #                 if (!['nombre', 'latitud', 'longitud', 'tipo', 'estado_bomba', 'en_linea', 'icono'].includes(key)) {{
# # # # # # # # #                     const value = typeof estacion[key] === 'number' ? estacion[key].toLocaleString('es-ES', {{ minimumFractionDigits: 2, maximumFractionDigits: 2 }}) : estacion[key];
# # # # # # # # #                     html += `<div class="var-row"><span class="var-label">${{key}}:</span><span class="var-value">${{value}}</span></div>`;
# # # # # # # # #                 }}
# # # # # # # # #             }}
# # # # # # # # #             html += `<hr><div class="timestamp">📅 ${{new Date().toLocaleString('es-ES')}}</div></div>`;
# # # # # # # # #             return html;
# # # # # # # # #         }}
        
# # # # # # # # #         function actualizarEstadisticas(datos) {{
# # # # # # # # #             if (!datos || !datos.estaciones) return;
# # # # # # # # #             const stats = {{ total:0, pozos_encendidos:0, pozos_apagados:0, tanques:0, offline:0, online:0 }};
            
# # # # # # # # #             datos.estaciones.forEach(estacion => {{
# # # # # # # # #                 stats.total++;
# # # # # # # # #                 const enLinea = estacion.en_linea || 1;
# # # # # # # # #                 const tipo = estacion.tipo || 'otro';
# # # # # # # # #                 const estado = estacion.estado_bomba || estacion.estado || 0;
                
# # # # # # # # #                 if (enLinea === 0) stats.offline++;
# # # # # # # # #                 else stats.online++;
                
# # # # # # # # #                 if (tipo === 'pozo' && enLinea === 1) {{
# # # # # # # # #                     if (estado === 1) stats.pozos_encendidos++;
# # # # # # # # #                     else stats.pozos_apagados++;
# # # # # # # # #                 }} else if (tipo === 'tanque') stats.tanques++;
# # # # # # # # #             }});
            
# # # # # # # # #             document.getElementById('stat-total').textContent = stats.total;
# # # # # # # # #             document.getElementById('stat-encendidos').textContent = stats.pozos_encendidos;
# # # # # # # # #             document.getElementById('stat-apagados').textContent = stats.pozos_apagados;
# # # # # # # # #             document.getElementById('stat-tanques').textContent = stats.tanques;
# # # # # # # # #             document.getElementById('stat-offline').textContent = stats.offline;
# # # # # # # # #             document.getElementById('stat-online').textContent = stats.online;
# # # # # # # # #         }}
        
# # # # # # # # #         document.addEventListener('DOMContentLoaded', initMap);
# # # # # # # # #     </script>
# # # # # # # # #     <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
# # # # # # # # # </body>
# # # # # # # # # </html>
# # # # # # # # # """

# # # # # # # # # # Mostrar mapa ocupando TODO el espacio (sin scroll)
# # # # # # # # # st.components.v1.html(
# # # # # # # # #     html_completo,
# # # # # # # # #     width=1920,
# # # # # # # # #     height=1080,
# # # # # # # # #     scrolling=False
# # # # # # # # # )

# # # # # # # # import streamlit as st
# # # # # # # # import requests
# # # # # # # # import json
# # # # # # # # import base64
# # # # # # # # from datetime import datetime
# # # # # # # # from streamlit_autorefresh import st_autorefresh
# # # # # # # # import time
# # # # # # # # import os

# # # # # # # # # Configuración minimalista
# # # # # # # # st.set_page_config(
# # # # # # # #     page_title="🌎 SCADA Monitor",
# # # # # # # #     layout="wide",
# # # # # # # #     initial_sidebar_state="collapsed"
# # # # # # # # )

# # # # # # # # # CSS AGRESIVO para eliminar TODO
# # # # # # # # st.markdown("""
# # # # # # # #     <style>
# # # # # # # #     [data-testid="stSidebar"] { display: none !important; }
# # # # # # # #     [data-testid="stHeader"] { display: none !important; }
# # # # # # # #     [data-testid="stDecoration"] { display: none !important; }
# # # # # # # #     header { display: none !important; }
# # # # # # # #     #MainMenu { display: none !important; }
# # # # # # # #     footer { display: none !important; }
# # # # # # # #     .stApp { background-color: #0e1117; padding: 0 !important; margin: 0 !important; overflow: hidden !important; }
# # # # # # # #     .block-container { padding: 0 !important; max-width: 100% !important; margin: 0 !important; overflow: hidden !important; }
# # # # # # # #     .main { padding: 0 !important; margin: 0 !important; overflow: hidden !important; }
# # # # # # # #     .block-container > div { padding: 0 !important; margin: 0 !important; }
# # # # # # # #     ::-webkit-scrollbar { display: none !important; }
# # # # # # # #     body { overflow: hidden !important; }
# # # # # # # #     </style>
# # # # # # # #     """, unsafe_allow_html=True)

# # # # # # # # # ==============================
# # # # # # # # # OBTENER TOKEN DE GITHUB (Streamlit Secrets o Environment Variable)
# # # # # # # # # ==============================
# # # # # # # # def obtener_token_github():
# # # # # # # #     """Obtiene el token de GitHub de Streamlit Secrets o variable de entorno"""
# # # # # # # #     try:
# # # # # # # #         # Intentar desde Streamlit Secrets (recomendado para producción)
# # # # # # # #         if hasattr(st, 'secrets') and "GITHUB_TOKEN" in st.secrets:
# # # # # # # #             return st.secrets["GITHUB_TOKEN"]
# # # # # # # #     except:
# # # # # # # #         pass
    
# # # # # # # #     # Intentar desde variable de entorno (para desarrollo local)
# # # # # # # #     return os.getenv("GITHUB_TOKEN", None)

# # # # # # # # # ==============================
# # # # # # # # # CARGAR DATOS CON TOKEN Y REINTENTOS SILENCIOSOS
# # # # # # # # # ==============================
# # # # # # # # def cargar_datos_github(datos_anteriores=None, max_intentos=3):
# # # # # # # #     token = obtener_token_github()
    
# # # # # # # #     for intento in range(max_intentos):
# # # # # # # #         try:
# # # # # # # #             GITHUB_USER = "AlarmasCiateq"
# # # # # # # #             REPO_NAME = "SCADA_T"
# # # # # # # #             BRANCH = "main"
# # # # # # # #             FILE_PATH = "datos_estaciones.json"
            
# # # # # # # #             api_url = f"https://api.github.com/repos/{GITHUB_USER}/{REPO_NAME}/contents/{FILE_PATH}?ref={BRANCH}"
            
# # # # # # # #             # Headers con token si está disponible
# # # # # # # #             headers = {
# # # # # # # #                 'User-Agent': f'SCADA-Monitor-{datetime.now().timestamp()}',
# # # # # # # #                 'Accept': 'application/vnd.github.v3+json'
# # # # # # # #             }
            
# # # # # # # #             # Agregar token si existe (aumenta límite a 5000 solicitudes/hora)
# # # # # # # #             if token:
# # # # # # # #                 headers['Authorization'] = f'token {token}'
            
# # # # # # # #             response = requests.get(api_url, headers=headers, timeout=10)
# # # # # # # #             response.raise_for_status()
            
# # # # # # # #             data = response.json()
# # # # # # # #             content_bytes = base64.b64decode(data['content'])
# # # # # # # #             content_str = content_bytes.decode('utf-8')
# # # # # # # #             datos = json.loads(content_str)
            
# # # # # # # #             return datos
            
# # # # # # # #         except requests.exceptions.HTTPError as e:
# # # # # # # #             # Si es error 401 (token inválido) o 403 (rate limit sin token), no reintentar
# # # # # # # #             if e.response.status_code in [401, 403]:
# # # # # # # #                 # Si no hay token y es 403, es rate limit sin autenticación
# # # # # # # #                 if not token and e.response.status_code == 403:
# # # # # # # #                     st.warning("⚠️ Sin token de GitHub. Límite de 60 solicitudes/hora alcanzado. Usa un token para 5000 solicitudes/hora.")
# # # # # # # #                 return datos_anteriores if datos_anteriores else None
# # # # # # # #             # Para otros errores HTTP, reintentar
# # # # # # # #             if intento < max_intentos - 1:
# # # # # # # #                 time.sleep(1)
# # # # # # # #                 continue
# # # # # # # #             return datos_anteriores if datos_anteriores else None
# # # # # # # #         except Exception:
# # # # # # # #             if intento < max_intentos - 1:
# # # # # # # #                 time.sleep(1)
# # # # # # # #                 continue
# # # # # # # #             return datos_anteriores if datos_anteriores else None
    
# # # # # # # #     return datos_anteriores if datos_anteriores else None

# # # # # # # # # ==============================
# # # # # # # # # AUTO-REFRESH (5 segundos para pruebas)
# # # # # # # # # ==============================
# # # # # # # # st_autorefresh(interval=5000, key="auto_refresh")

# # # # # # # # # ==============================
# # # # # # # # # CARGAR DATOS
# # # # # # # # # ==============================
# # # # # # # # if 'datos_cache' not in st.session_state:
# # # # # # # #     st.session_state.datos_cache = None

# # # # # # # # nuevos_datos = cargar_datos_github(st.session_state.datos_cache)
# # # # # # # # if nuevos_datos:
# # # # # # # #     st.session_state.datos_cache = nuevos_datos

# # # # # # # # datos = st.session_state.datos_cache
# # # # # # # # if not datos:
# # # # # # # #     st.markdown("""
# # # # # # # #         <div style="position:fixed;top:0;left:0;width:100%;height:100%;background:#0e1117;color:white;
# # # # # # # #                     display:flex;justify-content:center;align-items:center;font-family:Arial;">
# # # # # # # #             <div style="text-align:center;padding:20px;">
# # # # # # # #                 <h2>🛢️ SCADA Monitor</h2>
# # # # # # # #                 <p>Esperando primera conexión...</p>
# # # # # # # #                 <p style="font-size:12px;margin-top:10px;color:#7f8c8d">
# # # # # # # #                     {% if not token %}⚠️ Sin token de GitHub - Límite de 60 solicitudes/hora{% endif %}
# # # # # # # #                 </p>
# # # # # # # #             </div>
# # # # # # # #         </div>
# # # # # # # #         """, unsafe_allow_html=True)
# # # # # # # #     st.stop()

# # # # # # # # # ==============================
# # # # # # # # # GENERAR HTML+JS (mismo código corregido anterior)
# # # # # # # # # ==============================
# # # # # # # # datos_json = json.dumps(datos)

# # # # # # # # html_completo = f"""
# # # # # # # # <!DOCTYPE html>
# # # # # # # # <html lang="es">
# # # # # # # # <head>
# # # # # # # #     <meta charset="UTF-8">
# # # # # # # #     <meta name="viewport" content="width=device-width, initial-scale=1.0">
# # # # # # # #     <title>SCADA Monitor</title>
# # # # # # # #     <link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css" />
# # # # # # # #     <style>
# # # # # # # #         * {{ margin: 0; padding: 0; box-sizing: border-box; }}
# # # # # # # #         body {{ font-family: Arial, sans-serif; background: #0e1117; overflow: hidden; height: 100vh; width: 100vw; }}
# # # # # # # #         #map {{ position: absolute; top: 0; left: 0; width: 100%; height: 100%; z-index: 1; }}
# # # # # # # #         #stats-bar {{
# # # # # # # #             position: fixed;
# # # # # # # #             top: 10px;
# # # # # # # #             right: 15px;
# # # # # # # #             background: rgba(255, 255, 255, 0.95);
# # # # # # # #             padding: 6px 10px;
# # # # # # # #             border-radius: 6px;
# # # # # # # #             box-shadow: 0 2px 8px rgba(0,0,0,0.15);
# # # # # # # #             z-index: 1000;
# # # # # # # #             display: grid;
# # # # # # # #             grid-template-columns: repeat(7, auto);
# # # # # # # #             gap: 8px;
# # # # # # # #             align-items: center;
# # # # # # # #             font-family: Arial, sans-serif;
# # # # # # # #             font-size: 11px;
# # # # # # # #         }}
# # # # # # # #         .stat-value {{ font-weight: bold; color: #2c3e50; font-size: 14px; }}
# # # # # # # #         .stat-label {{ font-size: 7px; color: #7f8c8d; white-space: nowrap; }}
# # # # # # # #         .custom-popup {{ font-family: Arial; padding: 12px; min-width: 280px; background: white; border-radius: 6px; }}
# # # # # # # #         .custom-popup h4 {{ margin: 0 0 10px 0; color: #2c3e50; font-size: 16px; }}
# # # # # # # #         .custom-popup hr {{ margin: 8px 0; border-color: #ecf0f1; }}
# # # # # # # #         .custom-popup .var-row {{ margin: 6px 0; padding: 4px 0; display: flex; justify-content: space-between; font-size: 13px; }}
# # # # # # # #         .custom-popup .var-label {{ color: #7f8c8d; }}
# # # # # # # #         .custom-popup .var-value {{ font-weight: bold; color: #2c3e50; }}
# # # # # # # #         .custom-popup .timestamp {{ font-size: 11px; color: #95a5a6; text-align: center; margin-top: 8px; }}
# # # # # # # #         .status-online {{ color: #27ae60; font-weight: bold; }}
# # # # # # # #         .status-offline {{ color: #e74c3c; font-weight: bold; }}
# # # # # # # #     </style>
# # # # # # # # </head>
# # # # # # # # <body>
# # # # # # # #     <div id="map"></div>
# # # # # # # #     <div id="stats-bar">
# # # # # # # #         <div><div class="stat-value">📡 <span id="stat-total">0</span></div><div class="stat-label">Total Est.</div></div>
# # # # # # # #         <div><div class="stat-value" style="color:#27ae60">🟢 <span id="stat-encendidos">0</span></div><div class="stat-label">Pzs Off</div></div>
# # # # # # # #         <div><div class="stat-value" style="color:#e74c3c">🔴 <span id="stat-apagados">0</span></div><div class="stat-label">Pzs On</div></div>
# # # # # # # #         <div><div class="stat-value" style="color:#3498db">🔵 <span id="stat-tanques">0</span></div><div class="stat-label">Tanques</div></div>
# # # # # # # #         <div><div class="stat-value" style="color:#000">⚫ <span id="stat-offline">0</span></div><div class="stat-label">Offline</div></div>
# # # # # # # #         <div><div class="stat-value" style="color:#27ae60">✅ <span id="stat-online">0</span></div><div class="stat-label">Online</div></div>
# # # # # # # #         <div><div class="stat-value">🕐 <span id="stat-time">--:--</span></div><div class="stat-label">Actualizado</div></div>
# # # # # # # #     </div>

# # # # # # # #     <script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"></script>
# # # # # # # #     <script>
# # # # # # # #         const DATOS_INICIALES = {datos_json};
# # # # # # # #         let map = null;
# # # # # # # #         let markers = new Map();
# # # # # # # #         let primeraCarga = true;
        
# # # # # # # #         function initMap() {{
# # # # # # # #             map = L.map('map', {{
# # # # # # # #                 zoomControl: true,
# # # # # # # #                 scrollWheelZoom: true,
# # # # # # # #                 dragging: true
# # # # # # # #             }});
            
# # # # # # # #             L.tileLayer('https://{{s}}.basemaps.cartocdn.com/light_all/{{z}}/{{x}}/{{y}}{{r}}.png', {{
# # # # # # # #                 attribution: '',
# # # # # # # #                 subdomains: 'abcd',
# # # # # # # #                 maxZoom: 19
# # # # # # # #             }}).addTo(map);
            
# # # # # # # #             actualizarMapa(DATOS_INICIALES);
# # # # # # # #             actualizarEstadisticas(DATOS_INICIALES);
# # # # # # # #             document.getElementById('stat-time').textContent = new Date().toLocaleTimeString('es-ES', {{ hour: '2-digit', minute: '2-digit' }});
# # # # # # # #         }}
        
# # # # # # # #         function actualizarMapa(datos) {{
# # # # # # # #             if (!datos || !datos.estaciones) return;
# # # # # # # #             const nuevasBounds = [];
            
# # # # # # # #             datos.estaciones.forEach(estacion => {{
# # # # # # # #                 if (!estacion.latitud || !estacion.longitud) return;
# # # # # # # #                 const id = estacion.nombre || `${{estacion.latitud}},${{estacion.longitud}}`;
# # # # # # # #                 const lat = parseFloat(estacion.latitud);
# # # # # # # #                 const lng = parseFloat(estacion.longitud);
# # # # # # # #                 nuevasBounds.push([lat, lng]);
                
# # # # # # # #                 if (markers.has(id)) {{
# # # # # # # #                     const marker = markers.get(id);
# # # # # # # #                     marker.setPopupContent(crearPopupContent(estacion));
# # # # # # # #                     marker.setIcon(crearIcono(estacion.tipo, estacion.estado_bomba, estacion.en_linea));
# # # # # # # #                 }} else {{
# # # # # # # #                     const marker = L.marker([lat, lng], {{ 
# # # # # # # #                         icon: crearIcono(estacion.tipo, estacion.estado_bomba, estacion.en_linea)
# # # # # # # #                     }})
# # # # # # # #                     .bindPopup(crearPopupContent(estacion), {{ maxWidth: 320 }})
# # # # # # # #                     .bindTooltip(estacion.nombre || 'Estación', {{ 
# # # # # # # #                         permanent: false, 
# # # # # # # #                         direction: 'top',
# # # # # # # #                         opacity: 0.9
# # # # # # # #                     }})
# # # # # # # #                     .addTo(map);
# # # # # # # #                     markers.set(id, marker);
# # # # # # # #                 }}
# # # # # # # #             }});
            
# # # # # # # #             if (primeraCarga && nuevasBounds.length > 0) {{
# # # # # # # #                 map.fitBounds(nuevasBounds, {{ padding: [40, 40] }});
# # # # # # # #                 primeraCarga = false;
# # # # # # # #             }}
# # # # # # # #         }}
        
# # # # # # # #         function crearIcono(tipo, estado, enLinea) {{
# # # # # # # #             let color = '#000000';
# # # # # # # #             if (enLinea !== 0) {{
# # # # # # # #                 if (tipo === 'pozo' || tipo === 'bomba') {{
# # # # # # # #                     color = estado === 1 ? '#27ae60' : '#e74c3c';
# # # # # # # #                 }} else if (tipo === 'tanque') {{
# # # # # # # #                     color = estado === 1 ? '#3498db' : '#95a5a6';
# # # # # # # #                 }} else if (tipo === 'sensor') {{
# # # # # # # #                     color = '#9b59b6';
# # # # # # # #                 }} else {{
# # # # # # # #                     color = '#f39c12';
# # # # # # # #                 }}
# # # # # # # #             }}
            
# # # # # # # #             let iconClass = 'fa-tint';
# # # # # # # #             if (tipo === 'tanque') iconClass = 'fa-water';
# # # # # # # #             else if (tipo === 'bomba') iconClass = 'fa-cog';
# # # # # # # #             else if (tipo === 'sensor') iconClass = 'fa-microchip';
            
# # # # # # # #             return L.divIcon({{
# # # # # # # #                 html: `<div style="background:${{color}};width:32px;height:32px;border-radius:50%;display:flex;align-items:center;justify-content:center;box-shadow:0 2px 6px rgba(0,0,0,0.4);"><i class="fa ${{iconClass}}" style="color:white;font-size:16px;"></i></div>`,
# # # # # # # #                 className: '',
# # # # # # # #                 iconSize: [32, 32],
# # # # # # # #                 iconAnchor: [16, 16],
# # # # # # # #                 popupAnchor: [0, -16]
# # # # # # # #             }});
# # # # # # # #         }}
        
# # # # # # # #         function crearPopupContent(estacion) {{
# # # # # # # #             let html = `<div class="custom-popup"><h4>${{estacion.nombre || 'Estación'}}</h4><hr>`;
            
# # # # # # # #             const enLinea = estacion.en_linea !== undefined ? parseInt(estacion.en_linea) : 1;
# # # # # # # #             const estadoLinea = enLinea === 1 ? '<span class="status-online">En línea</span>' : '<span class="status-offline">Fuera de línea</span>';
# # # # # # # #             html += `<div class="var-row"><span class="var-label">Estado conexión:</span><span class="var-value">${{estadoLinea}}</span></div>`;
            
# # # # # # # #             for (const key in estacion) {{
# # # # # # # #                 if (!['nombre', 'latitud', 'longitud', 'tipo', 'estado_bomba', 'en_linea', 'icono'].includes(key)) {{
# # # # # # # #                     const value = typeof estacion[key] === 'number' 
# # # # # # # #                         ? estacion[key].toLocaleString('es-ES', {{ minimumFractionDigits: 2, maximumFractionDigits: 2 }})
# # # # # # # #                         : estacion[key];
# # # # # # # #                     html += `<div class="var-row"><span class="var-label">${{key}}:</span><span class="var-value">${{value}}</span></div>`;
# # # # # # # #                 }}
# # # # # # # #             }}
            
# # # # # # # #             html += `<hr><div class="timestamp">📅 ${{new Date().toLocaleString('es-ES')}}</div></div>`;
# # # # # # # #             return html;
# # # # # # # #         }}
        
# # # # # # # #         function actualizarEstadisticas(datos) {{
# # # # # # # #             if (!datos || !datos.estaciones) return;
            
# # # # # # # #             let total = 0;
# # # # # # # #             let pozos_encendidos = 0;
# # # # # # # #             let pozos_apagados = 0;
# # # # # # # #             let tanques = 0;
# # # # # # # #             let offline = 0;
# # # # # # # #             let online = 0;
            
# # # # # # # #             datos.estaciones.forEach(estacion => {{
# # # # # # # #                 total++;
# # # # # # # #                 const enLinea = estacion.en_linea !== undefined ? parseInt(estacion.en_linea) : 1;
# # # # # # # #                 const tipo = estacion.tipo || 'otro';
# # # # # # # #                 const estado = estacion.estado_bomba !== undefined ? parseInt(estacion.estado_bomba) : (estacion.estado !== undefined ? parseInt(estacion.estado) : 0);
                
# # # # # # # #                 if (enLinea === 0) {{
# # # # # # # #                     offline++;
# # # # # # # #                 }} else {{
# # # # # # # #                     online++;
# # # # # # # #                     if (tipo === 'pozo') {{
# # # # # # # #                         if (estado === 1) {{
# # # # # # # #                             pozos_encendidos++;
# # # # # # # #                         }} else {{
# # # # # # # #                             pozos_apagados++;
# # # # # # # #                         }}
# # # # # # # #                     }} else if (tipo === 'tanque') {{
# # # # # # # #                         tanques++;
# # # # # # # #                     }}
# # # # # # # #                 }}
# # # # # # # #             }});
            
# # # # # # # #             document.getElementById('stat-total').textContent = total;
# # # # # # # #             document.getElementById('stat-encendidos').textContent = pozos_encendidos;
# # # # # # # #             document.getElementById('stat-apagados').textContent = pozos_apagados;
# # # # # # # #             document.getElementById('stat-tanques').textContent = tanques;
# # # # # # # #             document.getElementById('stat-offline').textContent = offline;
# # # # # # # #             document.getElementById('stat-online').textContent = online;
# # # # # # # #         }}
        
# # # # # # # #         document.addEventListener('DOMContentLoaded', initMap);
# # # # # # # #     </script>
# # # # # # # #     <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
# # # # # # # # </body>
# # # # # # # # </html>
# # # # # # # # """

# # # # # # # # st.components.v1.html(
# # # # # # # #     html_completo,
# # # # # # # #     width=1920,
# # # # # # # #     height=1080,
# # # # # # # #     scrolling=False
# # # # # # # # )



# # # # # # # import streamlit as st
# # # # # # # import requests
# # # # # # # import json
# # # # # # # import base64
# # # # # # # from datetime import datetime
# # # # # # # from streamlit_autorefresh import st_autorefresh
# # # # # # # import time
# # # # # # # import os

# # # # # # # # Configuración minimalista
# # # # # # # st.set_page_config(
# # # # # # #     page_title="SCADA Monitor",
# # # # # # #     layout="wide",
# # # # # # #     initial_sidebar_state="collapsed"
# # # # # # # )

# # # # # # # # CSS AGRESIVO - VALORES EN NEGRITA
# # # # # # # st.markdown("""
# # # # # # #     <style>
# # # # # # #     [data-testid="stSidebar"] { display: none !important; }
# # # # # # #     [data-testid="stHeader"] { display: none !important; }
# # # # # # #     [data-testid="stDecoration"] { display: none !important; }
# # # # # # #     header { display: none !important; }
# # # # # # #     #MainMenu { display: none !important; }
# # # # # # #     footer { display: none !important; }
# # # # # # #     .stApp { background-color: #0e1117; padding: 0 !important; margin: 0 !important; overflow: hidden !important; }
# # # # # # #     .block-container { padding: 0 !important; max-width: 100% !important; margin: 0 !important; overflow: hidden !important; }
# # # # # # #     .main { padding: 0 !important; margin: 0 !important; overflow: hidden !important; }
# # # # # # #     .block-container > div { padding: 0 !important; margin: 0 !important; }
# # # # # # #     ::-webkit-scrollbar { display: none !important; }
# # # # # # #     body { overflow: hidden !important; }
    
# # # # # # #     /* Popup con valores en NEGRITA */
# # # # # # #     .custom-popup .var-label { 
# # # # # # #         color: #2c3e50 !important; 
# # # # # # #         font-weight: 600 !important; 
# # # # # # #         font-size: 13px !important;
# # # # # # #     }
# # # # # # #     .custom-popup .var-value { 
# # # # # # #         color: #2c3e50 !important; 
# # # # # # #         font-weight: bold !important; 
# # # # # # #         font-size: 14px !important;
# # # # # # #         text-align: right !important;
# # # # # # #     }
    
# # # # # # #     /* Mensaje de error */
# # # # # # #     .error-container {
# # # # # # #         position: fixed;
# # # # # # #         top: 50%;
# # # # # # #         left: 50%;
# # # # # # #         transform: translate(-50%, -50%);
# # # # # # #         background: rgba(231, 76, 60, 0.95);
# # # # # # #         color: white;
# # # # # # #         padding: 30px;
# # # # # # #         border-radius: 15px;
# # # # # # #         box-shadow: 0 10px 40px rgba(0,0,0,0.5);
# # # # # # #         max-width: 600px;
# # # # # # #         text-align: center;
# # # # # # #         z-index: 9999;
# # # # # # #         border: 3px solid white;
# # # # # # #     }
# # # # # # #     .error-title { font-size: 28px; font-weight: bold; margin-bottom: 15px; }
# # # # # # #     .error-message { font-size: 16px; margin-bottom: 20px; line-height: 1.5; }
# # # # # # #     .error-fix { background: rgba(0,0,0,0.3); padding: 15px; border-radius: 8px; margin-top: 15px; font-family: monospace; font-size: 14px; text-align: left; }
# # # # # # #     .error-footer { font-size: 12px; margin-top: 20px; opacity: 0.9; }
# # # # # # #     </style>
# # # # # # #     """, unsafe_allow_html=True)

# # # # # # # # ==============================
# # # # # # # # OBTENER TOKEN DE GITHUB
# # # # # # # # ==============================
# # # # # # # def obtener_token_github():
# # # # # # #     try:
# # # # # # #         if hasattr(st, 'secrets') and "GITHUB_TOKEN" in st.secrets:
# # # # # # #             return st.secrets["GITHUB_TOKEN"]
# # # # # # #     except:
# # # # # # #         pass
# # # # # # #     return os.getenv("GITHUB_TOKEN", None)

# # # # # # # # ==============================
# # # # # # # # CARGAR DATOS CON VALIDACIÓN DE JSON
# # # # # # # # ==============================
# # # # # # # def cargar_datos_github(datos_anteriores=None, max_intentos=3):
# # # # # # #     token = obtener_token_github()
    
# # # # # # #     for intento in range(max_intentos):
# # # # # # #         try:
# # # # # # #             GITHUB_USER = "AlarmasCiateq"
# # # # # # #             REPO_NAME = "SCADA_T"
# # # # # # #             BRANCH = "main"
# # # # # # #             FILE_PATH = "datos_estaciones.json"
            
# # # # # # #             api_url = f"https://api.github.com/repos/{GITHUB_USER}/{REPO_NAME}/contents/{FILE_PATH}?ref={BRANCH}"
            
# # # # # # #             headers = {
# # # # # # #                 'User-Agent': f'SCADA-Monitor-{datetime.now().timestamp()}',
# # # # # # #                 'Accept': 'application/vnd.github.v3+json'
# # # # # # #             }
            
# # # # # # #             if token:
# # # # # # #                 headers['Authorization'] = f'token {token}'
            
# # # # # # #             response = requests.get(api_url, headers=headers, timeout=10)
# # # # # # #             response.raise_for_status()
            
# # # # # # #             data = response.json()
# # # # # # #             content_bytes = base64.b64decode(data['content'])
# # # # # # #             content_str = content_bytes.decode('utf-8')
            
# # # # # # #             try:
# # # # # # #                 datos = json.loads(content_str)
# # # # # # #                 return datos
# # # # # # #             except json.JSONDecodeError as e:
# # # # # # #                 st.markdown(f"""
# # # # # # #                     <div class="error-container">
# # # # # # #                         <div class="error-title">⚠️ ERROR EN ARCHIVO JSON</div>
# # # # # # #                         <div class="error-message">
# # # # # # #                             El archivo <strong>datos_estaciones.json</strong> tiene formato incorrecto.<br>
# # # # # # #                             <strong>Línea {e.lineno}, Columna {e.colno}:</strong> {str(e.msg)[:50]}
# # # # # # #                         </div>
# # # # # # #                         <div class="error-fix">
# # # # # # # <strong>Solución:</strong><br>
# # # # # # # 1. Corrige el JSON en GitHub<br>
# # # # # # # 2. Usa validador: <a href="https://jsonlint.com" target="_blank" style="color:#3498db;text-decoration:underline">jsonlint.com</a><br>
# # # # # # # 3. Verifica comas y comillas
# # # # # # #                         </div>
# # # # # # #                         <div class="error-footer">
# # # # # # #                             ⏳ Reintentando en 10 segundos... | {datetime.now().strftime('%H:%M:%S')}
# # # # # # #                         </div>
# # # # # # #                     </div>
# # # # # # #                     """, unsafe_allow_html=True)
# # # # # # #                 time.sleep(10)
# # # # # # #                 st.rerun()
# # # # # # #                 return datos_anteriores if datos_anteriores else None
                
# # # # # # #         except requests.exceptions.HTTPError as e:
# # # # # # #             if e.response.status_code in [401, 403]:
# # # # # # #                 return datos_anteriores if datos_anteriores else None
# # # # # # #             if intento < max_intentos - 1:
# # # # # # #                 time.sleep(1)
# # # # # # #                 continue
# # # # # # #             return datos_anteriores if datos_anteriores else None
# # # # # # #         except Exception:
# # # # # # #             if intento < max_intentos - 1:
# # # # # # #                 time.sleep(1)
# # # # # # #                 continue
# # # # # # #             return datos_anteriores if datos_anteriores else None
    
# # # # # # #     return datos_anteriores if datos_anteriores else None

# # # # # # # # ==============================
# # # # # # # # AUTO-REFRESH
# # # # # # # # ==============================
# # # # # # # st_autorefresh(interval=5000, key="auto_refresh")

# # # # # # # # ==============================
# # # # # # # # CARGAR DATOS
# # # # # # # # ==============================
# # # # # # # if 'datos_cache' not in st.session_state:
# # # # # # #     st.session_state.datos_cache = None

# # # # # # # nuevos_datos = cargar_datos_github(st.session_state.datos_cache)
# # # # # # # if nuevos_datos:
# # # # # # #     st.session_state.datos_cache = nuevos_datos

# # # # # # # datos = st.session_state.datos_cache
# # # # # # # if not datos:
# # # # # # #     st.markdown("""
# # # # # # #         <div style="position:fixed;top:0;left:0;width:100%;height:100%;background:#0e1117;color:white;
# # # # # # #                     display:flex;justify-content:center;align-items:center;font-family:Arial;">
# # # # # # #             <div style="text-align:center;padding:20px;">
# # # # # # #                 <h2>🛢️ SCADA Monitor</h2>
# # # # # # #                 <p>Conectando con el sistema...</p>
# # # # # # #                 <p style="font-size:12px;margin-top:10px;color:#7f8c8d">
# # # # # # #                     Verificando datos en GitHub...
# # # # # # #                 </p>
# # # # # # #             </div>
# # # # # # #         </div>
# # # # # # #         """, unsafe_allow_html=True)
# # # # # # #     st.stop()

# # # # # # # # ==============================
# # # # # # # # GENERAR HTML+JS DEFINITIVO (OFFLINE = MISMO ICONO + FONDO NEGRO + BORDE ROJO)
# # # # # # # # ==============================
# # # # # # # datos_json = json.dumps(datos)

# # # # # # # html_completo = f"""
# # # # # # # <!DOCTYPE html>
# # # # # # # <html lang="es">
# # # # # # # <head>
# # # # # # #     <meta charset="UTF-8">
# # # # # # #     <meta name="viewport" content="width=device-width, initial-scale=1.0">
# # # # # # #     <title>SCADA Monitor</title>
# # # # # # #     <link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css" />
# # # # # # #     <style>
# # # # # # #         * {{ margin: 0; padding: 0; box-sizing: border-box; }}
# # # # # # #         body {{ font-family: Arial, sans-serif; background: #0e1117; overflow: hidden; height: 100vh; width: 100vw; }}
# # # # # # #         #map {{ position: absolute; top: 0; left: 0; width: 100%; height: 100%; z-index: 1; }}
# # # # # # #         #stats-bar {{
# # # # # # #             position: fixed;
# # # # # # #             top: 10px;
# # # # # # #             right: 15px;
# # # # # # #             background: rgba(255, 255, 255, 0.95);
# # # # # # #             padding: 6px 10px;
# # # # # # #             border-radius: 6px;
# # # # # # #             box-shadow: 0 2px 8px rgba(0,0,0,0.15);
# # # # # # #             z-index: 1000;
# # # # # # #             display: grid;
# # # # # # #             grid-template-columns: repeat(7, auto);
# # # # # # #             gap: 8px;
# # # # # # #             align-items: center;
# # # # # # #             font-family: Arial, sans-serif;
# # # # # # #             font-size: 11px;
# # # # # # #         }}
# # # # # # #         .stat-value {{ font-weight: bold; color: #2c3e50; font-size: 14px; }}
# # # # # # #         .stat-label {{ font-size: 7px; color: #7f8c8d; white-space: nowrap; }}
# # # # # # #         .custom-popup {{ font-family: Arial; padding: 12px; min-width: 280px; background: white; border-radius: 6px; }}
# # # # # # #         .custom-popup h4 {{ margin: 0 0 10px 0; color: #2c3e50; font-size: 16px; font-weight: bold; }}
# # # # # # #         .custom-popup hr {{ margin: 8px 0; border-color: #ecf0f1; }}
# # # # # # #         .custom-popup .var-row {{ margin: 6px 0; padding: 4px 0; display: flex; justify-content: space-between; }}
# # # # # # #         .custom-popup .var-label {{ 
# # # # # # #             color: #2c3e50; 
# # # # # # #             font-weight: 600; 
# # # # # # #             font-size: 13px; 
# # # # # # #             min-width: 120px;
# # # # # # #         }}
# # # # # # #         .custom-popup .var-value {{ 
# # # # # # #             color: #2c3e50; 
# # # # # # #             font-weight: bold; 
# # # # # # #             font-size: 14px; 
# # # # # # #             text-align: right;
# # # # # # #             min-width: 80px;
# # # # # # #         }}
# # # # # # #         .custom-popup .timestamp {{ font-size: 11px; color: #95a5a6; text-align: center; margin-top: 8px; }}
# # # # # # #         .status-online {{ color: #27ae60; font-weight: bold; }}
# # # # # # #         .status-offline {{ color: #e74c3c; font-weight: bold; }}
# # # # # # #     </style>
# # # # # # # </head>
# # # # # # # <body>
# # # # # # #     <div id="map"></div>
# # # # # # #     <div id="stats-bar">
# # # # # # #         <div><div class="stat-value">📡 <span id="stat-total">0</span></div><div class="stat-label">Total</div></div>
# # # # # # #         <div><div class="stat-value" style="color:#27ae60">🟢 <span id="stat-encendidos">0</span></div><div class="stat-label">Pozos Encendidos</div></div>
# # # # # # #         <div><div class="stat-value" style="color:#e74c3c">🔴 <span id="stat-apagados">0</span></div><div class="stat-label">Pozos Apagados</div></div>
# # # # # # #         <div><div class="stat-value" style="color:#3498db">🔵 <span id="stat-tanques">0</span></div><div class="stat-label">Tanques</div></div>
# # # # # # #         <div><div class="stat-value" style="color:#000">⚫ <span id="stat-offline">0</span></div><div class="stat-label">Offline</div></div>
# # # # # # #         <div><div class="stat-value" style="color:#27ae60">🟢 <span id="stat-online">0</span></div><div class="stat-label">Online</div></div>
# # # # # # #         <div><div class="stat-value">🕐 <span id="stat-time">--:--</span></div><div class="stat-label">Actualizado</div></div>
# # # # # # #     </div>

# # # # # # #     <script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"></script>
# # # # # # #     <script>
# # # # # # #         const DATOS_INICIALES = {datos_json};
# # # # # # #         let map = null;
# # # # # # #         let markers = new Map();
# # # # # # #         let primeraCarga = true;
        
# # # # # # #         // LIMPIAR URL
# # # # # # #         function limpiarUrl(url) {{
# # # # # # #             if (!url) return null;
# # # # # # #             return url.trim().replace(/\\s+/g, '%20');
# # # # # # #         }}
        
# # # # # # #         // SVG predeterminados por tipo (sin cambios)
# # # # # # #         function getDefaultSvg(tipo, color) {{
# # # # # # #             switch(tipo) {{
# # # # # # #                 case 'pozo': return `<svg xmlns="http://www.w3.org/2000/svg" height="32" viewBox="0 -960 960 960" width="32" fill="${{color}}"><path d="M480-120q-108 0-196.5-54T132-300q-3-5-4.5-10t-1.5-11q0-12 7.5-23.5T160-364q8-8 18-11.5t21-3.5q11 0 21 3.5t18 11.5q5 5 8 10.5t5 12.5q0 11-6 21t-16 17q-56 44-94 102t-38 126q0 83 58.5 141.5T480-120Zm0-360q-33 0-56.5-23.5T400-560q0-33 23.5-56.5T480-640q33 0 56.5 23.5T560-560q0 33-23.5 56.5T480-480Z"/></svg>`;
# # # # # # #                 case 'tanque': return `<svg xmlns="http://www.w3.org/2000/svg" height="32" viewBox="0 -960 960 960" width="32" fill="${{color}}"><path d="M120-200v-560h160v-80h400v80h160v560H120Zm280-440Zm0 320q50 0 85-35t35-85q0-50-35-85t-85-35q-50 0-85 35t-35 85q0 50 35 85t85 35Zm0-160q21 0 35.5-14.5T480-440q0-21-14.5-35.5T430-490q-21 0-35.5 14.5T380-440q0 21 14.5 35.5T430-390Zm280 160v-80H600v80h110Zm0-160v-80H600v80h110Zm-440 160v-80H260v80h110Zm0-160v-80H260v80h110Z"/></svg>`;
# # # # # # #                 case 'bomba': return `<svg xmlns="http://www.w3.org/2000/svg" height="32" viewBox="0 -960 960 960" width="32" fill="${{color}}"><path d="M120-280h164q-17-17-31.5-37T227-360H120v80Zm360 0q83 0 141.5-58.5T680-480q0-83-58.5-141.5T480-680q-83 0-141.5 58.5T280-480q0 83 58.5 141.5T480-280Zm253-320h107v-80H676q17 17 31.5 37t25.5 43ZM40-160v-320h80v40h83q-2-10-2.5-19.5T200-480q0-117 81.5-198.5T480-760h360v-40h80v320h-80v-40h-83q2 10 2.5 19.5t.5 20.5q0 117-81.5 198.5T480-200H120v40H40Zm80-120v-80 80Zm720-320v-80 80ZM480-480Zm0 120q-33 0-56.5-23.5T400-440q0-23 9.5-45.5T446-550l34-50 34 50q27 42 36.5 64.5T560-440q0 33-23.5 56.5T480-360Z"/></svg>`;
# # # # # # #                 case 'sensor': return `<svg xmlns="http://www.w3.org/2000/svg" height="32" viewBox="0 -960 960 960" width="32" fill="${{color}}"><path d="M480-80q-83 0-156-31.5T197-197q-54-54-85.5-127T80-480q0-83 31.5-156T197-763q54-54 127-85.5T480-880q83 0 156 31.5T763-763q54 54 85.5 127T880-480q0 83-31.5 156T763-197q-54 54-127 85.5T480-80Zm0-80q134 0 227-93t93-227q0-134-93-227t-227-93q-134 0-227 93t-93 227q0 134 93 227t227 93Zm0-320Z"/></svg>`;
# # # # # # #                 default: return `<svg xmlns="http://www.w3.org/2000/svg" height="32" viewBox="0 -960 960 960" width="32" fill="${{color}}"><path d="M480-280q17 0 28.5-11.5T520-320q0-17-11.5-28.5T480-360q-17 0-28.5 11.5T440-320q0 17 11.5 28.5T480-280Zm-40-160h80v-320h-80v320Zm40 240q-83 0-156-31.5T197-287q-54-54-85.5-127T80-560q0-83 31.5-156T197-843q54-54 127-85.5T480-960q83 0 156 31.5T763-843q54 54 85.5 127T880-560q0 83-31.5 156T763-287q-54 54-127 85.5T480-170Zm0-80q116 0 198-82t82-198q0-116-82-198t-198-82q-116 0-198 82t-82 198q0 116 82 198t198 82Zm0-280Z"/></svg>`;
# # # # # # #             }}
# # # # # # #         }}
        
# # # # # # #         // Detecta campo de porcentaje
# # # # # # #         function obtenerNivelTanque(estacion) {{
# # # # # # #             const campos = ['Porcentaje (%)', 'Porcentaje', 'Nivel (%)', 'nivel_%', 'Nivel', 'nivel'];
# # # # # # #             for (let campo of campos) {{
# # # # # # #                 if (estacion[campo] !== undefined) {{
# # # # # # #                     let v = parseFloat(estacion[campo]);
# # # # # # #                     return Math.max(0, Math.min(100, isNaN(v) ? 0 : v));
# # # # # # #                 }}
# # # # # # #             }}
# # # # # # #             return 0;
# # # # # # #         }}
        
# # # # # # #         // Lógica robusta para offline
# # # # # # #         function esOffline(enLinea) {{
# # # # # # #             if (enLinea === undefined || enLinea === null) return false;
# # # # # # #             const valor = String(enLinea).trim().toLowerCase();
# # # # # # #             return valor === '0' || valor === 'false' || valor === 'off' || valor === 'no';
# # # # # # #         }}
        
# # # # # # #         // BARRA DE LLENADO VERTICAL SIN BORDES
# # # # # # #         function crearIconoTanque(iconoUrl, nivel) {{
# # # # # # #             const alturaLlenado = Math.round((nivel / 100) * 24);
            
# # # # # # #             if (iconoUrl) {{
# # # # # # #                 return L.divIcon({{
# # # # # # #                     html: `<div style="position:relative;width:32px;height:32px;">
# # # # # # #                         <img src="${{iconoUrl}}" width="32" height="32" style="position:absolute;top:0;left:0;opacity:0.3;">
# # # # # # #                         <div style="
# # # # # # #                             position:absolute;
# # # # # # #                             bottom:4px;
# # # # # # #                             left:2px;
# # # # # # #                             width:28px;
# # # # # # #                             height:${{alturaLlenado}}px;
# # # # # # #                             background:rgba(52,152,219,0.95);
# # # # # # #                             border-radius:2px 2px 0 0;
# # # # # # #                         "></div>
# # # # # # #                         <div style="
# # # # # # #                             position:absolute;
# # # # # # #                             bottom:6px;
# # # # # # #                             width:32px;
# # # # # # #                             text-align:center;
# # # # # # #                             font-size:9px;
# # # # # # #                             color:white;
# # # # # # #                             font-weight:bold;
# # # # # # #                             text-shadow:0 1px 2px rgba(0,0,0,0.8);
# # # # # # #                         ">${{Math.round(nivel)}}%</div>
# # # # # # #                     </div>`,
# # # # # # #                     iconSize: [32, 32],
# # # # # # #                     iconAnchor: [16, 16],
# # # # # # #                     popupAnchor: [0, -16]
# # # # # # #                 }});
# # # # # # #             }} else {{
# # # # # # #                 const yInicio = 28 - alturaLlenado;
# # # # # # #                 const svg = `<svg xmlns="http://www.w3.org/2000/svg" width="32" height="32" viewBox="0 0 32 32">
# # # # # # #                     <rect x="2" y="4" width="28" height="24" fill="#ecf0f1" rx="2"/>
# # # # # # #                     <rect x="3" y="${{yInicio}}" width="26" height="${{alturaLlenado}}" fill="#3498db" rx="1"/>
# # # # # # #                     <text x="16" y="20" font-family="Arial" font-size="9" fill="#2c3e50" text-anchor="middle" font-weight="bold">${{Math.round(nivel)}}%</text>
# # # # # # #                 </svg>`;
# # # # # # #                 return L.divIcon({{
# # # # # # #                     html: svg,
# # # # # # #                     iconSize: [32, 32],
# # # # # # #                     iconAnchor: [16, 16],
# # # # # # #                     popupAnchor: [0, -16]
# # # # # # #                 }});
# # # # # # #             }}
# # # # # # #         }}
        
# # # # # # #         // CORREGIDO DEFINITIVO: OFFLINE = MISMO ICONO + FONDO NEGRO + BORDE ROJO (3px)
# # # # # # #         function crearIcono(estacion) {{
# # # # # # #             const tipo = estacion.tipo || 'otro';
# # # # # # #             const enLineaRaw = estacion.en_linea;
# # # # # # #             const offline = esOffline(enLineaRaw);
# # # # # # #             const estado = parseInt(estacion.estado_bomba || estacion.estado || 0);
# # # # # # #             const icono_url_on = limpiarUrl(estacion.icono_url_on);
# # # # # # #             const icono_url_off = limpiarUrl(estacion.icono_url_off);
# # # # # # #             const nivel = obtenerNivelTanque(estacion);
            
# # # # # # #             // OFFLINE: MISMO ICONO QUE TENDRÍA ONLINE + FONDO NEGRO + BORDE ROJO (3px)
# # # # # # #             if (offline) {{
# # # # # # #                 let iconContent;
                
# # # # # # #                 // Determinar qué icono usaría si estuviera online (mismo color y tipo)
# # # # # # #                 if (tipo === 'tanque') {{
# # # # # # #                     // Para tanque offline, usar barra de llenado con nivel actual (sin icono personalizado)
# # # # # # #                     const alturaLlenado = Math.round((nivel / 100) * 24);
# # # # # # #                     const yInicio = 28 - alturaLlenado;
# # # # # # #                     iconContent = `<svg xmlns="http://www.w3.org/2000/svg" width="28" height="28" viewBox="0 0 32 32">
# # # # # # #                         <rect x="2" y="4" width="28" height="24" fill="#ecf0f1" rx="2"/>
# # # # # # #                         <rect x="3" y="${{yInicio}}" width="26" height="${{alturaLlenado}}" fill="#3498db" rx="1"/>
# # # # # # #                         <text x="16" y="20" font-family="Arial" font-size="8" fill="#2c3e50" text-anchor="middle">${{Math.round(nivel)}}%</text>
# # # # # # #                     </svg>`;
# # # # # # #                 }} else if (estado === 1 && icono_url_on) {{
# # # # # # #                     // Icono personalizado ON (pero offline)
# # # # # # #                     iconContent = `<img src="${{icono_url_on}}" width="28" height="28" style="opacity:0.7;">`;
# # # # # # #                 }} else if (estado === 0 && icono_url_off) {{
# # # # # # #                     // Icono personalizado OFF (pero offline)
# # # # # # #                     iconContent = `<img src="${{icono_url_off}}" width="28" height="28" style="opacity:0.7;">`;
# # # # # # #                 }} else {{
# # # # # # #                     // SVG predeterminado con color según estado (pero offline)
# # # # # # #                     let color = '#f39c12';
# # # # # # #                     if (tipo === 'pozo' || tipo === 'bomba') {{
# # # # # # #                         color = estado === 1 ? '#27ae60' : '#e74c3c';
# # # # # # #                     }} else if (tipo === 'sensor') {{
# # # # # # #                         color = '#9b59b6';
# # # # # # #                     }}
# # # # # # #                     // Obtener SVG y reducir a 28x28
# # # # # # #                     let svg = getDefaultSvg(tipo, color);
# # # # # # #                     svg = svg.replace('width="32"', 'width="28"').replace('height="32"', 'height="28"');
# # # # # # #                     iconContent = svg;
# # # # # # #                 }}
                
# # # # # # #                 // Contenedor: FONDO NEGRO + BORDE ROJO (3px) + MISMO ICONO QUE ONLINE
# # # # # # #                 return L.divIcon({{
# # # # # # #                     html: `<div style="
# # # # # # #                         width: 32px;
# # # # # # #                         height: 32px;
# # # # # # #                         //background: #000;
# # # # # # #                         border: 3px solid #e74c3c;
# # # # # # #                         border-radius: 4px;
# # # # # # #                         display: flex;
# # # # # # #                         align-items: center;
# # # # # # #                         justify-content: center;
# # # # # # #                         box-sizing: border-box;
# # # # # # #                         box-shadow: 0 2px 8px rgba(0,0,0,0.5);
# # # # # # #                     ">${{iconContent}}</div>`,
# # # # # # #                     iconSize: [32, 32],
# # # # # # #                     iconAnchor: [16, 16],
# # # # # # #                     popupAnchor: [0, -16]
# # # # # # #                 }});
# # # # # # #             }}
            
# # # # # # #             // ONLINE: SIN FONDOS NI BORDES (solo el icono)
# # # # # # #             if (tipo === 'tanque') {{
# # # # # # #                 const iconoUrl = estado === 1 ? icono_url_on : icono_url_off;
# # # # # # #                 return crearIconoTanque(iconoUrl, nivel);
# # # # # # #             }}
            
# # # # # # #             if (estado === 1 && icono_url_on) {{
# # # # # # #                 return L.icon({{
# # # # # # #                     iconUrl: icono_url_on,
# # # # # # #                     iconSize: [32, 32],
# # # # # # #                     iconAnchor: [16, 16],
# # # # # # #                     popupAnchor: [0, -16]
# # # # # # #                 }});
# # # # # # #             }} else if (estado === 0 && icono_url_off) {{
# # # # # # #                 return L.icon({{
# # # # # # #                     iconUrl: icono_url_off,
# # # # # # #                     iconSize: [32, 32],
# # # # # # #                     iconAnchor: [16, 16],
# # # # # # #                     popupAnchor: [0, -16]
# # # # # # #                 }});
# # # # # # #             }}
            
# # # # # # #             // SVG predeterminado sin círculo
# # # # # # #             let color = '#f39c12';
# # # # # # #             if (tipo === 'pozo' || tipo === 'bomba') {{
# # # # # # #                 color = estado === 1 ? '#27ae60' : '#e74c3c';
# # # # # # #             }} else if (tipo === 'sensor') {{
# # # # # # #                 color = '#9b59b6';
# # # # # # #             }} else if (tipo === 'tanque') {{
# # # # # # #                 color = nivel >= 50 ? '#3498db' : '#95a5a6';
# # # # # # #             }}
            
# # # # # # #             const svg = getDefaultSvg(tipo, color);
# # # # # # #             return L.divIcon({{
# # # # # # #                 html: svg,
# # # # # # #                 iconSize: [32, 32],
# # # # # # #                 iconAnchor: [16, 16],
# # # # # # #                 popupAnchor: [0, -16]
# # # # # # #             }});
# # # # # # #         }}
        
# # # # # # #         function initMap() {{
# # # # # # #             map = L.map('map', {{
# # # # # # #                 zoomControl: true,
# # # # # # #                 scrollWheelZoom: true,
# # # # # # #                 dragging: true
# # # # # # #             }});
            
# # # # # # #             L.tileLayer('https://{{s}}.basemaps.cartocdn.com/light_all/{{z}}/{{x}}/{{y}}{{r}}.png', {{
# # # # # # #                 attribution: '',
# # # # # # #                 subdomains: 'abcd',
# # # # # # #                 maxZoom: 19
# # # # # # #             }}).addTo(map);
            
# # # # # # #             actualizarMapa(DATOS_INICIALES);
# # # # # # #             actualizarEstadisticas(DATOS_INICIALES);
# # # # # # #             document.getElementById('stat-time').textContent = new Date().toLocaleTimeString('es-ES', {{ hour: '2-digit', minute: '2-digit' }});
# # # # # # #         }}
        
# # # # # # #         function actualizarMapa(datos) {{
# # # # # # #             if (!datos || !datos.estaciones) return;
# # # # # # #             const nuevasBounds = [];
            
# # # # # # #             datos.estaciones.forEach(estacion => {{
# # # # # # #                 if (!estacion.latitud || !estacion.longitud) return;
# # # # # # #                 const id = estacion.nombre || `${{estacion.latitud}},${{estacion.longitud}}`;
# # # # # # #                 const lat = parseFloat(estacion.latitud);
# # # # # # #                 const lng = parseFloat(estacion.longitud);
# # # # # # #                 nuevasBounds.push([lat, lng]);
                
# # # # # # #                 if (markers.has(id)) {{
# # # # # # #                     const marker = markers.get(id);
# # # # # # #                     marker.setPopupContent(crearPopupContent(estacion));
# # # # # # #                     marker.setIcon(crearIcono(estacion));
# # # # # # #                 }} else {{
# # # # # # #                     const marker = L.marker([lat, lng], {{ icon: crearIcono(estacion) }})
# # # # # # #                     .bindPopup(crearPopupContent(estacion), {{ maxWidth: 320 }})
# # # # # # #                     .bindTooltip(estacion.nombre || 'Estación', {{ 
# # # # # # #                         permanent: false, 
# # # # # # #                         direction: 'top',
# # # # # # #                         opacity: 0.9
# # # # # # #                     }})
# # # # # # #                     .addTo(map);
# # # # # # #                     markers.set(id, marker);
# # # # # # #                 }}
# # # # # # #             }});
            
# # # # # # #             if (primeraCarga && nuevasBounds.length > 0) {{
# # # # # # #                 map.fitBounds(nuevasBounds, {{ padding: [40, 40] }});
# # # # # # #                 primeraCarga = false;
# # # # # # #             }}
# # # # # # #         }}
        
# # # # # # #         function crearPopupContent(estacion) {{
# # # # # # #             let html = `<div class="custom-popup"><h4>${{estacion.nombre || 'Estación'}}</h4><hr>`;
            
# # # # # # #             const offline = esOffline(estacion.en_linea);
# # # # # # #             const estadoLinea = offline ? '<span class="status-offline">Fuera de línea</span>' : '<span class="status-online">En línea</span>';
# # # # # # #             html += `<div class="var-row"><span class="var-label">Estado:</span><span class="var-value">${{estadoLinea}}</span></div>`;
            
# # # # # # #             if (estacion.tipo === 'tanque') {{
# # # # # # #                 html += `<div class="var-row"><span class="var-label">Nivel:</span><span class="var-value">${{obtenerNivelTanque(estacion)}}%</span></div>`;
# # # # # # #             }}
            
# # # # # # #             for (const key in estacion) {{
# # # # # # #                 if (!['nombre', 'latitud', 'longitud', 'tipo', 'estado_bomba', 'en_linea', 'icono', 'icono_url', 'icono_url_on', 'icono_url_off', 'Nivel', 'nivel', 'Porcentaje (%)', 'Porcentaje'].includes(key)) {{
# # # # # # #                     const value = typeof estacion[key] === 'number' 
# # # # # # #                         ? estacion[key].toLocaleString('es-ES', {{ minimumFractionDigits: 2, maximumFractionDigits: 2 }})
# # # # # # #                         : estacion[key];
# # # # # # #                     html += `<div class="var-row"><span class="var-label">${{key}}:</span><span class="var-value">${{value}}</span></div>`;
# # # # # # #                 }}
# # # # # # #             }}
            
# # # # # # #             html += `<hr><div class="timestamp">📅 ${{new Date().toLocaleString('es-ES')}}</div></div>`;
# # # # # # #             return html;
# # # # # # #         }}
        
# # # # # # #         function actualizarEstadisticas(datos) {{
# # # # # # #             if (!datos || !datos.estaciones) return;
            
# # # # # # #             let total = 0, pozos_encendidos = 0, pozos_apagados = 0, tanques = 0, offline = 0, online = 0;
            
# # # # # # #             datos.estaciones.forEach(estacion => {{
# # # # # # #                 total++;
# # # # # # #                 const offline = esOffline(estacion.en_linea);
                
# # # # # # #                 if (offline) {{
# # # # # # #                     offline++;
# # # # # # #                 }} else {{
# # # # # # #                     online++;
# # # # # # #                     const tipo = estacion.tipo || 'otro';
# # # # # # #                     const estado = parseInt(estacion.estado_bomba || estacion.estado || 0);
                    
# # # # # # #                     if (tipo === 'pozo') {{
# # # # # # #                         if (estado === 1) pozos_encendidos++;
# # # # # # #                         else pozos_apagados++;
# # # # # # #                     }} else if (tipo === 'tanque') {{
# # # # # # #                         tanques++;
# # # # # # #                     }}
# # # # # # #                 }}
# # # # # # #             }});
            
# # # # # # #             document.getElementById('stat-total').textContent = total;
# # # # # # #             document.getElementById('stat-encendidos').textContent = pozos_encendidos;
# # # # # # #             document.getElementById('stat-apagados').textContent = pozos_apagados;
# # # # # # #             document.getElementById('stat-tanques').textContent = tanques;
# # # # # # #             document.getElementById('stat-offline').textContent = offline;
# # # # # # #             document.getElementById('stat-online').textContent = online;
# # # # # # #         }}
        
# # # # # # #         document.addEventListener('DOMContentLoaded', initMap);
# # # # # # #     </script>
# # # # # # # </body>
# # # # # # # </html>
# # # # # # # """

# # # # # # # st.components.v1.html(
# # # # # # #     html_completo,
# # # # # # #     width=1920,
# # # # # # #     height=1080,
# # # # # # #     scrolling=False
# # # # # # # )


# # # # import streamlit as st
# # # # import requests
# # # # import json
# # # # import base64
# # # # from datetime import datetime
# # # # import os
# # # # import time

# # # # # ========================================
# # # # # FUNCIÓN PARA OBTENER EL FAVICON DESDE GITHUB
# # # # # ========================================
# # # # def obtener_favicon_github():
# # # #     """Descarga el icono de GitHub y lo convierte a base64"""
# # # #     try:
# # # #         GITHUB_USER = "AlarmasCiateq"
# # # #         REPO_NAME = "SCADA_T"
# # # #         BRANCH = "main"
# # # #         ICON_PATH = "iconos/ICONO CIATEQ 256.ico"  # Ajusta la ruta si es necesario
        
# # # #         # URL para descargar el archivo RAW (no la API)
# # # #         raw_url = f"https://raw.githubusercontent.com/{GITHUB_USER}/{REPO_NAME}/{BRANCH}/{ICON_PATH}"
# # # #         print(raw_url)
# # # #         headers = {'User-Agent': 'SCADA-Monitor'}
# # # #         response = requests.get(raw_url, headers=headers, timeout=10)
# # # #         response.raise_for_status()
        
# # # #         # Convertir a base64
# # # #         icon_base64 = base64.b64encode(response.content).decode('utf-8')
# # # #         return f"data:image/x-icon;base64,{icon_base64}"
# # # #     except Exception as e:
# # # #         print(f"Error cargando favicon: {e}")
# # # #         return None

# # # # # ========================================
# # # # # CONFIGURACIÓN DE PÁGINA
# # # # # ========================================
# # # # # Intentar obtener el favicon de GitHub
# # # # favicon_data = obtener_favicon_github()

# # # # if favicon_data:
# # # #     # Streamlit no soporta directamente data URLs en page_icon,
# # # #     # pero podemos inyectarlo con HTML después
# # # #     st.set_page_config(
# # # #         page_title="SCADA CIATEQ",
# # # #         page_icon="🌎",  # Usamos un emoji temporal
# # # #         layout="wide",
# # # #         initial_sidebar_state="collapsed"
# # # #     )
    
# # # #     # Inyectar el favicon personalizado vía HTML
# # # #     st.markdown(f"""
# # # #     <link rel="icon" href="{favicon_data}" type="image/x-icon">
# # # #     <link rel="shortcut icon" href="{favicon_data}" type="image/x-icon">
# # # #     """, unsafe_allow_html=True)
# # # # else:
# # # #     # Fallback al emoji si no se pudo cargar el icono
# # # #     st.set_page_config(
# # # #         page_title="SCADA CIATEQ",
# # # #         page_icon="🏭",
# # # #         layout="wide",
# # # #         initial_sidebar_state="collapsed"
# # # #     )
# # # # # CSS AGRESIVO
# # # # st.markdown("""
# # # # <style>
# # # # [data-testid="stSidebar"] { display: none !important; }
# # # # [data-testid="stHeader"] { display: none !important; }
# # # # [data-testid="stDecoration"] { display: none !important; }
# # # # header { display: none !important; }
# # # # #MainMenu { display: none !important; }
# # # # footer { display: none !important; }
# # # # .stApp { background-color: #0e1117; padding: 0 !important; margin: 0 !important; overflow: hidden !important; }
# # # # .block-container { padding: 0 !important; max-width: 100% !important; margin: 0 !important; overflow: hidden !important; }
# # # # .main { padding: 0 !important; margin: 0 !important; overflow: hidden !important; }
# # # # .block-container > div { padding: 0 !important; margin: 0 !important; }
# # # # ::-webkit-scrollbar { display: none !important; }
# # # # body { overflow: hidden !important; }
# # # # #loading {
# # # #     position: fixed;
# # # #     top: 0;
# # # #     left: 0;
# # # #     width: 100%;
# # # #     height: 100%;
# # # #     background: #0e1117;
# # # #     display: flex;
# # # #     justify-content: center;
# # # #     align-items: center;
# # # #     color: #3498db;
# # # #     font-family: Arial;
# # # #     font-size: 18px;
# # # #     z-index: 9999;
# # # #     transition: opacity 0.1s;
# # # # }
# # # # #loading.hidden {
# # # #     opacity: 0;
# # # #     pointer-events: none;
# # # # }
# # # # #debug-timestamp {
# # # #     position: fixed;
# # # #     bottom: 5px;
# # # #     right: 10px;
# # # #     background: rgba(0,0,0,0.7);
# # # #     color: #27ae60;
# # # #     padding: 3px 8px;
# # # #     font-family: monospace;
# # # #     font-size: 11px;
# # # #     border-radius: 3px;
# # # #     z-index: 1000;
# # # # }
# # # # </style>
# # # # """, unsafe_allow_html=True)

# # # # # ========================================
# # # # # OBTENER TOKEN DE GITHUB
# # # # # ========================================
# # # # def obtener_token_github():
# # # #     try:
# # # #         if hasattr(st, 'secrets') and "GITHUB_TOKEN" in st.secrets:
# # # #             return st.secrets["GITHUB_TOKEN"]
# # # #     except:
# # # #         pass
# # # #     return os.getenv("GITHUB_TOKEN", None)

# # # # # ========================================
# # # # # CARGAR DATOS FRESH DE GITHUB (CADA EJECUCIÓN)
# # # # # ========================================
# # # # def cargar_datos_github(max_intentos=3):
# # # #     token = obtener_token_github()
# # # #     for intento in range(max_intentos):
# # # #         try:
# # # #             GITHUB_USER = "AlarmasCiateq"
# # # #             REPO_NAME = "SCADA_T"
# # # #             BRANCH = "main"
# # # #             FILE_PATH = "datos_estaciones.json"
            
# # # #             # URL CORREGIDA: SIN ESPACIOS
# # # #             api_url = f"https://api.github.com/repos/{GITHUB_USER}/{REPO_NAME}/contents/{FILE_PATH}?ref={BRANCH}"
            
# # # #             headers = {
# # # #                 'User-Agent': f'SCADA-Monitor-{datetime.now().timestamp()}',
# # # #                 'Accept': 'application/vnd.github.v3+json'
# # # #             }
            
# # # #             if token:
# # # #                 headers['Authorization'] = f'token {token}'
            
# # # #             response = requests.get(api_url, headers=headers, timeout=10)
# # # #             response.raise_for_status()
            
# # # #             data = response.json()
# # # #             content_bytes = base64.b64decode(data['content'])
# # # #             content_str = content_bytes.decode('utf-8')
# # # #             datos = json.loads(content_str)
            
# # # #             datos['_timestamp_actualizacion'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
# # # #             return datos, True
            
# # # #         except Exception as e:
# # # #             print(f"Error cargando datos (intento {intento + 1}): {e}")
# # # #             if intento < max_intentos - 1:
# # # #                 time.sleep(1)
# # # #                 continue
# # # #             return None, False
# # # #     return None, False

# # # # # ========================================
# # # # # CARGAR DATOS FRESH EN CADA EJECUCIÓN
# # # # # ========================================
# # # # datos, exito = cargar_datos_github()

# # # # if not datos or not exito:
# # # #     st.markdown("""
# # # #     <div style="position:fixed;top:0;left:0;width:100%;height:100%;background:#0e1117;color:white;
# # # #     display:flex;justify-content:center;align-items:center;font-family:Arial;">
# # # #         <div style="text-align:center;padding:20px;">
# # # #             <h2>🛢️ SCADA Monitor</h2>
# # # #             <p style="color:#e74c3c; margin-top:15px;">Error: No se pudieron cargar los datos de GitHub</p>
# # # #             <p style="font-size:14px; margin-top:10px; color:#95a5a6;">Verifique conexión a internet</p>
# # # #         </div>
# # # #     </div>
# # # #     """, unsafe_allow_html=True)
# # # #     time.sleep(60)
# # # #     st.rerun()

# # # # # ========================================
# # # # # PREPARAR DATOS PARA HTML
# # # # # ========================================
# # # # tiempo_str = datetime.now().strftime('%H:%M:%S')
# # # # timestamp_debug = datos.get('_timestamp_actualizacion', tiempo_str)

# # # # # Escapar JSON correctamente para JavaScript
# # # # datos_json_safe = json.dumps(datos, ensure_ascii=False)
# # # # datos_json_safe = (datos_json_safe.replace('\\', '\\\\')
# # # #     .replace("'", "\\'")
# # # #     .replace('</', '<\\/')
# # # #     .replace('\n', '\\n')
# # # #     .replace('\r', '\\r')
# # # #     .replace('\t', '\\t'))

# # # # # ========================================
# # # # # HTML + JAVASCRIPT (CORREGIDO - SENSOR CON BARRA DE NIVEL)
# # # # # ========================================
# # # # html_completo = """
# # # # <!DOCTYPE html>
# # # # <html lang="es">
# # # # <head>
# # # #     <meta charset="UTF-8">
# # # #     <meta name="viewport" content="width=device-width, initial-scale=1.0">
# # # #     <title>SCADA Monitor</title>
# # # #     <link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css" />
# # # #     <style>
# # # #         * { margin: 0; padding: 0; box-sizing: border-box; }
# # # #         body { font-family: Arial, sans-serif; background: #0e1117; overflow: hidden; height: 100vh; width: 100vw; }
# # # #         #map { position: absolute; top: 0; left: 0; width: 100%; height: 100%; z-index: 1; }
        
# # # #         #stats-bar {
# # # #             position: fixed;
# # # #             top: 10px;
# # # #             right: 15px;
# # # #             background: rgba(255, 255, 255, 0.95);
# # # #             padding: 8px;
# # # #             border-radius: 6px;
# # # #             box-shadow: 0 2px 8px rgba(0,0,0,0.15);
# # # #             z-index: 1000;
# # # #             display: flex;
# # # #             gap: 12px;
# # # #             align-items: center;
# # # #             font-family: Arial, sans-serif;
# # # #             flex-wrap: nowrap;
# # # #             overflow-x: auto;
# # # #             max-width: 90%;
# # # #         }
        
# # # #         .stat-item {
# # # #             display: flex;
# # # #             flex-direction: column;
# # # #             align-items: center;
# # # #             min-width: 65px;
# # # #         }
        
# # # #         .stat-icon {
# # # #             width: 24px;
# # # #             height: 24px;
# # # #             margin-bottom: 2px;
# # # #             display: flex;
# # # #             align-items: center;
# # # #             justify-content: center;
# # # #         }
        
# # # #         .stat-icon img {
# # # #             width: 100%;
# # # #             height: 100%;
# # # #             object-fit: contain;
# # # #         }
        
# # # #         .stat-value {
# # # #             font-weight: bold;
# # # #             color: #2c3e50;
# # # #             font-size: 14px;
# # # #             text-align: center;
# # # #         }
        
# # # #         .stat-label {
# # # #             font-size: 8px;
# # # #             color: #7f8c8d;
# # # #             text-align: center;
# # # #             white-space: nowrap;
# # # #             text-transform: uppercase;
# # # #             letter-spacing: 0.5px;
# # # #         }
        
# # # #         .custom-popup {
# # # #             font-family: Arial;
# # # #             padding: 12px;
# # # #             min-width: 280px;
# # # #             background: white;
# # # #             border-radius: 6px;
# # # #         }
        
# # # #         .custom-popup h4 {
# # # #             margin: 0 0 10px 0;
# # # #             color: #2c3e50;
# # # #             font-size: 16px;
# # # #             font-weight: bold;
# # # #         }
        
# # # #         .custom-popup hr {
# # # #             margin: 8px 0;
# # # #             border-color: #ecf0f1;
# # # #         }
        
# # # #         .custom-popup .var-row {
# # # #             margin: 6px 0;
# # # #             padding: 4px 0;
# # # #             display: flex;
# # # #             justify-content: space-between;
# # # #         }
        
# # # #         .custom-popup .var-label {
# # # #             color: #2c3e50;
# # # #             font-weight: 600;
# # # #             font-size: 13px;
# # # #             min-width: 120px;
# # # #         }
        
# # # #         .custom-popup .var-value {
# # # #             color: #2c3e50;
# # # #             font-weight: bold;
# # # #             font-size: 14px;
# # # #             text-align: right;
# # # #             min-width: 80px;
# # # #         }
        
# # # #         .custom-popup .timestamp {
# # # #             font-size: 11px;
# # # #             color: #95a5a6;
# # # #             text-align: center;
# # # #             margin-top: 8px;
# # # #         }
        
# # # #         .status-online { color: #27ae60; font-weight: bold; }
# # # #         .status-offline { color: #e74c3c; font-weight: bold; }
        
# # # #         #loading {
# # # #             position: fixed;
# # # #             top: 0;
# # # #             left: 0;
# # # #             width: 100%;
# # # #             height: 100%;
# # # #             background: #0e1117;
# # # #             display: flex;
# # # #             justify-content: center;
# # # #             align-items: center;
# # # #             color: #3498db;
# # # #             font-family: Arial;
# # # #             font-size: 18px;
# # # #             z-index: 9999;
# # # #             transition: opacity 0.1s;
# # # #         }
        
# # # #         #loading.hidden {
# # # #             opacity: 0;
# # # #             pointer-events: none;
# # # #         }
        
# # # #         #debug-timestamp {
# # # #             position: fixed;
# # # #             bottom: 5px;
# # # #             right: 10px;
# # # #             background: rgba(0,0,0,0.7);
# # # #             color: #27ae60;
# # # #             padding: 3px 8px;
# # # #             font-family: monospace;
# # # #             font-size: 11px;
# # # #             border-radius: 3px;
# # # #             z-index: 1000;
# # # #         }
        
# # # #         /* Botón de Vista General */
# # # #         .leaflet-control-zoom-all {
# # # #             background: #fff;
# # # #             border: 2px solid rgba(0,0,0,0.2);
# # # #             border-radius: 4px;
# # # #             box-shadow: 0 1px 5px rgba(0,0,0,0.4);
# # # #             cursor: pointer;
# # # #             margin-top: 5px;
# # # #             transition: all 0.2s;
# # # #         }
        
# # # #         .leaflet-control-zoom-all:hover {
# # # #             background: #f4f4f4;
# # # #             box-shadow: 0 1px 7px rgba(0,0,0,0.45);
# # # #         }
        
# # # #         .leaflet-control-zoom-all:active {
# # # #             background: #e8e8e8;
# # # #         }
        
# # # #         .leaflet-control-zoom-all i {
# # # #             display: block;
# # # #             width: 30px;
# # # #             height: 30px;
# # # #             line-height: 30px;
# # # #             text-align: center;
# # # #             font-weight: bold;
# # # #             color: #333;
# # # #             font-size: 20px;
# # # #         }
        
# # # #         .leaflet-control-zoom-all:hover i {
# # # #             color: #2c3e50;
# # # #         }
# # # #     </style>
# # # # </head>
# # # # <body>
# # # #     <div id="loading">Cargando...</div>
# # # #     <div id="map"></div>
# # # #     <div id="stats-bar"></div>
# # # #     <div id="debug-timestamp">""" + timestamp_debug + """</div>
    
# # # #     <script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"></script>
# # # #     <script>
# # # #         // ========================================
# # # #         // GUARDAR ESTADO ANTES DE RECARGAR
# # # #         // ========================================
# # # #         window.addEventListener('beforeunload', function() {
# # # #             if (window.map) {
# # # #                 try {
# # # #                     const zoom = window.map.getZoom();
# # # #                     const center = window.map.getCenter();
# # # #                     localStorage.setItem('scada_map_zoom', zoom.toString());
# # # #                     localStorage.setItem('scada_map_center', JSON.stringify({lat: center.lat, lng: center.lng}));
# # # #                     localStorage.setItem('scada_map_initialized', 'true');
# # # #                 } catch(e) {}
# # # #             }
# # # #         });
        
# # # #         // ========================================
# # # #         // DATOS INYECTADOS POR PYTHON
# # # #         // ========================================
# # # #         const DATOS_INICIALES = """ + datos_json_safe + """;
# # # #         let map = null;
# # # #         let markers = new Map();
        
# # # #         // ========================================
# # # #         // FUNCIONES AUXILIARES
# # # #         // ========================================
# # # #         function limpiarUrl(url) {
# # # #             if (!url) return null;
# # # #             return url.trim().replace(/\\s+/g, '%20');
# # # #         }
        
# # # #         function esOffline(enLinea) {
# # # #             if (enLinea === undefined || enLinea === null) return false;
# # # #             const valor = String(enLinea).trim().toLowerCase();
# # # #             return valor === '0' || valor === 'false' || valor === 'off' || valor === 'no';
# # # #         }
        
# # # #         function obtenerNivelTanque(estacion) {
# # # #             const campos = ['Porcentaje (%)', 'Porcentaje', 'Nivel (%)', 'nivel_%', 'Nivel', 'nivel'];
# # # #             for (let campo of campos) {
# # # #                 if (estacion[campo] !== undefined) {
# # # #                     let v = parseFloat(estacion[campo]);
# # # #                     return Math.max(0, Math.min(100, isNaN(v) ? 0 : v));
# # # #                 }
# # # #             }
# # # #             return 0;
# # # #         }
        
# # # #         // ========================================
# # # #         // CREAR ÍCONO PARA TANQUE CON BARRA DE LLENADO
# # # #         // ========================================
# # # #         function crearIconoTanque(iconoUrl, nivel, offline = false) {
# # # #             const alturaLlenado = Math.round((nivel / 100) * 28);
# # # #             const bordeStyle = offline ?
# # # #                 'box-shadow: 0 0 0 3px #e74c3c, 0 2px 6px rgba(231, 76, 60, 0.5);' :
# # # #                 '';
            
# # # #             if (iconoUrl) {
# # # #                 return L.divIcon({
# # # #                     html: `<div style="position:relative;width:32px;height:32px;${bordeStyle}">
# # # #                         <div style="position:absolute;bottom:0;left:0;width:32px;height:${alturaLlenado}px;background:rgba(52,152,219,0.85);"></div>
# # # #                         <img src="${iconoUrl}" width="32" height="32" style="position:absolute;top:0;left:0;z-index:1;">
# # # #                         <div style="position:absolute;bottom:4px;width:32px;text-align:center;font-size:11px;color:blue;font-weight:bold;text-shadow:0 1px 2px rgba(0,0,0,0.8)">${Math.round(nivel)}%</div>
# # # #                     </div>`,
# # # #                     iconSize: [32, 32],
# # # #                     iconAnchor: [16, 16],
# # # #                     popupAnchor: [0, -16]
# # # #                 });
# # # #             } else {
# # # #                 const yInicio = 28 - alturaLlenado;
# # # #                 const svg = `<svg xmlns="http://www.w3.org/2000/svg" width="32" height="32" viewBox="0 0 32 32">
# # # #                     <rect x="0" y="${yInicio}" width="32" height="${alturaLlenado}" fill="rgba(52,152,219,0.85)"/>
# # # #                     <rect x="2" y="4" width="28" height="24" fill="#2c3e50"/>
# # # #                     <text x="16" y="20" font-family="Arial" font-size="9" fill="white" text-anchor="middle" font-weight="bold">${Math.round(nivel)}%</text>
# # # #                 </svg>`;
                
# # # #                 return L.divIcon({
# # # #                     html: `<div style="position:relative;width:32px;height:32px;${bordeStyle}">${svg}</div>`,
# # # #                     iconSize: [32, 32],
# # # #                     iconAnchor: [16, 16],
# # # #                     popupAnchor: [0, -16]
# # # #                 });
# # # #             }
# # # #         }
        
# # # #         // ========================================
# # # #         // CREAR ÍCONO PARA SENSOR DE NIVEL DE RÍO CON BARRA DE LLENADO
# # # #         // ========================================
# # # #         function crearIconoRio(iconoUrl, nivel, offline = false) {
# # # #             const alturaLlenado = Math.round((nivel / 100) * 28);
# # # #             const bordeStyle = offline ?
# # # #                 'box-shadow: 0 0 0 3px #e74c3c, 0 2px 6px rgba(231, 76, 60, 0.5);' :
# # # #                 '';
            
# # # #             if (iconoUrl) {
# # # #                 return L.divIcon({
# # # #                     html: `<div style="position:relative;width:32px;height:32px;${bordeStyle}">
# # # #                         <div style="position:absolute;bottom:0;left:0;width:32px;height:${alturaLlenado}px;background:rgba(52,152,219,0.85);"></div>
# # # #                         <img src="${iconoUrl}" width="32" height="32" style="position:absolute;top:0;left:0;z-index:1;">
# # # #                         <div style="position:absolute;bottom:4px;width:32px;text-align:center;font-size:11px;color:blue;font-weight:bold;text-shadow:0 1px 2px rgba(0,0,0,0.8)">${Math.round(nivel)}%</div>
# # # #                     </div>`,
# # # #                     iconSize: [32, 32],
# # # #                     iconAnchor: [16, 16],
# # # #                     popupAnchor: [0, -16]
# # # #                 });
# # # #             } else {
# # # #                 const yInicio = 28 - alturaLlenado;
# # # #                 const svg = `<svg xmlns="http://www.w3.org/2000/svg" width="32" height="32" viewBox="0 0 32 32">
# # # #                     <rect x="0" y="${yInicio}" width="32" height="${alturaLlenado}" fill="rgba(52,152,219,0.85)"/>
# # # #                     <path d="M4 18 Q16 12 28 18 L28 28 Q16 24 4 28 Z" fill="#2c3e50"/>
# # # #                     <text x="16" y="20" font-family="Arial" font-size="9" fill="blue" text-anchor="middle" font-weight="bold">${Math.round(nivel)}%</text>
# # # #                 </svg>`;
                
# # # #                 return L.divIcon({
# # # #                     html: `<div style="position:relative;width:32px;height:32px;${bordeStyle}">${svg}</div>`,
# # # #                     iconSize: [32, 32],
# # # #                     iconAnchor: [16, 16],
# # # #                     popupAnchor: [0, -16]
# # # #                 });
# # # #             }
# # # #         }
        
# # # #         // ========================================
# # # #         // OBTENER ICONO DE TIPO CON SOPORTE PARA ESTADO (POZO, BOMBA, REBOMBO)
# # # #         // ========================================
# # # #         function getIconoTipo(tipo, estado = null) {
# # # #             const tipos = DATOS_INICIALES.tipos || {};
# # # #             const config = tipos[tipo] || tipos['generico'] || {};
            
# # # #             // Tipos que tienen estado ON/OFF: pozo, bomba, rebombeo
# # # #             if (tipo === 'pozo' || tipo === 'bomba' || tipo === 'rebombeo') {
# # # #                 if (estado === 1) {
# # # #                     return {
# # # #                         url: limpiarUrl(config.icono_url_on) || limpiarUrl(config.icono_url) || null,
# # # #                         color: config.color_on || config.color || (tipo === 'pozo' ? '#27ae60' : '#9b59b6')
# # # #                     };
# # # #                 } else {
# # # #                     return {
# # # #                         url: limpiarUrl(config.icono_url_off) || limpiarUrl(config.icono_url) || null,
# # # #                         color: config.color_off || config.color || (tipo === 'pozo' ? '#e74c3c' : '#9b59b6')
# # # #                     };
# # # #                 }
# # # #             }
            
# # # #             // Tanque (manejado por función especial)
# # # #             if (tipo === 'tanque') {
# # # #                 return {
# # # #                     url: limpiarUrl(config.icono_url) || null,
# # # #                     color: config.color || '#3498db'
# # # #                 };
# # # #             }
            
# # # #             // Otros tipos (sensor, etc.)
# # # #             return {
# # # #                 url: limpiarUrl(config.icono_url) || null,
# # # #                 color: config.color || '#7f8c8d'
# # # #             };
# # # #         }
        
# # # #         // ========================================
# # # #         // CREAR ÍCONO PARA MARCADOR (CORREGIDO - SOPORTE COMPLETO DE ESTADO + SENSOR CON BARRA)
# # # #         // ========================================
# # # #         function crearIcono(estacion) {
# # # #             const tipo = estacion.tipo || 'generico';
# # # #             const offline = esOffline(estacion.en_linea);
# # # #             const estado = parseInt(estacion.estado_bomba || estacion.estado || 0);
# # # #             const nivel = obtenerNivelTanque(estacion);
            
# # # #             // ESPECIAL: Tanques siempre usan icono de tanque + barra de llenado
# # # #             if (tipo === 'tanque') {
# # # #                 const configTanque = (DATOS_INICIALES.tipos || {}).tanque || {};
# # # #                 const iconoUrl = limpiarUrl(configTanque.icono_url) || null;
# # # #                 return crearIconoTanque(iconoUrl, nivel, offline);
# # # #             }
            
# # # #             // ESPECIAL: Sensores de nivel de río también usan barra de llenado (color azul oscuro)
# # # #             if (tipo === 'sensor') {
# # # #                 const configSensor = (DATOS_INICIALES.tipos || {}).sensor || {};
# # # #                 const iconoUrl = limpiarUrl(configSensor.icono_url) || null;
# # # #                 return crearIconoRio(iconoUrl, nivel, offline);
# # # #             }
            
# # # #             // Obtener icono según tipo y estado (para pozo, bomba, rebombeo)
# # # #             const iconoInfo = getIconoTipo(tipo, estado);
            
# # # #             // Si está offline, envolver el icono con borde rojo
# # # #             if (offline && iconoInfo.url) {
# # # #                 return L.divIcon({
# # # #                     html: `<div style="
# # # #                         width: 32px;
# # # #                         height: 32px;
# # # #                         border: 3px solid #e74c3c;
# # # #                         border-radius: 4px;
# # # #                         display: flex;
# # # #                         align-items: center;
# # # #                         justify-content: center;
# # # #                         box-sizing: border-box;
# # # #                         box-shadow: 0 2px 6px rgba(231, 76, 60, 0.5);
# # # #                     ">
# # # #                         <img src="${iconoInfo.url}" width="26" height="26" style="display:block;">
# # # #                     </div>`,
# # # #                     iconSize: [32, 32],
# # # #                     iconAnchor: [16, 16],
# # # #                     popupAnchor: [0, -16]
# # # #                 });
# # # #             }
            
# # # #             // Si tiene URL de icono, usarla directamente
# # # #             if (iconoInfo.url) {
# # # #                 return L.icon({
# # # #                     iconUrl: iconoInfo.url,
# # # #                     iconSize: [32, 32],
# # # #                     iconAnchor: [16, 16],
# # # #                     popupAnchor: [0, -16]
# # # #                 });
# # # #             }
            
# # # #             // Fallback: icono genérico con color + borde rojo si offline
# # # #             const borderColor = offline ? '#e74c3c' : iconoInfo.color;
# # # #             const bgColor = offline ? 'rgba(231, 76, 60, 0.1)' : iconoInfo.color;
# # # #             return L.divIcon({
# # # #                 html: `<div style="
# # # #                     width: 32px;
# # # #                     height: 32px;
# # # #                     border: 2px solid ${borderColor};
# # # #                     border-radius: 50%;
# # # #                     display: flex;
# # # #                     align-items: center;
# # # #                     justify-content: center;
# # # #                     box-sizing: border-box;
# # # #                     background: ${bgColor};
# # # #                 ">
# # # #                     <div style="
# # # #                         width: 20px;
# # # #                         height: 20px;
# # # #                         border-radius: 50%;
# # # #                         background: white;
# # # #                     "></div>
# # # #                 </div>`,
# # # #                 iconSize: [32, 32],
# # # #                 iconAnchor: [16, 16],
# # # #                 popupAnchor: [0, -16]
# # # #             });
# # # #         }
        
# # # #         // ========================================
# # # #         // CREAR POPUP
# # # #         // ========================================
# # # #         function crearPopupContent(estacion) {
# # # #             let html = `<div class="custom-popup"><h4>${estacion.nombre || 'Estación'}</h4><hr>`;
            
# # # #             const offline = esOffline(estacion.en_linea);
# # # #             const estadoLinea = offline ? '<span class="status-offline">Fuera de línea</span>' : '<span class="status-online">En línea</span>';
# # # #             html += `<div class="var-row"><span class="var-label">Estado:</span><span class="var-value">${estadoLinea}</span></div>`;
            
# # # #             if (estacion.tipo === 'tanque' || estacion.tipo === 'sensor') {
# # # #                 html += `<div class="var-row"><span class="var-label">Nivel:</span><span class="var-value">${obtenerNivelTanque(estacion)}%</span></div>`;
# # # #             } else if (estacion.tipo === 'pozo' || estacion.tipo === 'bomba' || estacion.tipo === 'rebombeo') {
# # # #                 const estadoBomba = parseInt(estacion.estado_bomba || estacion.estado || 0);
# # # #                 const estadoTexto = estadoBomba === 1 ? '<span style="color:#27ae60;font-weight:bold;">Encendido</span>' : '<span style="color:#e74c3c;font-weight:bold;">Apagado</span>';
# # # #                 html += `<div class="var-row"><span class="var-label">Estado Bomba:</span><span class="var-value">${estadoTexto}</span></div>`;
# # # #             }
            
# # # #             for (const key in estacion) {
# # # #                 if (!['nombre', 'latitud', 'longitud', 'tipo', 'estado_bomba', 'en_linea', 'icono', 'icono_url', 'icono_url_on', 'icono_url_off', 'Nivel', 'nivel', 'Porcentaje (%)', 'Porcentaje', '_timestamp_actualizacion'].includes(key)) {
# # # #                     const value = typeof estacion[key] === 'number'
# # # #                         ? estacion[key].toLocaleString('es-ES', { minimumFractionDigits: 2, maximumFractionDigits: 2 })
# # # #                         : estacion[key];
# # # #                     html += `<div class="var-row"><span class="var-label">${key}:</span><span class="var-value">${value}</span></div>`;
# # # #                 }
# # # #             }
            
# # # #             html += `<hr><div class="timestamp">📅 ${new Date().toLocaleString('es-ES')}</div></div>`;
# # # #             return html;
# # # #         }
        
# # # #         // ========================================
# # # #         // ACTUALIZAR ESTADÍSTICAS CON ICONOS DE TIPOS
# # # #         // ========================================
# # # #         function actualizarEstadisticas(datos) {
# # # #             if (!datos || !datos.estaciones) return;
            
# # # #             // Contadores
# # # #             let total = 0;
# # # #             let pozos_encendidos = 0;
# # # #             let pozos_apagados = 0;
# # # #             let tanques = 0;
# # # #             let bombas_encendidas = 0;
# # # #             let bombas_apagadas = 0;
# # # #             let rebombeos_encendidos = 0;
# # # #             let rebombeos_apagados = 0;
# # # #             let sensores = 0;
# # # #             let offline_count = 0;
# # # #             let online = 0;
            
# # # #             datos.estaciones.forEach(estacion => {
# # # #                 total++;
# # # #                 const offline = esOffline(estacion.en_linea);
# # # #                 const tipo = estacion.tipo || 'generico';
# # # #                 const estado = parseInt(estacion.estado_bomba || estacion.estado || 0);
                
# # # #                 if (offline) {
# # # #                     offline_count++;
# # # #                 } else {
# # # #                     online++;
# # # #                     if (tipo === 'pozo') {
# # # #                         if (estado === 1) pozos_encendidos++;
# # # #                         else pozos_apagados++;
# # # #                     } else if (tipo === 'tanque') {
# # # #                         tanques++;
# # # #                     } else if (tipo === 'bomba') {
# # # #                         if (estado === 1) bombas_encendidas++;
# # # #                         else bombas_apagadas++;
# # # #                     } else if (tipo === 'rebombeo') {
# # # #                         if (estado === 1) rebombeos_encendidos++;
# # # #                         else rebombeos_apagados++;
# # # #                     } else if (tipo === 'sensor') {
# # # #                         sensores++;
# # # #                     }
# # # #                 }
# # # #             });
            
# # # #             // Obtener configuración de tipos
# # # #             const tipos = datos.tipos || {};
            
# # # #             // Definir las estadísticas a mostrar
# # # #             const stats = [
# # # #                 { tipo: 'total', value: total, label: 'Total' },
# # # #                 { tipo: 'pozo', estado: 1, value: pozos_encendidos, label: 'Pozos Enc.' },
# # # #                 { tipo: 'pozo', estado: 0, value: pozos_apagados, label: 'Pozos Apag.' },
# # # #                 { tipo: 'tanque', value: tanques, label: 'Tanques' },
# # # #                 { tipo: 'bomba', estado: 1, value: bombas_encendidas, label: 'Bombas Enc.' },
# # # #                 { tipo: 'bomba', estado: 0, value: bombas_apagadas, label: 'Bombas Apag.' },
# # # #                 { tipo: 'rebombeo', estado: 1, value: rebombeos_encendidos, label: 'Rebom. Enc.' },
# # # #                 { tipo: 'rebombeo', estado: 0, value: rebombeos_apagados, label: 'Rebom. Apag.' },
# # # #                 { tipo: 'sensor', value: sensores, label: 'Sensores Río' },
# # # #                 { tipo: 'offline', value: offline_count, label: 'Offline' },
# # # #                 { tipo: 'online', value: online, label: 'Online' },
# # # #                 { tipo: 'reloj', value: '""" + tiempo_str + """', label: 'Actualizado' }
# # # #             ];
            
# # # #             // Crear barra de estadísticas
# # # #             const statsBar = document.getElementById('stats-bar');
# # # #             if (!statsBar) return;
# # # #             statsBar.innerHTML = '';
            
# # # #             // Crear cada item
# # # #             stats.forEach(stat => {
# # # #                 const config = tipos[stat.tipo] || tipos['generico'] || {};
# # # #                 let iconoUrl = null;
                
# # # #                 // Manejar tipos con estado
# # # #                 if (stat.tipo === 'pozo' || stat.tipo === 'bomba' || stat.tipo === 'rebombeo') {
# # # #                     iconoUrl = stat.estado === 1 ?
# # # #                         (limpiarUrl(config.icono_url_on) || limpiarUrl(config.icono_url) || null) :
# # # #                         (limpiarUrl(config.icono_url_off) || limpiarUrl(config.icono_url) || null);
# # # #                 }
                
# # # #                 // Tipos especiales con iconos base64
# # # #                 else if (stat.tipo === 'offline') {
# # # #                     iconoUrl = 'https://raw.githubusercontent.com/AlarmasCiateq/SCADA_T/main/iconos/Offline.svg';
# # # #                 } else if (stat.tipo === 'online') {
# # # #                     iconoUrl = 'https://raw.githubusercontent.com/AlarmasCiateq/SCADA_T/main/iconos/Online_Alarma.svg';
# # # #                 } else if (stat.tipo === 'total') {
# # # #                     iconoUrl = 'https://raw.githubusercontent.com/AlarmasCiateq/SCADA_T/main/iconos/transmite.svg';
# # # #                 } else if (stat.tipo === 'reloj') {
# # # #                     iconoUrl = 'https://raw.githubusercontent.com/AlarmasCiateq/SCADA_T/main/iconos/update.svg';
# # # #                 }
                
# # # #                 // Otros tipos
# # # #                 else {
# # # #                     iconoUrl = limpiarUrl(config.icono_url) || null;
# # # #                 }
                
# # # #                 const item = document.createElement('div');
# # # #                 item.className = 'stat-item';
                
# # # #                 let iconHtml = '';
# # # #                 if (iconoUrl) {
# # # #                     iconHtml = `<div class="stat-icon"><img src="${iconoUrl}" alt="${stat.tipo}"></div>`;
# # # #                 } else {
# # # #                     const color = config.color || '#7f8c8d';
# # # #                     iconHtml = `<div class="stat-icon" style="color:${color};font-size:20px;">●</div>`;
# # # #                 }
                
# # # #                 item.innerHTML =
# # # #                     iconHtml +
# # # #                     '<div class="stat-value">' + stat.value + '</div>' +
# # # #                     '<div class="stat-label">' + stat.label + '</div>';
                
# # # #                 statsBar.appendChild(item);
# # # #             });
# # # #         }
        
# # # #         // ========================================
# # # #         // FUNCIÓN PARA ZOOM A TODOS LOS ICONOS
# # # #         // ========================================
# # # #         function zoomATodosLosIconos() {
# # # #             if (!map || markers.size === 0) return;
# # # #             const todasCoords = Array.from(markers.values()).map(m => m.getLatLng());
# # # #             map.fitBounds(todasCoords, { padding: [40, 40] });
# # # #             try {
# # # #                 localStorage.setItem('scada_map_zoom', map.getZoom().toString());
# # # #                 localStorage.setItem('scada_map_center', JSON.stringify({lat: map.getCenter().lat, lng: map.getCenter().lng}));
# # # #             } catch(e) {}
# # # #         }
        
# # # #         // ========================================
# # # #         // CONTROL PERSONALIZADO DE LEAFLET
# # # #         // ========================================
# # # #         L.Control.ZoomAll = L.Control.extend({
# # # #             options: { position: 'topleft' },
# # # #             onAdd: function(map) {
# # # #                 const container = L.DomUtil.create('div', 'leaflet-bar leaflet-control leaflet-control-zoom-all');
# # # #                 const button = L.DomUtil.create('a', 'leaflet-control-zoom-all', container);
# # # #                 button.href = '#';
# # # #                 button.title = 'Ver todas las estaciones';
# # # #                 button.innerHTML = '<i>⌂</i>';
# # # #                 L.DomEvent.disableClickPropagation(button);
# # # #                 L.DomEvent.on(button, 'click', function(e) {
# # # #                     L.DomEvent.stopPropagation(e);
# # # #                     L.DomEvent.preventDefault(e);
# # # #                     zoomATodosLosIconos();
# # # #                 });
# # # #                 return container;
# # # #             }
# # # #         });
        
# # # #         L.control.zoomAll = function(opts) { return new L.Control.ZoomAll(opts); };
        
# # # #         // ========================================
# # # #         // INICIALIZAR MAPA
# # # #         // ========================================
# # # #         function initMap() {
# # # #             try {
# # # #                 map = L.map('map', {
# # # #                     zoomControl: true,
# # # #                     scrollWheelZoom: true,
# # # #                     dragging: true
# # # #                 });
                
# # # #                 L.tileLayer('https://{s}.basemaps.cartocdn.com/light_all/{z}/{x}/{y}{r}.png', {
# # # #                     attribution: '',
# # # #                     subdomains: 'abcd',
# # # #                     maxZoom: 19
# # # #                 }).addTo(map);
                
# # # #                 L.control.zoomAll().addTo(map);
                
# # # #                 // Restaurar zoom/centro
# # # #                 const savedZoom = localStorage.getItem('scada_map_zoom');
# # # #                 const savedCenter = localStorage.getItem('scada_map_center');
# # # #                 const wasInitialized = localStorage.getItem('scada_map_initialized') === 'true';
# # # #                 let hizoFitBounds = false;
                
# # # #                 if (wasInitialized && savedZoom && savedCenter) {
# # # #                     try {
# # # #                         const center = JSON.parse(savedCenter);
# # # #                         map.setView([center.lat, center.lng], parseInt(savedZoom));
# # # #                         console.log('✓ Zoom restaurado:', savedZoom);
# # # #                     } catch(e) {
# # # #                         console.log('Error restaurando zoom:', e);
# # # #                     }
# # # #                 } else {
# # # #                     const todasCoords = [];
# # # #                     DATOS_INICIALES.estaciones.forEach(est => {
# # # #                         if (est.latitud && est.longitud) {
# # # #                             todasCoords.push([parseFloat(est.latitud), parseFloat(est.longitud)]);
# # # #                         }
# # # #                     });
# # # #                     if (todasCoords.length > 0) {
# # # #                         map.fitBounds(todasCoords, { padding: [40, 40] });
# # # #                         console.log('✓ Zoom inicial ajustado');
# # # #                         hizoFitBounds = true;
# # # #                     }
# # # #                 }
                
# # # #                 // Agregar marcadores
# # # #                 DATOS_INICIALES.estaciones.forEach(estacion => {
# # # #                     if (!estacion.latitud || !estacion.longitud) return;
# # # #                     const id = estacion.nombre || `${estacion.latitud},${estacion.longitud}`;
# # # #                     const lat = parseFloat(estacion.latitud);
# # # #                     const lng = parseFloat(estacion.longitud);
# # # #                     const marker = L.marker([lat, lng], { icon: crearIcono(estacion) })
# # # #                         .bindPopup(crearPopupContent(estacion), { maxWidth: 320 })
# # # #                         .bindTooltip(estacion.nombre || 'Estación', { permanent: false, direction: 'top', opacity: 0.9 })
# # # #                         .addTo(map);
# # # #                     markers.set(id, marker);
# # # #                 });
                
# # # #                 if (!hizoFitBounds && markers.size > 0 && !wasInitialized) {
# # # #                     const todasCoords = Array.from(markers.values()).map(m => m.getLatLng());
# # # #                     map.fitBounds(todasCoords, { padding: [40, 40] });
# # # #                     localStorage.setItem('scada_map_initialized', 'true');
# # # #                 }
                
# # # #                 // Actualizar estadísticas
# # # #                 actualizarEstadisticas(DATOS_INICIALES);
                
# # # #                 // Ocultar loading
# # # #                 document.getElementById('loading').classList.add('hidden');
# # # #                 window.map = map;
                
# # # #             } catch(e) {
# # # #                 document.getElementById('loading').innerHTML = `<div style="color:#e74c3c;text-align:center;padding:20px;">❌ Error: ${e.message}</div>`;
# # # #                 console.error('Error:', e);
# # # #             }
# # # #         }
        
# # # #         if (document.readyState === 'loading') {
# # # #             document.addEventListener('DOMContentLoaded', initMap);
# # # #         } else {
# # # #             initMap();
# # # #         }
# # # #     </script>
# # # # </body>
# # # # </html>
# # # # """

# # # # # Renderizar el mapa
# # # # st.components.v1.html(
# # # #     html_completo,
# # # #     width=1920,
# # # #     height=1080,
# # # #     scrolling=False
# # # # )

# # # # # ========================================
# # # # # FORZAR RECARGA COMPLETA CADA 60 SEGUNDOS (1 MINUTO)
# # # # # ========================================
# # # # time.sleep(60)
# # # # st.rerun()



# # # import streamlit as st
# # # import requests
# # # import json
# # # import base64
# # # from datetime import datetime
# # # import os
# # # import time

# # # # ========================================
# # # # FUNCIÓN PARA OBTENER EL FAVICON DESDE GITHUB
# # # # ========================================
# # # def obtener_favicon_github():
# # #     """Descarga el icono de GitHub y lo convierte a base64"""
# # #     try:
# # #         GITHUB_USER = "AlarmasCiateq"
# # #         REPO_NAME = "SCADA_T"
# # #         BRANCH = "main"
# # #         ICON_PATH = "iconos/ICONO CIATEQ 256.ico"  # Ajusta la ruta si es necesario
        
# # #         # URL para descargar el archivo RAW (no la API)
# # #         raw_url = f"https://raw.githubusercontent.com/{GITHUB_USER}/{REPO_NAME}/{BRANCH}/{ICON_PATH}"
# # #         print(raw_url)
# # #         headers = {'User-Agent': 'SCADA-Monitor'}
# # #         response = requests.get(raw_url, headers=headers, timeout=10)
# # #         response.raise_for_status()
        
# # #         # Convertir a base64
# # #         icon_base64 = base64.b64encode(response.content).decode('utf-8')
# # #         return f"data:image/x-icon;base64,{icon_base64}"
# # #     except Exception as e:
# # #         print(f"Error cargando favicon: {e}")
# # #         return None

# # # # ========================================
# # # # CONFIGURACIÓN DE PÁGINA
# # # # ========================================
# # # # Intentar obtener el favicon de GitHub
# # # favicon_data = obtener_favicon_github()

# # # if favicon_data:
# # #     # Streamlit no soporta directamente data URLs en page_icon,
# # #     # pero podemos inyectarlo con HTML después
# # #     st.set_page_config(
# # #         page_title="SCADA CIATEQ",
# # #         page_icon="🌎",  # Usamos un emoji temporal
# # #         layout="wide",
# # #         initial_sidebar_state="collapsed"
# # #     )
    
# # #     # Inyectar el favicon personalizado vía HTML
# # #     st.markdown(f"""
# # #     <link rel="icon" href="{favicon_data}" type="image/x-icon">
# # #     <link rel="shortcut icon" href="{favicon_data}" type="image/x-icon">
# # #     """, unsafe_allow_html=True)
# # # else:
# # #     # Fallback al emoji si no se pudo cargar el icono
# # #     st.set_page_config(
# # #         page_title="SCADA CIATEQ",
# # #         page_icon="🏭",
# # #         layout="wide",
# # #         initial_sidebar_state="collapsed"
# # #     )
# # # # CSS AGRESIVO
# # # st.markdown("""
# # # <style>
# # # [data-testid="stSidebar"] { display: none !important; }
# # # [data-testid="stHeader"] { display: none !important; }
# # # [data-testid="stDecoration"] { display: none !important; }
# # # header { display: none !important; }
# # # #MainMenu { display: none !important; }
# # # footer { display: none !important; }
# # # .stApp { background-color: #0e1117; padding: 0 !important; margin: 0 !important; overflow: hidden !important; }
# # # .block-container { padding: 0 !important; max-width: 100% !important; margin: 0 !important; overflow: hidden !important; }
# # # .main { padding: 0 !important; margin: 0 !important; overflow: hidden !important; }
# # # .block-container > div { padding: 0 !important; margin: 0 !important; }
# # # ::-webkit-scrollbar { display: none !important; }
# # # body { overflow: hidden !important; }
# # # #loading {
# # #     position: fixed;
# # #     top: 0;
# # #     left: 0;
# # #     width: 100%;
# # #     height: 100%;
# # #     background: #0e1117;
# # #     display: flex;
# # #     justify-content: center;
# # #     align-items: center;
# # #     color: #3498db;
# # #     font-family: Arial;
# # #     font-size: 18px;
# # #     z-index: 9999;
# # #     transition: opacity 0.1s;
# # # }
# # # #loading.hidden {
# # #     opacity: 0;
# # #     pointer-events: none;
# # # }
# # # #debug-timestamp {
# # #     position: fixed;
# # #     bottom: 5px;
# # #     right: 10px;
# # #     background: rgba(0,0,0,0.7);
# # #     color: #27ae60;
# # #     padding: 3px 8px;
# # #     font-family: monospace;
# # #     font-size: 11px;
# # #     border-radius: 3px;
# # #     z-index: 1000;
# # # }
# # # </style>
# # # """, unsafe_allow_html=True)

# # # # ========================================
# # # # OBTENER TOKEN DE GITHUB
# # # # ========================================
# # # def obtener_token_github():
# # #     try:
# # #         if hasattr(st, 'secrets') and "GITHUB_TOKEN" in st.secrets:
# # #             return st.secrets["GITHUB_TOKEN"]
# # #     except:
# # #         pass
# # #     return os.getenv("GITHUB_TOKEN", None)

# # # # ========================================
# # # # CARGAR DATOS FRESH DE GITHUB (CADA EJECUCIÓN)
# # # # ========================================
# # # def cargar_datos_github(max_intentos=3):
# # #     token = obtener_token_github()
# # #     for intento in range(max_intentos):
# # #         try:
# # #             GITHUB_USER = "AlarmasCiateq"
# # #             REPO_NAME = "SCADA_T"
# # #             BRANCH = "main"
# # #             FILE_PATH = "datos_estaciones.json"
            
# # #             # URL CORREGIDA: SIN ESPACIOS
# # #             api_url = f"https://api.github.com/repos/{GITHUB_USER}/{REPO_NAME}/contents/{FILE_PATH}?ref={BRANCH}"
            
# # #             headers = {
# # #                 'User-Agent': f'SCADA-Monitor-{datetime.now().timestamp()}',
# # #                 'Accept': 'application/vnd.github.v3+json'
# # #             }
            
# # #             if token:
# # #                 headers['Authorization'] = f'token {token}'
            
# # #             response = requests.get(api_url, headers=headers, timeout=10)
# # #             response.raise_for_status()
            
# # #             data = response.json()
# # #             content_bytes = base64.b64decode(data['content'])
# # #             content_str = content_bytes.decode('utf-8')
# # #             datos = json.loads(content_str)
            
# # #             datos['_timestamp_actualizacion'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
# # #             return datos, True
            
# # #         except Exception as e:
# # #             print(f"Error cargando datos (intento {intento + 1}): {e}")
# # #             if intento < max_intentos - 1:
# # #                 time.sleep(1)
# # #                 continue
# # #             return None, False
# # #     return None, False

# # # # ========================================
# # # # CARGAR DATOS FRESH EN CADA EJECUCIÓN
# # # # ========================================
# # # datos, exito = cargar_datos_github()

# # # if not datos or not exito:
# # #     st.markdown("""
# # #     <div style="position:fixed;top:0;left:0;width:100%;height:100%;background:#0e1117;color:white;
# # #     display:flex;justify-content:center;align-items:center;font-family:Arial;">
# # #         <div style="text-align:center;padding:20px;">
# # #             <h2>🛢️ SCADA Monitor</h2>
# # #             <p style="color:#e74c3c; margin-top:15px;">Error: No se pudieron cargar los datos de GitHub</p>
# # #             <p style="font-size:14px; margin-top:10px; color:#95a5a6;">Verifique conexión a internet</p>
# # #         </div>
# # #     </div>
# # #     """, unsafe_allow_html=True)
# # #     time.sleep(60)
# # #     st.rerun()

# # # # ========================================
# # # # PREPARAR DATOS PARA HTML
# # # # ========================================
# # # tiempo_str = datetime.now().strftime('%H:%M:%S')
# # # timestamp_debug = datos.get('_timestamp_actualizacion', tiempo_str)

# # # # Escapar JSON correctamente para JavaScript
# # # datos_json_safe = json.dumps(datos, ensure_ascii=False)
# # # datos_json_safe = (datos_json_safe.replace('\\', '\\\\')
# # #     .replace("'", "\\'")
# # #     .replace('</', '<\\/')
# # #     .replace('\n', '\\n')
# # #     .replace('\r', '\\r')
# # #     .replace('\t', '\\t'))

# # # # ========================================
# # # # HTML + JAVASCRIPT (CORREGIDO - SENSOR CON BARRA DE NIVEL)
# # # # ========================================
# # # html_completo = """
# # # <!DOCTYPE html>
# # # <html lang="es">
# # # <head>
# # #     <meta charset="UTF-8">
# # #     <meta name="viewport" content="width=device-width, initial-scale=1.0">
# # #     <title>SCADA Monitor</title>
# # #     <link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css" />
# # #     <style>
# # #         * { margin: 0; padding: 0; box-sizing: border-box; }
# # #         body { font-family: Arial, sans-serif; background: #0e1117; overflow: hidden; height: 100vh; width: 100vw; }
# # #         #map { position: absolute; top: 0; left: 0; width: 100%; height: 100%; z-index: 1; }
        
# # #         #stats-bar {
# # #             position: fixed;
# # #             top: 10px;
# # #             right: 15px;
# # #             background: rgba(255, 255, 255, 0.95);
# # #             padding: 8px;
# # #             border-radius: 6px;
# # #             box-shadow: 0 2px 8px rgba(0,0,0,0.15);
# # #             z-index: 1000;
# # #             display: flex;
# # #             gap: 12px;
# # #             align-items: center;
# # #             font-family: Arial, sans-serif;
# # #             flex-wrap: nowrap;
# # #             overflow-x: auto;
# # #             max-width: 90%;
# # #         }
        
# # #         .stat-item {
# # #             display: flex;
# # #             flex-direction: column;
# # #             align-items: center;
# # #             min-width: 65px;
# # #         }
        
# # #         .stat-icon {
# # #             width: 24px;
# # #             height: 24px;
# # #             margin-bottom: 2px;
# # #             display: flex;
# # #             align-items: center;
# # #             justify-content: center;
# # #         }
        
# # #         .stat-icon img {
# # #             width: 100%;
# # #             height: 100%;
# # #             object-fit: contain;
# # #         }
        
# # #         .stat-value {
# # #             font-weight: bold;
# # #             color: #2c3e50;
# # #             font-size: 14px;
# # #             text-align: center;
# # #         }
        
# # #         .stat-label {
# # #             font-size: 8px;
# # #             color: #7f8c8d;
# # #             text-align: center;
# # #             white-space: nowrap;
# # #             text-transform: uppercase;
# # #             letter-spacing: 0.5px;
# # #         }
        
# # #         .custom-popup {
# # #             font-family: Arial;
# # #             padding: 12px;
# # #             min-width: 280px;
# # #             background: white;
# # #             border-radius: 6px;
# # #         }
        
# # #         .custom-popup h4 {
# # #             margin: 0 0 10px 0;
# # #             color: #2c3e50;
# # #             font-size: 16px;
# # #             font-weight: bold;
# # #         }
        
# # #         .custom-popup hr {
# # #             margin: 8px 0;
# # #             border-color: #ecf0f1;
# # #         }
        
# # #         .custom-popup .var-row {
# # #             margin: 6px 0;
# # #             padding: 4px 0;
# # #             display: flex;
# # #             justify-content: space-between;
# # #         }
        
# # #         .custom-popup .var-label {
# # #             color: #2c3e50;
# # #             font-weight: 600;
# # #             font-size: 13px;
# # #             min-width: 120px;
# # #         }
        
# # #         .custom-popup .var-value {
# # #             color: #2c3e50;
# # #             font-weight: bold;
# # #             font-size: 14px;
# # #             text-align: right;
# # #             min-width: 80px;
# # #         }
        
# # #         .custom-popup .timestamp {
# # #             font-size: 11px;
# # #             color: #95a5a6;
# # #             text-align: center;
# # #             margin-top: 8px;
# # #         }
        
# # #         .status-online { color: #27ae60; font-weight: bold; }
# # #         .status-offline { color: #e74c3c; font-weight: bold; }
        
# # #         #loading {
# # #             position: fixed;
# # #             top: 0;
# # #             left: 0;
# # #             width: 100%;
# # #             height: 100%;
# # #             background: #0e1117;
# # #             display: flex;
# # #             justify-content: center;
# # #             align-items: center;
# # #             color: #3498db;
# # #             font-family: Arial;
# # #             font-size: 18px;
# # #             z-index: 9999;
# # #             transition: opacity 0.1s;
# # #         }
        
# # #         #loading.hidden {
# # #             opacity: 0;
# # #             pointer-events: none;
# # #         }
        
# # #         #debug-timestamp {
# # #             position: fixed;
# # #             bottom: 5px;
# # #             right: 10px;
# # #             background: rgba(0,0,0,0.7);
# # #             color: #27ae60;
# # #             padding: 3px 8px;
# # #             font-family: monospace;
# # #             font-size: 11px;
# # #             border-radius: 3px;
# # #             z-index: 1000;
# # #         }
        
# # #         /* Botón de Vista General */
# # #         .leaflet-control-zoom-all {
# # #             background: #fff;
# # #             border: 2px solid rgba(0,0,0,0.2);
# # #             border-radius: 4px;
# # #             box-shadow: 0 1px 5px rgba(0,0,0,0.4);
# # #             cursor: pointer;
# # #             margin-top: 5px;
# # #             transition: all 0.2s;
# # #         }
        
# # #         .leaflet-control-zoom-all:hover {
# # #             background: #f4f4f4;
# # #             box-shadow: 0 1px 7px rgba(0,0,0,0.45);
# # #         }
        
# # #         .leaflet-control-zoom-all:active {
# # #             background: #e8e8e8;
# # #         }
        
# # #         .leaflet-control-zoom-all i {
# # #             display: block;
# # #             width: 30px;
# # #             height: 30px;
# # #             line-height: 30px;
# # #             text-align: center;
# # #             font-weight: bold;
# # #             color: #333;
# # #             font-size: 20px;
# # #         }
        
# # #         .leaflet-control-zoom-all:hover i {
# # #             color: #2c3e50;
# # #         }
# # #     </style>
# # # </head>
# # # <body>
# # #     <div id="loading">Cargando...</div>
# # #     <div id="map"></div>
# # #     <div id="stats-bar"></div>
# # #     <div id="debug-timestamp">""" + timestamp_debug + """</div>
    
# # #     <script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"></script>
# # #     <script>
# # #         // ========================================
# # #         // GUARDAR ESTADO ANTES DE RECARGAR
# # #         // ========================================
# # #         window.addEventListener('beforeunload', function() {
# # #             if (window.map) {
# # #                 try {
# # #                     const zoom = window.map.getZoom();
# # #                     const center = window.map.getCenter();
# # #                     localStorage.setItem('scada_map_zoom', zoom.toString());
# # #                     localStorage.setItem('scada_map_center', JSON.stringify({lat: center.lat, lng: center.lng}));
# # #                     localStorage.setItem('scada_map_initialized', 'true');
# # #                 } catch(e) {}
# # #             }
# # #         });
        
# # #         // ========================================
# # #         // DATOS INYECTADOS POR PYTHON
# # #         // ========================================
# # #         const DATOS_INICIALES = """ + datos_json_safe + """;
# # #         let map = null;
# # #         let markers = new Map();
        
# # #         // ========================================
# # #         // FUNCIONES AUXILIARES
# # #         // ========================================
# # #         function limpiarUrl(url) {
# # #             if (!url) return null;
# # #             return url.trim().replace(/\\s+/g, '%20');
# # #         }
        
# # #         function esOffline(enLinea) {
# # #             if (enLinea === undefined || enLinea === null) return false;
# # #             const valor = String(enLinea).trim().toLowerCase();
# # #             return valor === '0' || valor === 'false' || valor === 'off' || valor === 'no';
# # #         }
        
# # #         function obtenerNivelTanque(estacion) {
# # #             const campos = ['Porcentaje (%)', 'Porcentaje', 'Nivel (%)', 'nivel_%', 'Nivel', 'nivel'];
# # #             for (let campo of campos) {
# # #                 if (estacion[campo] !== undefined) {
# # #                     let v = parseFloat(estacion[campo]);
# # #                     return Math.max(0, Math.min(100, isNaN(v) ? 0 : v));
# # #                 }
# # #             }
# # #             return 0;
# # #         }
        
# # #         // ========================================
# # #         // CREAR ÍCONO PARA TANQUE CON BARRA DE LLENADO
# # #         // ========================================
# # #         function crearIconoTanque(iconoUrl, nivel, offline = false) {
# # #             const alturaLlenado = Math.round((nivel / 100) * 28);
# # #             const bordeStyle = offline ?
# # #                 'box-shadow: 0 0 0 3px #e74c3c, 0 2px 6px rgba(231, 76, 60, 0.5);' :
# # #                 '';
            
# # #             if (iconoUrl) {
# # #                 return L.divIcon({
# # #                     html: `<div style="position:relative;width:32px;height:32px;${bordeStyle}">
# # #                         <div style="position:absolute;bottom:0;left:0;width:32px;height:${alturaLlenado}px;background:rgba(52,152,219,0.85);"></div>
# # #                         <img src="${iconoUrl}" width="32" height="32" style="position:absolute;top:0;left:0;z-index:1;">
# # #                         <div style="position:absolute;bottom:4px;width:32px;text-align:center;font-size:11px;color:blue;font-weight:bold;text-shadow:0 1px 2px rgba(0,0,0,0.8)">${Math.round(nivel)}%</div>
# # #                     </div>`,
# # #                     iconSize: [32, 32],
# # #                     iconAnchor: [16, 16],
# # #                     popupAnchor: [0, -16]
# # #                 });
# # #             } else {
# # #                 const yInicio = 28 - alturaLlenado;
# # #                 const svg = `<svg xmlns="http://www.w3.org/2000/svg" width="32" height="32" viewBox="0 0 32 32">
# # #                     <rect x="0" y="${yInicio}" width="32" height="${alturaLlenado}" fill="rgba(52,152,219,0.85)"/>
# # #                     <rect x="2" y="4" width="28" height="24" fill="#2c3e50"/>
# # #                     <text x="16" y="20" font-family="Arial" font-size="9" fill="white" text-anchor="middle" font-weight="bold">${Math.round(nivel)}%</text>
# # #                 </svg>`;
                
# # #                 return L.divIcon({
# # #                     html: `<div style="position:relative;width:32px;height:32px;${bordeStyle}">${svg}</div>`,
# # #                     iconSize: [32, 32],
# # #                     iconAnchor: [16, 16],
# # #                     popupAnchor: [0, -16]
# # #                 });
# # #             }
# # #         }
        
# # #         // ========================================
# # #         // CREAR ÍCONO PARA SENSOR DE NIVEL DE RÍO CON BARRA DE LLENADO
# # #         // ========================================
# # #         function crearIconoRio(iconoUrl, nivel, offline = false) {
# # #             const alturaLlenado = Math.round((nivel / 100) * 28);
# # #             const bordeStyle = offline ?
# # #                 'box-shadow: 0 0 0 3px #e74c3c, 0 2px 6px rgba(231, 76, 60, 0.5);' :
# # #                 '';
            
# # #             if (iconoUrl) {
# # #                 return L.divIcon({
# # #                     html: `<div style="position:relative;width:32px;height:32px;${bordeStyle}">
# # #                         <div style="position:absolute;bottom:0;left:0;width:32px;height:${alturaLlenado}px;background:rgba(52,152,219,0.85);"></div>
# # #                         <img src="${iconoUrl}" width="32" height="32" style="position:absolute;top:0;left:0;z-index:1;">
# # #                         <div style="position:absolute;bottom:4px;width:32px;text-align:center;font-size:11px;color:blue;font-weight:bold;text-shadow:0 1px 2px rgba(0,0,0,0.8)">${Math.round(nivel)}%</div>
# # #                     </div>`,
# # #                     iconSize: [32, 32],
# # #                     iconAnchor: [16, 16],
# # #                     popupAnchor: [0, -16]
# # #                 });
# # #             } else {
# # #                 const yInicio = 28 - alturaLlenado;
# # #                 const svg = `<svg xmlns="http://www.w3.org/2000/svg" width="32" height="32" viewBox="0 0 32 32">
# # #                     <rect x="0" y="${yInicio}" width="32" height="${alturaLlenado}" fill="rgba(52,152,219,0.85)"/>
# # #                     <path d="M4 18 Q16 12 28 18 L28 28 Q16 24 4 28 Z" fill="#2c3e50"/>
# # #                     <text x="16" y="20" font-family="Arial" font-size="9" fill="blue" text-anchor="middle" font-weight="bold">${Math.round(nivel)}%</text>
# # #                 </svg>`;
                
# # #                 return L.divIcon({
# # #                     html: `<div style="position:relative;width:32px;height:32px;${bordeStyle}">${svg}</div>`,
# # #                     iconSize: [32, 32],
# # #                     iconAnchor: [16, 16],
# # #                     popupAnchor: [0, -16]
# # #                 });
# # #             }
# # #         }
        
# # #         // ========================================
# # #         // OBTENER ICONO DE TIPO CON SOPORTE PARA ESTADO (POZO, BOMBA, REBOMBO)
# # #         // ========================================
# # #         function getIconoTipo(tipo, estado = null) {
# # #             const tipos = DATOS_INICIALES.tipos || {};
# # #             const config = tipos[tipo] || tipos['generico'] || {};
            
# # #             // Tipos que tienen estado ON/OFF: pozo, bomba, rebombeo
# # #             if (tipo === 'pozo' || tipo === 'bomba' || tipo === 'rebombeo') {
# # #                 if (estado === 1) {
# # #                     return {
# # #                         url: limpiarUrl(config.icono_url_on) || limpiarUrl(config.icono_url) || null,
# # #                         color: config.color_on || config.color || (tipo === 'pozo' ? '#27ae60' : '#9b59b6')
# # #                     };
# # #                 } else {
# # #                     return {
# # #                         url: limpiarUrl(config.icono_url_off) || limpiarUrl(config.icono_url) || null,
# # #                         color: config.color_off || config.color || (tipo === 'pozo' ? '#e74c3c' : '#9b59b6')
# # #                     };
# # #                 }
# # #             }
            
# # #             // Tanque (manejado por función especial)
# # #             if (tipo === 'tanque') {
# # #                 return {
# # #                     url: limpiarUrl(config.icono_url) || null,
# # #                     color: config.color || '#3498db'
# # #                 };
# # #             }
            
# # #             // Otros tipos (sensor, etc.)
# # #             return {
# # #                 url: limpiarUrl(config.icono_url) || null,
# # #                 color: config.color || '#7f8c8d'
# # #             };
# # #         }
        
# # #         // ========================================
# # #         // CREAR ÍCONO PARA MARCADOR (CORREGIDO - SOPORTE COMPLETO DE ESTADO + SENSOR CON BARRA)
# # #         // ========================================
# # #         function crearIcono(estacion) {
# # #             const tipo = estacion.tipo || 'generico';
# # #             const offline = esOffline(estacion.en_linea);
# # #             const estado = parseInt(estacion.estado_bomba || estacion.estado || 0);
# # #             const nivel = obtenerNivelTanque(estacion);
            
# # #             // ESPECIAL: Tanques siempre usan icono de tanque + barra de llenado
# # #             if (tipo === 'tanque') {
# # #                 const configTanque = (DATOS_INICIALES.tipos || {}).tanque || {};
# # #                 const iconoUrl = limpiarUrl(configTanque.icono_url) || null;
# # #                 return crearIconoTanque(iconoUrl, nivel, offline);
# # #             }
            
# # #             // ESPECIAL: Sensores de nivel de río también usan barra de llenado (color azul oscuro)
# # #             if (tipo === 'sensor') {
# # #                 const configSensor = (DATOS_INICIALES.tipos || {}).sensor || {};
# # #                 const iconoUrl = limpiarUrl(configSensor.icono_url) || null;
# # #                 return crearIconoRio(iconoUrl, nivel, offline);
# # #             }
            
# # #             // Obtener icono según tipo y estado (para pozo, bomba, rebombeo)
# # #             const iconoInfo = getIconoTipo(tipo, estado);
            
# # #             // Si está offline, envolver el icono con borde rojo
# # #             if (offline && iconoInfo.url) {
# # #                 return L.divIcon({
# # #                     html: `<div style="
# # #                         width: 32px;
# # #                         height: 32px;
# # #                         border: 3px solid #e74c3c;
# # #                         border-radius: 4px;
# # #                         display: flex;
# # #                         align-items: center;
# # #                         justify-content: center;
# # #                         box-sizing: border-box;
# # #                         box-shadow: 0 2px 6px rgba(231, 76, 60, 0.5);
# # #                     ">
# # #                         <img src="${iconoInfo.url}" width="26" height="26" style="display:block;">
# # #                     </div>`,
# # #                     iconSize: [32, 32],
# # #                     iconAnchor: [16, 16],
# # #                     popupAnchor: [0, -16]
# # #                 });
# # #             }
            
# # #             // Si tiene URL de icono, usarla directamente
# # #             if (iconoInfo.url) {
# # #                 return L.icon({
# # #                     iconUrl: iconoInfo.url,
# # #                     iconSize: [32, 32],
# # #                     iconAnchor: [16, 16],
# # #                     popupAnchor: [0, -16]
# # #                 });
# # #             }
            
# # #             // Fallback: icono genérico con color + borde rojo si offline
# # #             const borderColor = offline ? '#e74c3c' : iconoInfo.color;
# # #             const bgColor = offline ? 'rgba(231, 76, 60, 0.1)' : iconoInfo.color;
# # #             return L.divIcon({
# # #                 html: `<div style="
# # #                     width: 32px;
# # #                     height: 32px;
# # #                     border: 2px solid ${borderColor};
# # #                     border-radius: 50%;
# # #                     display: flex;
# # #                     align-items: center;
# # #                     justify-content: center;
# # #                     box-sizing: border-box;
# # #                     background: ${bgColor};
# # #                 ">
# # #                     <div style="
# # #                         width: 20px;
# # #                         height: 20px;
# # #                         border-radius: 50%;
# # #                         background: white;
# # #                     "></div>
# # #                 </div>`,
# # #                 iconSize: [32, 32],
# # #                 iconAnchor: [16, 16],
# # #                 popupAnchor: [0, -16]
# # #             });
# # #         }
        
# # #         // ========================================
# # #         // CREAR POPUP
# # #         // ========================================
# # #         function crearPopupContent(estacion) {
# # #             let html = `<div class="custom-popup"><h4>${estacion.nombre || 'Estación'}</h4><hr>`;
            
# # #             const offline = esOffline(estacion.en_linea);
# # #             const estadoLinea = offline ? '<span class="status-offline">Fuera de línea</span>' : '<span class="status-online">En línea</span>';
# # #             html += `<div class="var-row"><span class="var-label">Estado:</span><span class="var-value">${estadoLinea}</span></div>`;
            
# # #             if (estacion.tipo === 'tanque' || estacion.tipo === 'sensor') {
# # #                 html += `<div class="var-row"><span class="var-label">Nivel:</span><span class="var-value">${obtenerNivelTanque(estacion)}%</span></div>`;
# # #             } else if (estacion.tipo === 'pozo' || estacion.tipo === 'bomba' || estacion.tipo === 'rebombeo') {
# # #                 const estadoBomba = parseInt(estacion.estado_bomba || estacion.estado || 0);
# # #                 const estadoTexto = estadoBomba === 1 ? '<span style="color:#27ae60;font-weight:bold;">Encendido</span>' : '<span style="color:#e74c3c;font-weight:bold;">Apagado</span>';
# # #                 html += `<div class="var-row"><span class="var-label">Estado Bomba:</span><span class="var-value">${estadoTexto}</span></div>`;
# # #             }
            
# # #             for (const key in estacion) {
# # #                 if (!['nombre', 'latitud', 'longitud', 'tipo', 'estado_bomba', 'en_linea', 'icono', 'icono_url', 'icono_url_on', 'icono_url_off', 'Nivel', 'nivel', 'Porcentaje (%)', 'Porcentaje', '_timestamp_actualizacion'].includes(key)) {
# # #                     const value = typeof estacion[key] === 'number'
# # #                         ? estacion[key].toLocaleString('es-ES', { minimumFractionDigits: 2, maximumFractionDigits: 2 })
# # #                         : estacion[key];
# # #                     html += `<div class="var-row"><span class="var-label">${key}:</span><span class="var-value">${value}</span></div>`;
# # #                 }
# # #             }
            
# # #             html += `<hr><div class="timestamp">📅 ${new Date().toLocaleString('es-ES')}</div></div>`;
# # #             return html;
# # #         }
        
# # #         // ========================================
# # #         // ACTUALIZAR ESTADÍSTICAS CON ICONOS DE TIPOS
# # #         // ========================================
# # #         function actualizarEstadisticas(datos) {
# # #             if (!datos || !datos.estaciones) return;
            
# # #             // Contadores
# # #             let total = 0;
# # #             let pozos_encendidos = 0;
# # #             let pozos_apagados = 0;
# # #             let tanques = 0;
# # #             let bombas_encendidas = 0;
# # #             let bombas_apagadas = 0;
# # #             let rebombeos_encendidos = 0;
# # #             let rebombeos_apagados = 0;
# # #             let sensores = 0;
# # #             let offline_count = 0;
# # #             let online = 0;
            
# # #             datos.estaciones.forEach(estacion => {
# # #                 total++;
# # #                 const offline = esOffline(estacion.en_linea);
# # #                 const tipo = estacion.tipo || 'generico';
# # #                 const estado = parseInt(estacion.estado_bomba || estacion.estado || 0);
                
# # #                 if (offline) {
# # #                     offline_count++;
# # #                 } else {
# # #                     online++;
# # #                     if (tipo === 'pozo') {
# # #                         if (estado === 1) pozos_encendidos++;
# # #                         else pozos_apagados++;
# # #                     } else if (tipo === 'tanque') {
# # #                         tanques++;
# # #                     } else if (tipo === 'bomba') {
# # #                         if (estado === 1) bombas_encendidas++;
# # #                         else bombas_apagadas++;
# # #                     } else if (tipo === 'rebombeo') {
# # #                         if (estado === 1) rebombeos_encendidos++;
# # #                         else rebombeos_apagados++;
# # #                     } else if (tipo === 'sensor') {
# # #                         sensores++;
# # #                     }
# # #                 }
# # #             });
            
# # #             // Obtener configuración de tipos
# # #             const tipos = datos.tipos || {};
            
# # #             // Definir las estadísticas a mostrar
# # #             const stats = [
# # #                 { tipo: 'total', value: total, label: 'Total' },
# # #                 { tipo: 'pozo', estado: 1, value: pozos_encendidos, label: 'Pozos Enc.' },
# # #                 { tipo: 'pozo', estado: 0, value: pozos_apagados, label: 'Pozos Apag.' },
# # #                 { tipo: 'tanque', value: tanques, label: 'Tanques' },
# # #                 { tipo: 'bomba', estado: 1, value: bombas_encendidas, label: 'Bombas Enc.' },
# # #                 { tipo: 'bomba', estado: 0, value: bombas_apagadas, label: 'Bombas Apag.' },
# # #                 { tipo: 'rebombeo', estado: 1, value: rebombeos_encendidos, label: 'Rebom. Enc.' },
# # #                 { tipo: 'rebombeo', estado: 0, value: rebombeos_apagados, label: 'Rebom. Apag.' },
# # #                 { tipo: 'sensor', value: sensores, label: 'Sensores Río' },
# # #                 { tipo: 'offline', value: offline_count, label: 'Offline' },
# # #                 { tipo: 'online', value: online, label: 'Online' },
# # #                 { tipo: 'reloj', value: '""" + tiempo_str + """', label: 'Actualizado' }
# # #             ];
            
# # #             // Crear barra de estadísticas
# # #             const statsBar = document.getElementById('stats-bar');
# # #             if (!statsBar) return;
# # #             statsBar.innerHTML = '';
            
# # #             // Crear cada item
# # #             stats.forEach(stat => {
# # #                 const config = tipos[stat.tipo] || tipos['generico'] || {};
# # #                 let iconoUrl = null;
                
# # #                 // Manejar tipos con estado
# # #                 if (stat.tipo === 'pozo' || stat.tipo === 'bomba' || stat.tipo === 'rebombeo') {
# # #                     iconoUrl = stat.estado === 1 ?
# # #                         (limpiarUrl(config.icono_url_on) || limpiarUrl(config.icono_url) || null) :
# # #                         (limpiarUrl(config.icono_url_off) || limpiarUrl(config.icono_url) || null);
# # #                 }
                
# # #                 // Tipos especiales con iconos base64
# # #                 else if (stat.tipo === 'offline') {
# # #                     iconoUrl = 'https://raw.githubusercontent.com/AlarmasCiateq/SCADA_T/main/iconos/Offline.svg';
# # #                 } else if (stat.tipo === 'online') {
# # #                     iconoUrl = 'https://raw.githubusercontent.com/AlarmasCiateq/SCADA_T/main/iconos/Online_Alarma.svg';
# # #                 } else if (stat.tipo === 'total') {
# # #                     iconoUrl = 'https://raw.githubusercontent.com/AlarmasCiateq/SCADA_T/main/iconos/transmite.svg';
# # #                 } else if (stat.tipo === 'reloj') {
# # #                     iconoUrl = 'https://raw.githubusercontent.com/AlarmasCiateq/SCADA_T/main/iconos/update.svg';
# # #                 }
                
# # #                 // Otros tipos
# # #                 else {
# # #                     iconoUrl = limpiarUrl(config.icono_url) || null;
# # #                 }
                
# # #                 const item = document.createElement('div');
# # #                 item.className = 'stat-item';
                
# # #                 let iconHtml = '';
# # #                 if (iconoUrl) {
# # #                     iconHtml = `<div class="stat-icon"><img src="${iconoUrl}" alt="${stat.tipo}"></div>`;
# # #                 } else {
# # #                     const color = config.color || '#7f8c8d';
# # #                     iconHtml = `<div class="stat-icon" style="color:${color};font-size:20px;">●</div>`;
# # #                 }
                
# # #                 item.innerHTML =
# # #                     iconHtml +
# # #                     '<div class="stat-value">' + stat.value + '</div>' +
# # #                     '<div class="stat-label">' + stat.label + '</div>';
                
# # #                 statsBar.appendChild(item);
# # #             });
# # #         }
        
# # #         // ========================================
# # #         // FUNCIÓN PARA ZOOM A TODOS LOS ICONOS
# # #         // ========================================
# # #         function zoomATodosLosIconos() {
# # #             if (!map || markers.size === 0) return;
# # #             const todasCoords = Array.from(markers.values()).map(m => m.getLatLng());
# # #             map.fitBounds(todasCoords, { padding: [40, 40] });
# # #             try {
# # #                 localStorage.setItem('scada_map_zoom', map.getZoom().toString());
# # #                 localStorage.setItem('scada_map_center', JSON.stringify({lat: map.getCenter().lat, lng: map.getCenter().lng}));
# # #             } catch(e) {}
# # #         }
        
# # #         // ========================================
# # #         // CONTROL PERSONALIZADO DE LEAFLET
# # #         // ========================================
# # #         L.Control.ZoomAll = L.Control.extend({
# # #             options: { position: 'topleft' },
# # #             onAdd: function(map) {
# # #                 const container = L.DomUtil.create('div', 'leaflet-bar leaflet-control leaflet-control-zoom-all');
# # #                 const button = L.DomUtil.create('a', 'leaflet-control-zoom-all', container);
# # #                 button.href = '#';
# # #                 button.title = 'Ver todas las estaciones';
# # #                 button.innerHTML = '<i>⌂</i>';
# # #                 L.DomEvent.disableClickPropagation(button);
# # #                 L.DomEvent.on(button, 'click', function(e) {
# # #                     L.DomEvent.stopPropagation(e);
# # #                     L.DomEvent.preventDefault(e);
# # #                     zoomATodosLosIconos();
# # #                 });
# # #                 return container;
# # #             }
# # #         });
        
# # #         L.control.zoomAll = function(opts) { return new L.Control.ZoomAll(opts); };
        
# # #         // ========================================
# # #         // INICIALIZAR MAPA
# # #         // ========================================
# # #         function initMap() {
# # #             try {
# # #                 map = L.map('map', {
# # #                     zoomControl: true,
# # #                     scrollWheelZoom: true,
# # #                     dragging: true
# # #                 });
                
# # #                 L.tileLayer('https://{s}.basemaps.cartocdn.com/light_all/{z}/{x}/{y}{r}.png', {
# # #                     attribution: '',
# # #                     subdomains: 'abcd',
# # #                     maxZoom: 19
# # #                 }).addTo(map);
                
# # #                 L.control.zoomAll().addTo(map);
                
# # #                 // Restaurar zoom/centro
# # #                 const savedZoom = localStorage.getItem('scada_map_zoom');
# # #                 const savedCenter = localStorage.getItem('scada_map_center');
# # #                 const wasInitialized = localStorage.getItem('scada_map_initialized') === 'true';
# # #                 let hizoFitBounds = false;
                
# # #                 if (wasInitialized && savedZoom && savedCenter) {
# # #                     try {
# # #                         const center = JSON.parse(savedCenter);
# # #                         map.setView([center.lat, center.lng], parseInt(savedZoom));
# # #                         console.log('✓ Zoom restaurado:', savedZoom);
# # #                     } catch(e) {
# # #                         console.log('Error restaurando zoom:', e);
# # #                     }
# # #                 } else {
# # #                     const todasCoords = [];
# # #                     DATOS_INICIALES.estaciones.forEach(est => {
# # #                         if (est.latitud && est.longitud) {
# # #                             todasCoords.push([parseFloat(est.latitud), parseFloat(est.longitud)]);
# # #                         }
# # #                     });
# # #                     if (todasCoords.length > 0) {
# # #                         map.fitBounds(todasCoords, { padding: [40, 40] });
# # #                         console.log('✓ Zoom inicial ajustado');
# # #                         hizoFitBounds = true;
# # #                     }
# # #                 }
                
# # #                 // Agregar marcadores
# # #                 DATOS_INICIALES.estaciones.forEach(estacion => {
# # #                     if (!estacion.latitud || !estacion.longitud) return;
# # #                     const id = estacion.nombre || `${estacion.latitud},${estacion.longitud}`;
# # #                     const lat = parseFloat(estacion.latitud);
# # #                     const lng = parseFloat(estacion.longitud);
# # #                     const marker = L.marker([lat, lng], { icon: crearIcono(estacion) })
# # #                         .bindPopup(crearPopupContent(estacion), { maxWidth: 320 })
# # #                         .bindTooltip(estacion.nombre || 'Estación', { permanent: false, direction: 'top', opacity: 0.9 })
# # #                         .addTo(map);
# # #                     markers.set(id, marker);
# # #                 });
                
# # #                 if (!hizoFitBounds && markers.size > 0 && !wasInitialized) {
# # #                     const todasCoords = Array.from(markers.values()).map(m => m.getLatLng());
# # #                     map.fitBounds(todasCoords, { padding: [40, 40] });
# # #                     localStorage.setItem('scada_map_initialized', 'true');
# # #                 }
                
# # #                 // Actualizar estadísticas
# # #                 actualizarEstadisticas(DATOS_INICIALES);
                
# # #                 // Ocultar loading
# # #                 document.getElementById('loading').classList.add('hidden');
# # #                 window.map = map;
                
# # #             } catch(e) {
# # #                 document.getElementById('loading').innerHTML = `<div style="color:#e74c3c;text-align:center;padding:20px;">❌ Error: ${e.message}</div>`;
# # #                 console.error('Error:', e);
# # #             }
# # #         }
        
# # #         if (document.readyState === 'loading') {
# # #             document.addEventListener('DOMContentLoaded', initMap);
# # #         } else {
# # #             initMap();
# # #         }
# # #     </script>
# # # </body>
# # # </html>
# # # """

# # # # Renderizar el mapa
# # # st.components.v1.html(
# # #     html_completo,
# # #     width=1920,
# # #     height=1080,
# # #     scrolling=False
# # # )

# # # # ========================================
# # # # FORZAR RECARGA COMPLETA CADA 60 SEGUNDOS (1 MINUTO)
# # # # ========================================
# # # time.sleep(60)
# # # st.rerun()



# # import streamlit as st
# # import requests
# # import json
# # import base64
# # from datetime import datetime
# # import os
# # import time

# # # ========================================
# # # FUNCIÓN PARA OBTENER EL FAVICON DESDE GITHUB
# # # ========================================
# # def obtener_favicon_github():
# #     """Descarga el icono de GitHub y lo convierte a base64"""
# #     try:
# #         GITHUB_USER = "AlarmasCiateq"
# #         REPO_NAME = "SCADA_T"
# #         BRANCH = "main"
# #         ICON_PATH = "iconos/ICONO CIATEQ 256.ico"
        
# #         # CAMBIO 4: Quitados los espacios en la URL
# #         raw_url = f"https://raw.githubusercontent.com/{GITHUB_USER}/{REPO_NAME}/{BRANCH}/{ICON_PATH}"
# #         print(raw_url)
# #         headers = {'User-Agent': 'SCADA-Monitor'}
# #         response = requests.get(raw_url, headers=headers, timeout=10)
# #         response.raise_for_status()
        
# #         icon_base64 = base64.b64encode(response.content).decode('utf-8')
# #         return f"image/x-icon;base64,{icon_base64}"
# #     except Exception as e:
# #         print(f"Error cargando favicon: {e}")
# #         return None

# # # ========================================
# # # CONFIGURACIÓN DE PÁGINA
# # # ========================================
# # favicon_data = obtener_favicon_github()

# # if favicon_data:
# #     st.set_page_config(
# #         page_title="SCADA CIATEQ",
# #         page_icon="🌎",
# #         layout="wide",
# #         initial_sidebar_state="collapsed"
# #     )
    
# #     st.markdown(f"""
# #     <link rel="icon" href="{favicon_data}" type="image/x-icon">
# #     <link rel="shortcut icon" href="{favicon_data}" type="image/x-icon">
# #     """, unsafe_allow_html=True)
# # else:
# #     st.set_page_config(
# #         page_title="SCADA CIATEQ",
# #         page_icon="🏭",
# #         layout="wide",
# #         initial_sidebar_state="collapsed"
# #     )

# # st.markdown("""
# # <style>
# # [data-testid="stSidebar"] { display: none !important; }
# # [data-testid="stHeader"] { display: none !important; }
# # [data-testid="stDecoration"] { display: none !important; }
# # header { display: none !important; }
# # #MainMenu { display: none !important; }
# # footer { display: none !important; }
# # .stApp { background-color: #0e1117; padding: 0 !important; margin: 0 !important; overflow: hidden !important; }
# # .block-container { padding: 0 !important; max-width: 100% !important; margin: 0 !important; overflow: hidden !important; }
# # .main { padding: 0 !important; margin: 0 !important; overflow: hidden !important; }
# # .block-container > div { padding: 0 !important; margin: 0 !important; }
# # ::-webkit-scrollbar { display: none !important; }
# # body { overflow: hidden !important; }
# # #loading {
# #     position: fixed;
# #     top: 0;
# #     left: 0;
# #     width: 100%;
# #     height: 100%;
# #     background: #0e1117;
# #     display: flex;
# #     justify-content: center;
# #     align-items: center;
# #     color: #3498db;
# #     font-family: Arial;
# #     font-size: 18px;
# #     z-index: 9999;
# #     transition: opacity 0.1s;
# # }
# # #loading.hidden {
# #     opacity: 0;
# #     pointer-events: none;
# # }
# # #debug-timestamp {
# #     position: fixed;
# #     bottom: 5px;
# #     right: 10px;
# #     background: rgba(0,0,0,0.7);
# #     color: #27ae60;
# #     padding: 3px 8px;
# #     font-family: monospace;
# #     font-size: 11px;
# #     border-radius: 3px;
# #     z-index: 1000;
# # }
# # </style>
# # """, unsafe_allow_html=True)

# # # ========================================
# # # OBTENER TOKEN DE GITHUB
# # # ========================================
# # def obtener_token_github():
# #     try:
# #         if hasattr(st, 'secrets') and "GITHUB_TOKEN" in st.secrets:
# #             return st.secrets["GITHUB_TOKEN"]
# #     except:
# #         pass
# #     return os.getenv("GITHUB_TOKEN", None)

# # # ========================================
# # # CARGAR DATOS FRESH DE GITHUB (CADA EJECUCIÓN)
# # # ========================================
# # def cargar_datos_github(max_intentos=3):
# #     token = obtener_token_github()
# #     for intento in range(max_intentos):
# #         try:
# #             GITHUB_USER = "AlarmasCiateq"
# #             REPO_NAME = "SCADA_T"
# #             BRANCH = "main"
# #             FILE_PATH = "datos_estaciones.json"
            
# #             # CAMBIO 4 (parte 2): Quitados los espacios en la URL de la API
# #             api_url = f"https://api.github.com/repos/{GITHUB_USER}/{REPO_NAME}/contents/{FILE_PATH}?ref={BRANCH}"
            
# #             headers = {
# #                 'User-Agent': f'SCADA-Monitor-{datetime.now().timestamp()}',
# #                 'Accept': 'application/vnd.github.v3+json'
# #             }
            
# #             if token:
# #                 headers['Authorization'] = f'token {token}'
            
# #             response = requests.get(api_url, headers=headers, timeout=10)
# #             response.raise_for_status()
            
# #             data = response.json()
# #             content_bytes = base64.b64decode(data['content'])
# #             content_str = content_bytes.decode('utf-8')
# #             datos = json.loads(content_str)
            
# #             datos['_timestamp_actualizacion'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
# #             return datos, True
            
# #         except Exception as e:
# #             print(f"Error cargando datos (intento {intento + 1}): {e}")
# #             if intento < max_intentos - 1:
# #                 time.sleep(1)
# #                 continue
# #             return None, False
# #     return None, False

# # # ========================================
# # # CARGAR DATOS FRESH EN CADA EJECUCIÓN
# # # ========================================
# # datos, exito = cargar_datos_github()

# # if not datos or not exito:
# #     st.markdown("""
# #     <div style="position:fixed;top:0;left:0;width:100%;height:100%;background:#0e1117;color:white;
# #     display:flex;justify-content:center;align-items:center;font-family:Arial;">
# #         <div style="text-align:center;padding:20px;">
# #             <h2>🛢️ SCADA Monitor</h2>
# #             <p style="color:#e74c3c; margin-top:15px;">Error: No se pudieron cargar los datos de GitHub</p>
# #             <p style="font-size:14px; margin-top:10px; color:#95a5a6;">Verifique conexión a internet</p>
# #         </div>
# #     </div>
# #     """, unsafe_allow_html=True)
# #     time.sleep(60)
# #     st.rerun()

# # # ========================================
# # # PREPARAR DATOS PARA HTML
# # # ========================================
# # tiempo_str = datetime.now().strftime('%H:%M:%S')
# # timestamp_debug = datos.get('_timestamp_actualizacion', tiempo_str)

# # datos_json_safe = json.dumps(datos, ensure_ascii=False)
# # datos_json_safe = (datos_json_safe.replace('\\', '\\\\')
# #     .replace("'", "\\'")
# #     .replace('</', '<\\/')
# #     .replace('\n', '\\n')
# #     .replace('\r', '\\r')
# #     .replace('\t', '\\t'))

# # # ========================================
# # # HTML + JAVASCRIPT
# # # ========================================
# # html_completo = """
# # <!DOCTYPE html>
# # <html lang="es">
# # <head>
# #     <meta charset="UTF-8">
# #     <meta name="viewport" content="width=device-width, initial-scale=1.0">
# #     <title>SCADA Monitor</title>
# #     <link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css" />
# #     <style>
# #         * { margin: 0; padding: 0; box-sizing: border-box; }
# #         body { font-family: Arial, sans-serif; background: #0e1117; overflow: hidden; height: 100vh; width: 100vw; }
# #         #map { position: absolute; top: 0; left: 0; width: 100%; height: 100%; z-index: 1; }
        
# #         #stats-bar {
# #             position: fixed;
# #             top: 10px;
# #             right: 15px;
# #             background: rgba(255, 255, 255, 0.95);
# #             padding: 8px;
# #             border-radius: 6px;
# #             box-shadow: 0 2px 8px rgba(0,0,0,0.15);
# #             z-index: 1000;
# #             display: flex;
# #             gap: 12px;
# #             align-items: center;
# #             font-family: Arial, sans-serif;
# #             flex-wrap: nowrap;
# #             overflow-x: auto;
# #             max-width: 90%;
# #         }
        
# #         .stat-item {
# #             display: flex;
# #             flex-direction: column;
# #             align-items: center;
# #             min-width: 65px;
# #         }
        
# #         .stat-icon {
# #             width: 24px;
# #             height: 24px;
# #             margin-bottom: 2px;
# #             display: flex;
# #             align-items: center;
# #             justify-content: center;
# #         }
        
# #         .stat-icon img {
# #             width: 100%;
# #             height: 100%;
# #             object-fit: contain;
# #         }
        
# #         .stat-value {
# #             font-weight: bold;
# #             color: #2c3e50;
# #             font-size: 14px;
# #             text-align: center;
# #         }
        
# #         .stat-label {
# #             font-size: 8px;
# #             color: #7f8c8d;
# #             text-align: center;
# #             white-space: nowrap;
# #             text-transform: uppercase;
# #             letter-spacing: 0.5px;
# #         }
        
# #         .custom-popup {
# #             font-family: Arial;
# #             padding: 12px;
# #             min-width: 280px;
# #             background: white;
# #             border-radius: 6px;
# #         }
        
# #         .custom-popup h4 {
# #             margin: 0 0 10px 0;
# #             color: #2c3e50;
# #             font-size: 16px;
# #             font-weight: bold;
# #         }
        
# #         .custom-popup hr {
# #             margin: 8px 0;
# #             border-color: #ecf0f1;
# #         }
        
# #         .custom-popup .var-row {
# #             margin: 6px 0;
# #             padding: 4px 0;
# #             display: flex;
# #             justify-content: space-between;
# #         }
        
# #         .custom-popup .var-label {
# #             color: #2c3e50;
# #             font-weight: 600;
# #             font-size: 13px;
# #             min-width: 120px;
# #         }
        
# #         .custom-popup .var-value {
# #             color: #2c3e50;
# #             font-weight: bold;
# #             font-size: 14px;
# #             text-align: right;
# #             min-width: 80px;
# #         }
        
# #         .custom-popup .timestamp {
# #             font-size: 11px;
# #             color: #95a5a6;
# #             text-align: center;
# #             margin-top: 8px;
# #         }
        
# #         .status-online { color: #27ae60; font-weight: bold; }
# #         .status-offline { color: #e74c3c; font-weight: bold; }
        
# #         #loading {
# #             position: fixed;
# #             top: 0;
# #             left: 0;
# #             width: 100%;
# #             height: 100%;
# #             background: #0e1117;
# #             display: flex;
# #             justify-content: center;
# #             align-items: center;
# #             color: #3498db;
# #             font-family: Arial;
# #             font-size: 18px;
# #             z-index: 9999;
# #             transition: opacity 0.1s;
# #         }
        
# #         #loading.hidden {
# #             opacity: 0;
# #             pointer-events: none;
# #         }
        
# #         #debug-timestamp {
# #             position: fixed;
# #             bottom: 5px;
# #             right: 10px;
# #             background: rgba(0,0,0,0.7);
# #             color: #27ae60;
# #             padding: 3px 8px;
# #             font-family: monospace;
# #             font-size: 11px;
# #             border-radius: 3px;
# #             z-index: 1000;
# #         }
        
# #         .leaflet-control-zoom-all {
# #             background: #fff;
# #             border: 2px solid rgba(0,0,0,0.2);
# #             border-radius: 4px;
# #             box-shadow: 0 1px 5px rgba(0,0,0,0.4);
# #             cursor: pointer;
# #             margin-top: 5px;
# #             transition: all 0.2s;
# #         }
        
# #         .leaflet-control-zoom-all:hover {
# #             background: #f4f4f4;
# #             box-shadow: 0 1px 7px rgba(0,0,0,0.45);
# #         }
        
# #         .leaflet-control-zoom-all:active {
# #             background: #e8e8e8;
# #         }
        
# #         .leaflet-control-zoom-all i {
# #             display: block;
# #             width: 30px;
# #             height: 30px;
# #             line-height: 30px;
# #             text-align: center;
# #             font-weight: bold;
# #             color: #333;
# #             font-size: 20px;
# #         }
        
# #         .leaflet-control-zoom-all:hover i {
# #             color: #2c3e50;
# #         }
# #     </style>
# # </head>
# # <body>
# #     <div id="loading">Cargando...</div>
# #     <div id="map"></div>
# #     <div id="stats-bar"></div>
# #     <div id="debug-timestamp">""" + timestamp_debug + """</div>
    
# #     <script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"></script>
# #     <script>
# #         window.addEventListener('beforeunload', function() {
# #             if (window.map) {
# #                 try {
# #                     const zoom = window.map.getZoom();
# #                     const center = window.map.getCenter();
# #                     localStorage.setItem('scada_map_zoom', zoom.toString());
# #                     localStorage.setItem('scada_map_center', JSON.stringify({lat: center.lat, lng: center.lng}));
# #                     localStorage.setItem('scada_map_initialized', 'true');
# #                 } catch(e) {}
# #             }
# #         });
        
# #         const DATOS_INICIALES = """ + datos_json_safe + """;
# #         let map = null;
# #         let markers = new Map();
        
# #         function limpiarUrl(url) {
# #             if (!url) return null;
# #             return url.trim().replace(/\\s+/g, '%20');
# #         }
        
# #         function esOffline(enLinea) {
# #             if (enLinea === undefined || enLinea === null) return false;
# #             const valor = String(enLinea).trim().toLowerCase();
# #             return valor === '0' || valor === 'false' || valor === 'off' || valor === 'no';
# #         }
        
# #         function obtenerNivelTanque(estacion) {
# #             const campos = ['Porcentaje (%)', 'Porcentaje', 'Nivel (%)', 'nivel_%', 'Nivel', 'nivel'];
# #             for (let campo of campos) {
# #                 if (estacion[campo] !== undefined) {
# #                     let v = parseFloat(estacion[campo]);
# #                     return Math.max(0, Math.min(100, isNaN(v) ? 0 : v));
# #                 }
# #             }
# #             return 0;
# #         }
        
# #         function crearIconoTanque(iconoUrl, nivel, offline = false) {
# #             const alturaLlenado = Math.round((nivel / 100) * 28);
# #             const bordeStyle = offline ?
# #                 'box-shadow: 0 0 0 3px #e74c3c, 0 2px 6px rgba(231, 76, 60, 0.5);' :
# #                 '';
            
# #             if (iconoUrl) {
# #                 return L.divIcon({
# #                     html: `<div style="position:relative;width:32px;height:32px;${bordeStyle}">
# #                         <div style="position:absolute;bottom:0;left:0;width:32px;height:${alturaLlenado}px;background:rgba(52,152,219,0.85);"></div>
# #                         <img src="${iconoUrl}" width="32" height="32" style="position:absolute;top:0;left:0;z-index:1;">
# #                         <div style="position:absolute;bottom:4px;width:32px;text-align:center;font-size:11px;color:blue;font-weight:bold;text-shadow:0 1px 2px rgba(0,0,0,0.8)">${Math.round(nivel)}%</div>
# #                     </div>`,
# #                     iconSize: [32, 32],
# #                     iconAnchor: [16, 16],
# #                     popupAnchor: [0, -16]
# #                 });
# #             } else {
# #                 const yInicio = 28 - alturaLlenado;
# #                 const svg = `<svg xmlns="http://www.w3.org/2000/svg" width="32" height="32" viewBox="0 0 32 32">
# #                     <rect x="0" y="${yInicio}" width="32" height="${alturaLlenado}" fill="rgba(52,152,219,0.85)"/>
# #                     <rect x="2" y="4" width="28" height="24" fill="#2c3e50"/>
# #                     <text x="16" y="20" font-family="Arial" font-size="9" fill="white" text-anchor="middle" font-weight="bold">${Math.round(nivel)}%</text>
# #                 </svg>`;
                
# #                 return L.divIcon({
# #                     html: `<div style="position:relative;width:32px;height:32px;${bordeStyle}">${svg}</div>`,
# #                     iconSize: [32, 32],
# #                     iconAnchor: [16, 16],
# #                     popupAnchor: [0, -16]
# #                 });
# #             }
# #         }
        
# #         function crearIconoRio(iconoUrl, nivel, offline = false) {
# #             const alturaLlenado = Math.round((nivel / 100) * 28);
# #             const bordeStyle = offline ?
# #                 'box-shadow: 0 0 0 3px #e74c3c, 0 2px 6px rgba(231, 76, 60, 0.5);' :
# #                 '';
            
# #             if (iconoUrl) {
# #                 return L.divIcon({
# #                     html: `<div style="position:relative;width:32px;height:32px;${bordeStyle}">
# #                         <div style="position:absolute;bottom:0;left:0;width:32px;height:${alturaLlenado}px;background:rgba(52,152,219,0.85);"></div>
# #                         <img src="${iconoUrl}" width="32" height="32" style="position:absolute;top:0;left:0;z-index:1;">
# #                         <div style="position:absolute;bottom:4px;width:32px;text-align:center;font-size:11px;color:blue;font-weight:bold;text-shadow:0 1px 2px rgba(0,0,0,0.8)">${Math.round(nivel)}%</div>
# #                     </div>`,
# #                     iconSize: [32, 32],
# #                     iconAnchor: [16, 16],
# #                     popupAnchor: [0, -16]
# #                 });
# #             } else {
# #                 const yInicio = 28 - alturaLlenado;
# #                 const svg = `<svg xmlns="http://www.w3.org/2000/svg" width="32" height="32" viewBox="0 0 32 32">
# #                     <rect x="0" y="${yInicio}" width="32" height="${alturaLlenado}" fill="rgba(52,152,219,0.85)"/>
# #                     <path d="M4 18 Q16 12 28 18 L28 28 Q16 24 4 28 Z" fill="#2c3e50"/>
# #                     <text x="16" y="20" font-family="Arial" font-size="9" fill="blue" text-anchor="middle" font-weight="bold">${Math.round(nivel)}%</text>
# #                 </svg>`;
                
# #                 return L.divIcon({
# #                     html: `<div style="position:relative;width:32px;height:32px;${bordeStyle}">${svg}</div>`,
# #                     iconSize: [32, 32],
# #                     iconAnchor: [16, 16],
# #                     popupAnchor: [0, -16]
# #                 });
# #             }
# #         }
        
# #         function getIconoTipo(tipo, estado = null) {
# #             const tipos = DATOS_INICIALES.tipos || {};
# #             const config = tipos[tipo] || tipos['generico'] || {};
            
# #             if (tipo === 'pozo' || tipo === 'bomba' || tipo === 'rebombeo') {
# #                 // CAMBIO 1: Comparar con texto "Encendido" en lugar de 1
# #                 if (estado === "Encendido") {
# #                     return {
# #                         url: limpiarUrl(config.icono_url_on) || limpiarUrl(config.icono_url) || null,
# #                         color: config.color_on || config.color || (tipo === 'pozo' ? '#27ae60' : '#9b59b6')
# #                     };
# #                 } else {
# #                     return {
# #                         url: limpiarUrl(config.icono_url_off) || limpiarUrl(config.icono_url) || null,
# #                         color: config.color_off || config.color || (tipo === 'pozo' ? '#e74c3c' : '#9b59b6')
# #                     };
# #                 }
# #             }
            
# #             if (tipo === 'tanque') {
# #                 return {
# #                     url: limpiarUrl(config.icono_url) || null,
# #                     color: config.color || '#3498db'
# #                 };
# #             }
            
# #             return {
# #                 url: limpiarUrl(config.icono_url) || null,
# #                 color: config.color || '#7f8c8d'
# #             };
# #         }
        
# #         function crearIcono(estacion) {
# #             const tipo = estacion.tipo || 'generico';
# #             const offline = esOffline(estacion.en_linea);
# #             // CAMBIO 2: Leer "Estado del Arrancador" como texto
# #             const estado = estacion["Estado del Arrancador"] || estacion.estado || "Apagado";
# #             const nivel = obtenerNivelTanque(estacion);
            
# #             if (tipo === 'tanque') {
# #                 const configTanque = (DATOS_INICIALES.tipos || {}).tanque || {};
# #                 const iconoUrl = limpiarUrl(configTanque.icono_url) || null;
# #                 return crearIconoTanque(iconoUrl, nivel, offline);
# #             }
            
# #             if (tipo === 'sensor') {
# #                 const configSensor = (DATOS_INICIALES.tipos || {}).sensor || {};
# #                 const iconoUrl = limpiarUrl(configSensor.icono_url) || null;
# #                 return crearIconoRio(iconoUrl, nivel, offline);
# #             }
            
# #             const iconoInfo = getIconoTipo(tipo, estado);
            
# #             if (offline && iconoInfo.url) {
# #                 return L.divIcon({
# #                     html: `<div style="
# #                         width: 32px;
# #                         height: 32px;
# #                         border: 3px solid #e74c3c;
# #                         border-radius: 4px;
# #                         display: flex;
# #                         align-items: center;
# #                         justify-content: center;
# #                         box-sizing: border-box;
# #                         box-shadow: 0 2px 6px rgba(231, 76, 60, 0.5);
# #                     ">
# #                         <img src="${iconoInfo.url}" width="26" height="26" style="display:block;">
# #                     </div>`,
# #                     iconSize: [32, 32],
# #                     iconAnchor: [16, 16],
# #                     popupAnchor: [0, -16]
# #                 });
# #             }
            
# #             if (iconoInfo.url) {
# #                 return L.icon({
# #                     iconUrl: iconoInfo.url,
# #                     iconSize: [32, 32],
# #                     iconAnchor: [16, 16],
# #                     popupAnchor: [0, -16]
# #                 });
# #             }
            
# #             const borderColor = offline ? '#e74c3c' : iconoInfo.color;
# #             const bgColor = offline ? 'rgba(231, 76, 60, 0.1)' : iconoInfo.color;
# #             return L.divIcon({
# #                 html: `<div style="
# #                     width: 32px;
# #                     height: 32px;
# #                     border: 2px solid ${borderColor};
# #                     border-radius: 50%;
# #                     display: flex;
# #                     align-items: center;
# #                     justify-content: center;
# #                     box-sizing: border-box;
# #                     background: ${bgColor};
# #                 ">
# #                     <div style="
# #                         width: 20px;
# #                         height: 20px;
# #                         border-radius: 50%;
# #                         background: white;
# #                     "></div>
# #                 </div>`,
# #                 iconSize: [32, 32],
# #                 iconAnchor: [16, 16],
# #                 popupAnchor: [0, -16]
# #             });
# #         }
        
# #         function crearPopupContent(estacion) {
# #             let html = `<div class="custom-popup"><h4>${estacion.nombre || 'Estación'}</h4><hr>`;
            
# #             const offline = esOffline(estacion.en_linea);
# #             const estadoLinea = offline ? '<span class="status-offline">Fuera de línea</span>' : '<span class="status-online">En línea</span>';
# #             html += `<div class="var-row"><span class="var-label">Estado:</span><span class="var-value">${estadoLinea}</span></div>`;
            
# #             if (estacion.tipo === 'tanque' || estacion.tipo === 'sensor') {
# #                 html += `<div class="var-row"><span class="var-label">Nivel:</span><span class="var-value">${obtenerNivelTanque(estacion)}%</span></div>`;
# #             } else if (estacion.tipo === 'pozo' || estacion.tipo === 'bomba' || estacion.tipo === 'rebombeo') {
# #                 // CAMBIO 3: Usar "Estado del Arrancador" con comparación de texto
# #                 const estadoArrancador = estacion["Estado del Arrancador"] || estacion.estado || "Apagado";
# #                 const estadoTexto = estadoArrancador === "Encendido" ? '<span style="color:#27ae60;font-weight:bold;">Encendido</span>' : '<span style="color:#e74c3c;font-weight:bold;">Apagado</span>';
# #                 html += `<div class="var-row"><span class="var-label">Estado del Arrancador:</span><span class="var-value">${estadoTexto}</span></div>`;
# #             }
            
# #             for (const key in estacion) {
# #                 // CAMBIO 3b: Filtrar "Estado del Arrancador" en lugar de "estado_bomba"
# #                 if (!['nombre', 'latitud', 'longitud', 'tipo', 'Estado del Arrancador', 'en_linea', 'icono', 'icono_url', 'icono_url_on', 'icono_url_off', 'Nivel', 'nivel', 'Porcentaje (%)', 'Porcentaje', '_timestamp_actualizacion'].includes(key)) {
# #                     const value = typeof estacion[key] === 'number'
# #                         ? estacion[key].toLocaleString('es-ES', { minimumFractionDigits: 2, maximumFractionDigits: 2 })
# #                         : estacion[key];
# #                     html += `<div class="var-row"><span class="var-label">${key}:</span><span class="var-value">${value}</span></div>`;
# #                 }
# #             }
            
# #             html += `<hr><div class="timestamp">📅 ${new Date().toLocaleString('es-ES')}</div></div>`;
# #             return html;
# #         }
        
# #         function actualizarEstadisticas(datos) {
# #             if (!datos || !datos.estaciones) return;
            
# #             let total = 0;
# #             let pozos_encendidos = 0;
# #             let pozos_apagados = 0;
# #             let tanques = 0;
# #             let bombas_encendidas = 0;
# #             let bombas_apagadas = 0;
# #             let rebombeos_encendidos = 0;
# #             let rebombeos_apagados = 0;
# #             let sensores = 0;
# #             let offline_count = 0;
# #             let online = 0;
            
# #             datos.estaciones.forEach(estacion => {
# #                 total++;
# #                 const offline = esOffline(estacion.en_linea);
# #                 const tipo = estacion.tipo || 'generico';
# #                 // CAMBIO 3c: Leer estado como texto
# #                 const estado = estacion["Estado del Arrancador"] || estacion.estado || "Apagado";
                
# #                 if (offline) {
# #                     offline_count++;
# #                 } else {
# #                     online++;
# #                     if (tipo === 'pozo') {
# #                         if (estado === "Encendido") pozos_encendidos++;
# #                         else pozos_apagados++;
# #                     } else if (tipo === 'tanque') {
# #                         tanques++;
# #                     } else if (tipo === 'bomba') {
# #                         if (estado === "Encendido") bombas_encendidas++;
# #                         else bombas_apagadas++;
# #                     } else if (tipo === 'rebombeo') {
# #                         if (estado === "Encendido") rebombeos_encendidos++;
# #                         else rebombeos_apagados++;
# #                     } else if (tipo === 'sensor') {
# #                         sensores++;
# #                     }
# #                 }
# #             });
            
# #             const tipos = datos.tipos || {};
            
# #             const stats = [
# #                 { tipo: 'total', value: total, label: 'Total' },
# #                 // CAMBIO 3d: Estados como texto en lugar de 1/0
# #                 { tipo: 'pozo', estado: "Encendido", value: pozos_encendidos, label: 'Pozos Enc.' },
# #                 { tipo: 'pozo', estado: "Apagado", value: pozos_apagados, label: 'Pozos Apag.' },
# #                 { tipo: 'tanque', value: tanques, label: 'Tanques' },
# #                 { tipo: 'bomba', estado: "Encendido", value: bombas_encendidas, label: 'Bombas Enc.' },
# #                 { tipo: 'bomba', estado: "Apagado", value: bombas_apagadas, label: 'Bombas Apag.' },
# #                 { tipo: 'rebombeo', estado: "Encendido", value: rebombeos_encendidos, label: 'Rebom. Enc.' },
# #                 { tipo: 'rebombeo', estado: "Apagado", value: rebombeos_apagados, label: 'Rebom. Apag.' },
# #                 { tipo: 'sensor', value: sensores, label: 'Sensores Río' },
# #                 { tipo: 'offline', value: offline_count, label: 'Offline' },
# #                 { tipo: 'online', value: online, label: 'Online' },
# #                 { tipo: 'reloj', value: '""" + tiempo_str + """', label: 'Actualizado' }
# #             ];
            
# #             const statsBar = document.getElementById('stats-bar');
# #             if (!statsBar) return;
# #             statsBar.innerHTML = '';
            
# #             stats.forEach(stat => {
# #                 const config = tipos[stat.tipo] || tipos['generico'] || {};
# #                 let iconoUrl = null;
                
# #                 if (stat.tipo === 'pozo' || stat.tipo === 'bomba' || stat.tipo === 'rebombeo') {
# #                     // CAMBIO 3e: Comparar con texto para seleccionar icono
# #                     iconoUrl = stat.estado === "Encendido" ?
# #                         (limpiarUrl(config.icono_url_on) || limpiarUrl(config.icono_url) || null) :
# #                         (limpiarUrl(config.icono_url_off) || limpiarUrl(config.icono_url) || null);
# #                 }
# #                 else if (stat.tipo === 'offline') {
# #                     iconoUrl = 'https://raw.githubusercontent.com/AlarmasCiateq/SCADA_T/main/iconos/Offline.svg';
# #                 } else if (stat.tipo === 'online') {
# #                     iconoUrl = 'https://raw.githubusercontent.com/AlarmasCiateq/SCADA_T/main/iconos/Online_Alarma.svg';
# #                 } else if (stat.tipo === 'total') {
# #                     iconoUrl = 'https://raw.githubusercontent.com/AlarmasCiateq/SCADA_T/main/iconos/transmite.svg';
# #                 } else if (stat.tipo === 'reloj') {
# #                     iconoUrl = 'https://raw.githubusercontent.com/AlarmasCiateq/SCADA_T/main/iconos/update.svg';
# #                 }
# #                 else {
# #                     iconoUrl = limpiarUrl(config.icono_url) || null;
# #                 }
                
# #                 const item = document.createElement('div');
# #                 item.className = 'stat-item';
                
# #                 let iconHtml = '';
# #                 if (iconoUrl) {
# #                     iconHtml = `<div class="stat-icon"><img src="${iconoUrl}" alt="${stat.tipo}"></div>`;
# #                 } else {
# #                     const color = config.color || '#7f8c8d';
# #                     iconHtml = `<div class="stat-icon" style="color:${color};font-size:20px;">●</div>`;
# #                 }
                
# #                 item.innerHTML =
# #                     iconHtml +
# #                     '<div class="stat-value">' + stat.value + '</div>' +
# #                     '<div class="stat-label">' + stat.label + '</div>';
                
# #                 statsBar.appendChild(item);
# #             });
# #         }
        
# #         function zoomATodosLosIconos() {
# #             if (!map || markers.size === 0) return;
# #             const todasCoords = Array.from(markers.values()).map(m => m.getLatLng());
# #             map.fitBounds(todasCoords, { padding: [40, 40] });
# #             try {
# #                 localStorage.setItem('scada_map_zoom', map.getZoom().toString());
# #                 localStorage.setItem('scada_map_center', JSON.stringify({lat: map.getCenter().lat, lng: map.getCenter().lng}));
# #             } catch(e) {}
# #         }
        
# #         L.Control.ZoomAll = L.Control.extend({
# #             options: { position: 'topleft' },
# #             onAdd: function(map) {
# #                 const container = L.DomUtil.create('div', 'leaflet-bar leaflet-control leaflet-control-zoom-all');
# #                 const button = L.DomUtil.create('a', 'leaflet-control-zoom-all', container);
# #                 button.href = '#';
# #                 button.title = 'Ver todas las estaciones';
# #                 button.innerHTML = '<i>⌂</i>';
# #                 L.DomEvent.disableClickPropagation(button);
# #                 L.DomEvent.on(button, 'click', function(e) {
# #                     L.DomEvent.stopPropagation(e);
# #                     L.DomEvent.preventDefault(e);
# #                     zoomATodosLosIconos();
# #                 });
# #                 return container;
# #             }
# #         });
        
# #         L.control.zoomAll = function(opts) { return new L.Control.ZoomAll(opts); };
        
# #         function initMap() {
# #             try {
# #                 map = L.map('map', {
# #                     zoomControl: true,
# #                     scrollWheelZoom: true,
# #                     dragging: true
# #                 });
                
# #                 L.tileLayer('https://{s}.basemaps.cartocdn.com/light_all/{z}/{x}/{y}{r}.png', {
# #                     attribution: '',
# #                     subdomains: 'abcd',
# #                     maxZoom: 19
# #                 }).addTo(map);
                
# #                 L.control.zoomAll().addTo(map);
                
# #                 const savedZoom = localStorage.getItem('scada_map_zoom');
# #                 const savedCenter = localStorage.getItem('scada_map_center');
# #                 const wasInitialized = localStorage.getItem('scada_map_initialized') === 'true';
# #                 let hizoFitBounds = false;
                
# #                 if (wasInitialized && savedZoom && savedCenter) {
# #                     try {
# #                         const center = JSON.parse(savedCenter);
# #                         map.setView([center.lat, center.lng], parseInt(savedZoom));
# #                         console.log('✓ Zoom restaurado:', savedZoom);
# #                     } catch(e) {
# #                         console.log('Error restaurando zoom:', e);
# #                     }
# #                 } else {
# #                     const todasCoords = [];
# #                     DATOS_INICIALES.estaciones.forEach(est => {
# #                         if (est.latitud && est.longitud) {
# #                             todasCoords.push([parseFloat(est.latitud), parseFloat(est.longitud)]);
# #                         }
# #                     });
# #                     if (todasCoords.length > 0) {
# #                         map.fitBounds(todasCoords, { padding: [40, 40] });
# #                         console.log('✓ Zoom inicial ajustado');
# #                         hizoFitBounds = true;
# #                     }
# #                 }
                
# #                 DATOS_INICIALES.estaciones.forEach(estacion => {
# #                     if (!estacion.latitud || !estacion.longitud) return;
# #                     const id = estacion.nombre || `${estacion.latitud},${estacion.longitud}`;
# #                     const lat = parseFloat(estacion.latitud);
# #                     const lng = parseFloat(estacion.longitud);
# #                     const marker = L.marker([lat, lng], { icon: crearIcono(estacion) })
# #                         .bindPopup(crearPopupContent(estacion), { maxWidth: 320 })
# #                         .bindTooltip(estacion.nombre || 'Estación', { permanent: false, direction: 'top', opacity: 0.9 })
# #                         .addTo(map);
# #                     markers.set(id, marker);
# #                 });
                
# #                 if (!hizoFitBounds && markers.size > 0 && !wasInitialized) {
# #                     const todasCoords = Array.from(markers.values()).map(m => m.getLatLng());
# #                     map.fitBounds(todasCoords, { padding: [40, 40] });
# #                     localStorage.setItem('scada_map_initialized', 'true');
# #                 }
                
# #                 actualizarEstadisticas(DATOS_INICIALES);
                
# #                 document.getElementById('loading').classList.add('hidden');
# #                 window.map = map;
                
# #             } catch(e) {
# #                 document.getElementById('loading').innerHTML = `<div style="color:#e74c3c;text-align:center;padding:20px;">❌ Error: ${e.message}</div>`;
# #                 console.error('Error:', e);
# #             }
# #         }
        
# #         if (document.readyState === 'loading') {
# #             document.addEventListener('DOMContentLoaded', initMap);
# #         } else {
# #             initMap();
# #         }
# #     </script>
# # </body>
# # </html>
# # """

# # st.components.v1.html(
# #     html_completo,
# #     width=1920,
# #     height=1080,
# #     scrolling=False
# # )

# # time.sleep(60)
# # st.rerun()

# # import streamlit as st
# # import requests
# # import json
# # import base64
# # from datetime import datetime
# # import os
# # import time

# # # ========================================
# # # FUNCIÓN PARA OBTENER EL FAVICON DESDE GITHUB
# # # ========================================
# # def obtener_favicon_github():
# #     try:
# #         GITHUB_USER = "AlarmasCiateq"
# #         REPO_NAME = "SCADA_T"
# #         BRANCH = "main"
# #         ICON_PATH = "iconos/ICONO CIATEQ 256.ico"
# #         raw_url = f"https://raw.githubusercontent.com/{GITHUB_USER}/{REPO_NAME}/{BRANCH}/{ICON_PATH}"
# #         headers = {'User-Agent': 'SCADA-Monitor'}
# #         response = requests.get(raw_url, headers=headers, timeout=10)
# #         response.raise_for_status()
# #         icon_base64 = base64.b64encode(response.content).decode('utf-8')
# #         return f"image/x-icon;base64,{icon_base64}"
# #     except Exception as e:
# #         print(f"Error cargando favicon: {e}")
# #         return None

# # # ========================================
# # # CONFIGURACIÓN DE PÁGINA
# # # ========================================
# # favicon_data = obtener_favicon_github()

# # if favicon_data:
# #     st.set_page_config(page_title="SCADA CIATEQ", page_icon="🌎", layout="wide", initial_sidebar_state="collapsed")
# #     st.markdown(f"""
# #     <link rel="icon" href="{favicon_data}" type="image/x-icon">
# #     <link rel="shortcut icon" href="{favicon_data}" type="image/x-icon">
# #     """, unsafe_allow_html=True)
# # else:
# #     st.set_page_config(page_title="SCADA CIATEQ", page_icon="🏭", layout="wide", initial_sidebar_state="collapsed")

# # st.markdown("""
# # <style>
# # [data-testid="stSidebar"] { display: none !important; }
# # [data-testid="stHeader"] { display: none !important; }
# # [data-testid="stDecoration"] { display: none !important; }
# # header { display: none !important; }
# # #MainMenu { display: none !important; }
# # footer { display: none !important; }
# # .stApp { background-color: #0e1117; padding: 0 !important; margin: 0 !important; overflow: hidden !important; }
# # .block-container { padding: 0 !important; max-width: 100% !important; margin: 0 !important; overflow: hidden !important; }
# # .main { padding: 0 !important; margin: 0 !important; overflow: hidden !important; }
# # .block-container > div { padding: 0 !important; margin: 0 !important; }
# # ::-webkit-scrollbar { display: none !important; }
# # body { overflow: hidden !important; }
# # #loading {
# #     position: fixed; top: 0; left: 0; width: 100%; height: 100%;
# #     background: #0e1117; display: flex; justify-content: center; align-items: center;
# #     color: #3498db; font-family: Arial; font-size: 18px; z-index: 9999;
# #     transition: opacity 0.1s;
# # }
# # #loading.hidden { opacity: 0; pointer-events: none; }
# # #debug-timestamp {
# #     position: fixed; bottom: 5px; right: 10px;
# #     background: rgba(0,0,0,0.7); color: #27ae60;
# #     padding: 3px 8px; font-family: monospace; font-size: 11px;
# #     border-radius: 3px; z-index: 1000;
# # }
# # /* Forzar transparencia en iconos de leaflet */
# # .leaflet-div-icon {
# #     background: transparent !important;
# #     border: none !important;
# # }
# # </style>
# # """, unsafe_allow_html=True)

# # # ========================================
# # # OBTENER TOKEN DE GITHUB
# # # ========================================
# # def obtener_token_github():
# #     try:
# #         if hasattr(st, 'secrets') and "GITHUB_TOKEN" in st.secrets:
# #             return st.secrets["GITHUB_TOKEN"]
# #     except: pass
# #     return os.getenv("GITHUB_TOKEN", None)

# # # ========================================
# # # CARGAR DATOS FRESH DE GITHUB
# # # ========================================
# # def cargar_datos_github(max_intentos=3):
# #     token = obtener_token_github()
# #     for intento in range(max_intentos):
# #         try:
# #             GITHUB_USER = "AlarmasCiateq"
# #             REPO_NAME = "SCADA_T"
# #             BRANCH = "main"
# #             FILE_PATH = "datos_estaciones.json"
# #             api_url = f"https://api.github.com/repos/{GITHUB_USER}/{REPO_NAME}/contents/{FILE_PATH}?ref={BRANCH}"
            
# #             headers = {'User-Agent': f'SCADA-Monitor-{datetime.now().timestamp()}', 'Accept': 'application/vnd.github.v3+json'}
# #             if token: headers['Authorization'] = f'token {token}'
            
# #             response = requests.get(api_url, headers=headers, timeout=10)
# #             response.raise_for_status()
            
# #             data = response.json()
# #             content_bytes = base64.b64decode(data['content'])
# #             content_str = content_bytes.decode('utf-8')
# #             datos = json.loads(content_str)
            
# #             datos['_timestamp_actualizacion'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
# #             return datos, True
            
# #         except Exception as e:
# #             print(f"Error cargando datos (intento {intento + 1}): {e}")
# #             if intento < max_intentos - 1: time.sleep(1)
# #             else: return None, False
# #     return None, False

# # # ========================================
# # # CARGAR DATOS
# # # ========================================
# # datos, exito = cargar_datos_github()

# # if not datos or not exito:
# #     st.markdown("""
# #     <div style="position:fixed;top:0;left:0;width:100%;height:100%;background:#0e1117;color:white;
# #     display:flex;justify-content:center;align-items:center;font-family:Arial;">
# #         <div style="text-align:center;padding:20px;">
# #             <h2>🛢️ SCADA Monitor</h2>
# #             <p style="color:#e74c3c; margin-top:15px;">Error: No se pudieron cargar los datos de GitHub</p>
# #         </div>
# #     </div>
# #     """, unsafe_allow_html=True)
# #     time.sleep(60)
# #     st.rerun()

# # # ========================================
# # # PREPARAR DATOS PARA HTML
# # # ========================================
# # tiempo_str = datetime.now().strftime('%H:%M:%S')
# # timestamp_debug = datos.get('_timestamp_actualizacion', tiempo_str)
# # datos_json_safe = json.dumps(datos, ensure_ascii=False)
# # datos_json_safe = (datos_json_safe.replace('\\', '\\\\').replace("'", "\\'").replace('</', '<\\/').replace('\n', '\\n').replace('\r', '\\r').replace('\t', '\\t'))

# # # ========================================
# # # HTML + JAVASCRIPT (CORREGIDO: TRANSPARENCIA TOTAL)
# # # ========================================
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
# #         body {{ font-family: Arial, sans-serif; background: #0e1117; overflow: hidden; height: 100vh; width: 100vw; }}
# #         #map {{ position: absolute; top: 0; left: 0; width: 100%; height: 100%; z-index: 1; }}
        
# #         #stats-bar {{
# #             position: fixed; top: 10px; right: 15px;
# #             background: rgba(255, 255, 255, 0.95); padding: 8px; border-radius: 6px;
# #             box-shadow: 0 2px 8px rgba(0,0,0,0.15); z-index: 1000;
# #             display: flex; gap: 12px; align-items: center; font-family: Arial, sans-serif;
# #             flex-wrap: nowrap; overflow-x: auto; max-width: 90%;
# #         }}
# #         .stat-item {{ display: flex; flex-direction: column; align-items: center; min-width: 65px; }}
# #         .stat-icon {{ width: 24px; height: 24px; margin-bottom: 2px; display: flex; align-items: center; justify-content: center; }}
# #         .stat-icon img {{ width: 100%; height: 100%; object-fit: contain; }}
# #         .stat-value {{ font-weight: bold; color: #2c3e50; font-size: 14px; text-align: center; }}
# #         .stat-label {{ font-size: 8px; color: #7f8c8d; text-align: center; white-space: nowrap; text-transform: uppercase; }}
        
# #         .custom-popup {{ font-family: Arial; padding: 12px; min-width: 280px; background: white; border-radius: 6px; }}
# #         .custom-popup h4 {{ margin: 0 0 10px 0; color: #2c3e50; font-size: 16px; font-weight: bold; }}
# #         .custom-popup hr {{ margin: 8px 0; border-color: #ecf0f1; }}
# #         .custom-popup .var-row {{ margin: 6px 0; padding: 4px 0; display: flex; justify-content: space-between; }}
# #         .custom-popup .var-label {{ color: #2c3e50; font-weight: 600; font-size: 13px; min-width: 120px; }}
# #         .custom-popup .var-value {{ color: #2c3e50; font-weight: bold; font-size: 14px; text-align: right; min-width: 80px; }}
# #         .custom-popup .timestamp {{ font-size: 11px; color: #95a5a6; text-align: center; margin-top: 8px; }}
# #         .status-online {{ color: #27ae60; font-weight: bold; }}
# #         .status-offline {{ color: #e74c3c; font-weight: bold; }}
        
# #         #loading {{ position: fixed; top: 0; left: 0; width: 100%; height: 100%; background: #0e1117; display: flex; justify-content: center; align-items: center; color: #3498db; font-family: Arial; font-size: 18px; z-index: 9999; transition: opacity 0.1s; }}
# #         #loading.hidden {{ opacity: 0; pointer-events: none; }}
# #         #debug-timestamp {{ position: fixed; bottom: 5px; right: 10px; background: rgba(0,0,0,0.7); color: #27ae60; padding: 3px 8px; font-family: monospace; font-size: 11px; border-radius: 3px; z-index: 1000; }}
        
# #         .leaflet-control-zoom-all {{ background: #fff; border: 2px solid rgba(0,0,0,0.2); border-radius: 4px; box-shadow: 0 1px 5px rgba(0,0,0,0.4); cursor: pointer; margin-top: 5px; }}
# #         .leaflet-control-zoom-all:hover {{ background: #f4f4f4; }}
# #         .leaflet-control-zoom-all i {{ display: block; width: 30px; height: 30px; line-height: 30px; text-align: center; font-weight: bold; color: #333; font-size: 20px; }}
        
# #         /* CLASE EXTRA PARA ASEGURAR TRANSPARENCIA EN EL CONTENIDO DEL ICONO */
# #         .composite-icon-container {{
# #             background: transparent !important;
# #             border: none !important;
# #             padding: 0 !important;
# #             margin: 0 !important;
# #             box-shadow: none !important;
# #         }}
# #     </style>
# # </head>
# # <body>
# #     <div id="loading">Cargando...</div>
# #     <div id="map"></div>
# #     <div id="stats-bar"></div>
# #     <div id="debug-timestamp">{timestamp_debug}</div>
    
# #     <script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"></script>
# #     <script>
# #         const DATOS_INICIALES = {datos_json_safe};
# #         let map = null;
# #         let markers = new Map();
        
# #         function limpiarUrl(url) {{
# #             if (!url) return null;
# #             return url.trim().replace(/\\s+/g, '%20');
# #         }}
        
# #         function esOffline(enLinea) {{
# #             if (enLinea === undefined || enLinea === null) return false;
# #             const valor = String(enLinea).trim().toLowerCase();
# #             return valor === '0' || valor === 'false' || valor === 'off';
# #         }}
        
# #         function obtenerNivelTanque(estacion) {{
# #             const campos = ['Porcentaje (%)', 'Porcentaje', 'Nivel (%)', 'nivel_%', 'Nivel', 'nivel'];
# #             for (let campo of campos) {{
# #                 if (estacion[campo] !== undefined) {{
# #                     let v = parseFloat(estacion[campo]);
# #                     return Math.max(0, Math.min(100, isNaN(v) ? 0 : v));
# #                 }}
# #             }}
# #             return 0;
# #         }}

# #         function getIconoUrl(tipo, enLinea) {{
# #             const tipos = DATOS_INICIALES.tipos || {{}};
# #             const config = tipos[tipo] || tipos['generico'] || {{}};
            
# #             if (!enLinea) {{
# #                 return limpiarUrl(config.icono_url_off) || limpiarUrl(config.icono_url);
# #             }}
            
# #             if (tipo === 'pozo' || tipo === 'bomba' || tipo === 'rebombeo') {{
# #                 return limpiarUrl(config.icono_url_on) || limpiarUrl(config.icono_url);
# #             }}
# #             return limpiarUrl(config.icono_url);
# #         }}

# #         function crearIconoCompuesto(estacion) {{
# #             const tipos = estacion.tipos_presentes || ['generico'];
# #             const enLinea = estacion.en_linea === 1;
# #             const n_tipos = tipos.length;
            
# #             let containerSize = 32; 
# #             let iconSize = 24;
# #             let gridTemplate = "1fr";
            
# #             if (n_tipos === 2) {{
# #                 containerSize = 50;
# #                 gridTemplate = "1fr 1fr";
# #             }} else if (n_tipos === 3) {{
# #                 containerSize = 50;
# #                 gridTemplate = "1fr 1fr";
# #             }} else if (n_tipos >= 4) {{
# #                 containerSize = 56;
# #                 gridTemplate = "1fr 1fr";
# #             }}

# #             let iconsHtml = "";
# #             tipos.forEach((tipo) => {{
# #                 const url = getIconoUrl(tipo, enLinea);
# #                 if (url) {{
# #                     // Añadimos estilo inline para asegurar que la imagen no tenga fondo
# #                     iconsHtml += `<img src="${{url}}" style="width:${{iconSize}}px;height:${{iconSize}}px;object-fit:contain;background:transparent;border:none;">`;
# #                 }} else {{
# #                     const color = (DATOS_INICIALES.tipos[tipo] || {{}}).color || '#7f8c8d';
# #                     iconsHtml += `<div style="width:${{iconSize}}px;height:${{iconSize}}px;background:${{color}};border-radius:50%;"></div>`;
# #                 }}
# #             }});

# #             const borderStyle = !enLinea ? `border:2px solid #e74c3c;box-shadow:0 0 0 2px rgba(231,76,60,0.3);` : '';
            
# #             // CORRECCIÓN DEFINITIVA: Estilo inline agresivo para transparencia
# #             const htmlFinal = `
# #                 <div class="composite-icon-container" style="
# #                     display:grid;
# #                     grid-template-columns:${{gridTemplate}};
# #                     gap:2px;
# #                     align-items:center;
# #                     justify-items:center;
# #                     width:${{containerSize}}px;
# #                     height:${{containerSize}}px;
# #                     ${{borderStyle}}
# #                     background:transparent !important;
# #                     border:none !important;
# #                     padding:0 !important;
# #                     margin:0 !important;
# #                     box-shadow:none !important;
# #                 ">
# #                     ${{iconsHtml}}
# #                 </div>
# #             `;

# #             return L.divIcon({{
# #                 html: htmlFinal,
# #                 className: 'composite-icon-container', // Clase CSS externa también
# #                 iconSize: [containerSize, containerSize],
# #                 iconAnchor: [containerSize/2, containerSize/2],
# #                 popupAnchor: [0, -(containerSize/2)]
# #             }});
# #         }}

# #         function crearIcono(estacion) {{
# #             return crearIconoCompuesto(estacion);
# #         }}
        
# #         function crearPopupContent(estacion) {{
# #             let html = `<div class="custom-popup"><h4>${{estacion.nombre || 'Estación'}}</h4><hr>`;
# #             const offline = esOffline(estacion.en_linea);
# #             const estadoLinea = offline ? '<span class="status-offline">Fuera de línea</span>' : '<span class="status-online">En línea</span>';
# #             html += `<div class="var-row"><span class="var-label">Estado:</span><span class="var-value">${{estadoLinea}}</span></div>`;
            
# #             if (estacion.tipo === 'tanque' || estacion.tipo === 'sensor' || (estacion.tipos_presentes && estacion.tipos_presentes.includes('tanque'))) {{
# #                 html += `<div class="var-row"><span class="var-label">Nivel:</span><span class="var-value">${{obtenerNivelTanque(estacion)}}%</span></div>`;
# #             }}
            
# #             const estadoArrancador = estacion["Estado del Arrancador"];
# #             if (estadoArrancador) {{
# #                 const estadoTexto = estadoArrancador === "Encendido" ? '<span style="color:#27ae60;font-weight:bold;">Encendido</span>' : '<span style="color:#e74c3c;font-weight:bold;">Apagado</span>';
# #                 html += `<div class="var-row"><span class="var-label">Arrancador:</span><span class="var-value">${{estadoTexto}}</span></div>`;
# #             }}
            
# #             for (const key in estacion) {{
# #                 if (!['nombre', 'latitud', 'longitud', 'tipo', 'en_linea', 'tipos_presentes', 'estado_global', 'Estado del Arrancador', 'Nivel', 'nivel', 'Porcentaje (%)', '_timestamp_actualizacion'].includes(key)) {{
# #                     const value = typeof estacion[key] === 'number' ? estacion[key].toLocaleString('es-ES', {{ minimumFractionDigits: 2, maximumFractionDigits: 2 }}) : estacion[key];
# #                     html += `<div class="var-row"><span class="var-label">${{key}}:</span><span class="var-value">${{value}}</span></div>`;
# #                 }}
# #             }}
# #             html += `<hr><div class="timestamp">📅 ${{new Date().toLocaleString('es-ES')}}</div></div>`;
# #             return html;
# #         }}
        
# #         function actualizarEstadisticas(datos) {{
# #             if (!datos || !datos.estaciones) return;
# #             let total = 0, online = 0, offline_count = 0;
# #             let pozos_enc = 0, pozos_apag = 0, tanques = 0, bombas_enc = 0, bombas_apag = 0, rebombeos_enc = 0, rebombeos_apag = 0, sensores = 0;
            
# #             datos.estaciones.forEach(estacion => {{
# #                 total++;
# #                 const offline = esOffline(estacion.en_linea);
# #                 const tipos = estacion.tipos_presentes || [estacion.tipo || 'generico'];
# #                 const estadoTxt = estacion["Estado del Arrancador"] || "Apagado";
# #                 const isOn = estadoTxt === "Encendido";

# #                 if (offline) offline_count++; else online++;

# #                 tipos.forEach(t => {{
# #                     if (t === 'pozo') isOn ? pozos_enc++ : pozos_apag++;
# #                     if (t === 'tanque') tanques++;
# #                     if (t === 'bomba') isOn ? bombas_enc++ : bombas_apag++;
# #                     if (t === 'rebombeo') isOn ? rebombeos_enc++ : rebombeos_apag++;
# #                     if (t === 'sensor') sensores++;
# #                 }});
# #             }});
            
# #             const tiposConfig = datos.tipos || {{}};
# #             const stats = [
# #                 {{ tipo: 'total', value: total, label: 'Total' }},
# #                 {{ tipo: 'pozo', estado: "Encendido", value: pozos_enc, label: 'Pozos Enc.' }},
# #                 {{ tipo: 'pozo', estado: "Apagado", value: pozos_apag, label: 'Pozos Apag.' }},
# #                 {{ tipo: 'tanque', value: tanques, label: 'Tanques' }},
# #                 {{ tipo: 'bomba', estado: "Encendido", value: bombas_enc, label: 'Bombas Enc.' }},
# #                 {{ tipo: 'bomba', estado: "Apagado", value: bombas_apag, label: 'Bombas Apag.' }},
# #                 {{ tipo: 'rebombeo', estado: "Encendido", value: rebombeos_enc, label: 'Rebom. Enc.' }},
# #                 {{ tipo: 'rebombeo', estado: "Apagado", value: rebombeos_apag, label: 'Rebom. Apag.' }},
# #                 {{ tipo: 'sensor', value: sensores, label: 'Sensores' }},
# #                 {{ tipo: 'offline', value: offline_count, label: 'Offline' }},
# #                 {{ tipo: 'online', value: online, label: 'Online' }},
# #                 {{ tipo: 'reloj', value: '{tiempo_str}', label: 'Actualizado' }}
# #             ];
            
# #             const statsBar = document.getElementById('stats-bar');
# #             if (!statsBar) return;
# #             statsBar.innerHTML = '';
            
# #             stats.forEach(stat => {{
# #                 const config = tiposConfig[stat.tipo] || tiposConfig['generico'] || {{}};
# #                 let iconoUrl = null;
                
# #                 if (stat.tipo === 'pozo' || stat.tipo === 'bomba' || stat.tipo === 'rebombeo') {{
# #                     iconoUrl = stat.estado === "Encendido" ? (limpiarUrl(config.icono_url_on) || limpiarUrl(config.icono_url)) : (limpiarUrl(config.icono_url_off) || limpiarUrl(config.icono_url));
# #                 }} else if (stat.tipo === 'offline') iconoUrl = 'https://raw.githubusercontent.com/AlarmasCiateq/SCADA_T/main/iconos/Offline.svg';
# #                 else if (stat.tipo === 'online') iconoUrl = 'https://raw.githubusercontent.com/AlarmasCiateq/SCADA_T/main/iconos/Online_Alarma.svg';
# #                 else if (stat.tipo === 'total') iconoUrl = 'https://raw.githubusercontent.com/AlarmasCiateq/SCADA_T/main/iconos/transmite.svg';
# #                 else if (stat.tipo === 'reloj') iconoUrl = 'https://raw.githubusercontent.com/AlarmasCiateq/SCADA_T/main/iconos/update.svg';
# #                 else iconoUrl = limpiarUrl(config.icono_url);
                
# #                 const item = document.createElement('div');
# #                 item.className = 'stat-item';
# #                 let iconHtml = iconoUrl ? `<div class="stat-icon"><img src="${{iconoUrl}}" alt="${{stat.tipo}}"></div>` : `<div class="stat-icon" style="color:${{config.color || '#7f8c8d'}};font-size:20px;">●</div>`;
                
# #                 item.innerHTML = iconHtml + '<div class="stat-value">' + stat.value + '</div>' + '<div class="stat-label">' + stat.label + '</div>';
# #                 statsBar.appendChild(item);
# #             }});
# #         }}
        
# #         function zoomATodosLosIconos() {{
# #             if (!map || markers.size === 0) return;
# #             const todasCoords = Array.from(markers.values()).map(m => m.getLatLng());
# #             map.fitBounds(todasCoords, {{ padding: [40, 40] }});
# #         }}
        
# #         L.Control.ZoomAll = L.Control.extend({{
# #             options: {{ position: 'topleft' }},
# #             onAdd: function(map) {{
# #                 const container = L.DomUtil.create('div', 'leaflet-bar leaflet-control leaflet-control-zoom-all');
# #                 const button = L.DomUtil.create('a', 'leaflet-control-zoom-all', container);
# #                 button.href = '#'; button.title = 'Ver todas las estaciones';
# #                 button.innerHTML = '<i>⌂</i>';
# #                 L.DomEvent.disableClickPropagation(button);
# #                 L.DomEvent.on(button, 'click', function(e) {{ L.DomEvent.stopPropagation(e); L.DomEvent.preventDefault(e); zoomATodosLosIconos(); }});
# #                 return container;
# #             }}
# #         }});
# #         L.control.zoomAll = function(opts) {{ return new L.Control.ZoomAll(opts); }};
        
# #         function initMap() {{
# #             try {{
# #                 map = L.map('map', {{ zoomControl: true, scrollWheelZoom: true, dragging: true }});
# #                 L.tileLayer('https://{{s}}.basemaps.cartocdn.com/light_all/{{z}}/{{x}}/{{y}}{{r}}.png', {{ attribution: '', subdomains: 'abcd', maxZoom: 19 }}).addTo(map);
# #                 L.control.zoomAll().addTo(map);
                
# #                 const savedZoom = localStorage.getItem('scada_map_zoom');
# #                 const savedCenter = localStorage.getItem('scada_map_center');
# #                 const wasInitialized = localStorage.getItem('scada_map_initialized') === 'true';
# #                 let hizoFitBounds = false;
                
# #                 if (wasInitialized && savedZoom && savedCenter) {{
# #                     try {{
# #                         const center = JSON.parse(savedCenter);
# #                         map.setView([center.lat, center.lng], parseInt(savedZoom));
# #                     }} catch(e) {{}}
# #                 }} else {{
# #                     const todasCoords = [];
# #                     DATOS_INICIALES.estaciones.forEach(est => {{
# #                         if (est.latitud && est.longitud) todasCoords.push([parseFloat(est.latitud), parseFloat(est.longitud)]);
# #                     }});
# #                     if (todasCoords.length > 0) {{ map.fitBounds(todasCoords, {{ padding: [40, 40] }}); hizoFitBounds = true; }}
# #                 }}
                
# #                 DATOS_INICIALES.estaciones.forEach(estacion => {{
# #                     if (!estacion.latitud || !estacion.longitud) return;
# #                     const id = estacion.nombre || `${{estacion.latitud}},${{estacion.longitud}}`;
# #                     const lat = parseFloat(estacion.latitud);
# #                     const lng = parseFloat(estacion.longitud);
# #                     const marker = L.marker([lat, lng], {{ icon: crearIcono(estacion) }})
# #                         .bindPopup(crearPopupContent(estacion), {{ maxWidth: 320 }})
# #                         .bindTooltip(estacion.nombre || 'Estación', {{ permanent: false, direction: 'top', opacity: 0.9 }})
# #                         .addTo(map);
# #                     markers.set(id, marker);
# #                 }});
                
# #                 if (!hizoFitBounds && markers.size > 0 && !wasInitialized) {{
# #                     const todasCoords = Array.from(markers.values()).map(m => m.getLatLng());
# #                     map.fitBounds(todasCoords, {{ padding: [40, 40] }});
# #                     localStorage.setItem('scada_map_initialized', 'true');
# #                 }}
                
# #                 actualizarEstadisticas(DATOS_INICIALES);
# #                 document.getElementById('loading').classList.add('hidden');
# #                 window.map = map;
# #             }} catch(e) {{
# #                 document.getElementById('loading').innerHTML = `<div style="color:#e74c3c;text-align:center;padding:20px;">❌ Error: ${{e.message}}</div>`;
# #                 console.error('Error:', e);
# #             }}
# #         }}
        
# #         if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', initMap);
# #         else initMap();
# #     </script>
# # </body>
# # </html>
# # """

# # st.components.v1.html(html_completo, width=1920, height=1080, scrolling=False)
# # time.sleep(60)
# # st.rerun()


# import streamlit as st
# import requests
# import json
# import base64
# from datetime import datetime
# import os
# import time

# def obtener_favicon_github():
#     try:
#         GITHUB_USER = "AlarmasCiateq"
#         REPO_NAME = "SCADA_T"
#         BRANCH = "main"
#         ICON_PATH = "iconos/ICONO CIATEQ 256.ico"
#         raw_url = f"https://raw.githubusercontent.com/{GITHUB_USER}/{REPO_NAME}/{BRANCH}/{ICON_PATH}"
#         headers = {'User-Agent': 'SCADA-Monitor'}
#         response = requests.get(raw_url, headers=headers, timeout=10)
#         response.raise_for_status()
#         icon_base64 = base64.b64encode(response.content).decode('utf-8')
#         return f"image/x-icon;base64,{icon_base64}"
#     except Exception as e:
#         print(f"Error cargando favicon: {e}")
#         return None

# favicon_data = obtener_favicon_github()

# if favicon_
#     st.set_page_config(page_title="SCADA CIATEQ", page_icon="🌎", layout="wide", initial_sidebar_state="collapsed")
#     st.markdown(f"""
#     <link rel="icon" href="{favicon_data}" type="image/x-icon">
#     <link rel="shortcut icon" href="{favicon_data}" type="image/x-icon">
#     """, unsafe_allow_html=True)
# else:
#     st.set_page_config(page_title="SCADA CIATEQ", page_icon="🏭", layout="wide", initial_sidebar_state="collapsed")

# st.markdown("""
# <style>
# [data-testid="stSidebar"] { display: none !important; }
# [data-testid="stHeader"] { display: none !important; }
# [data-testid="stDecoration"] { display: none !important; }
# header { display: none !important; }
# #MainMenu { display: none !important; }
# footer { display: none !important; }
# .stApp { background-color: #0e1117; padding: 0 !important; margin: 0 !important; overflow: hidden !important; }
# .block-container { padding: 0 !important; max-width: 100% !important; margin: 0 !important; overflow: hidden !important; }
# .main { padding: 0 !important; margin: 0 !important; overflow: hidden !important; }
# .block-container > div { padding: 0 !important; margin: 0 !important; }
# ::-webkit-scrollbar { display: none !important; }
# body { overflow: hidden !important; }
# #loading { position: fixed; top: 0; left: 0; width: 100%; height: 100%; background: #0e1117; display: flex; justify-content: center; align-items: center; color: #3498db; font-family: Arial; font-size: 18px; z-index: 9999; transition: opacity 0.1s; }
# #loading.hidden { opacity: 0; pointer-events: none; }
# #debug-timestamp { position: fixed; bottom: 5px; right: 10px; background: rgba(0,0,0,0.7); color: #27ae60; padding: 3px 8px; font-family: monospace; font-size: 11px; border-radius: 3px; z-index: 1000; }
# /* Forzar transparencia en leaflet-div-icon PERO permitir bordes condicionales */
# .leaflet-div-icon { background: transparent !important; border: none !important; }
# </style>
# """, unsafe_allow_html=True)

# def obtener_token_github():
#     try:
#         if hasattr(st, 'secrets') and "GITHUB_TOKEN" in st.secrets:
#             return st.secrets["GITHUB_TOKEN"]
#     except: pass
#     return os.getenv("GITHUB_TOKEN", None)

# def cargar_datos_github(max_intentos=3):
#     token = obtener_token_github()
#     for intento in range(max_intentos):
#         try:
#             GITHUB_USER = "AlarmasCiateq"
#             REPO_NAME = "SCADA_T"
#             BRANCH = "main"
#             FILE_PATH = "datos_estaciones.json"
#             api_url = f"https://api.github.com/repos/{GITHUB_USER}/{REPO_NAME}/contents/{FILE_PATH}?ref={BRANCH}"
#             headers = {'User-Agent': f'SCADA-Monitor-{datetime.now().timestamp()}', 'Accept': 'application/vnd.github.v3+json'}
#             if token: headers['Authorization'] = f'token {token}'
#             response = requests.get(api_url, headers=headers, timeout=10)
#             response.raise_for_status()
#             data = response.json()
#             content_bytes = base64.b64decode(data['content'])
#             content_str = content_bytes.decode('utf-8')
#             datos = json.loads(content_str)
#             datos['_timestamp_actualizacion'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
#             return datos, True
#         except Exception as e:
#             print(f"Error cargando datos (intento {intento + 1}): {e}")
#             if intento < max_intentos - 1: time.sleep(1)
#             else: return None, False
#     return None, False

# datos, exito = cargar_datos_github()

# if not datos or not exito:
#     st.markdown("""
#     <div style="position:fixed;top:0;left:0;width:100%;height:100%;background:#0e1117;color:white;display:flex;justify-content:center;align-items:center;font-family:Arial;">
#         <div style="text-align:center;padding:20px;"><h2>🛢️ SCADA Monitor</h2><p style="color:#e74c3c; margin-top:15px;">Error: No se pudieron cargar los datos de GitHub</p></div>
#     </div>
#     """, unsafe_allow_html=True)
#     time.sleep(60)
#     st.rerun()

# tiempo_str = datetime.now().strftime('%H:%M:%S')
# timestamp_debug = datos.get('_timestamp_actualizacion', tiempo_str)
# datos_json_safe = json.dumps(datos, ensure_ascii=False)
# datos_json_safe = (datos_json_safe.replace('\\', '\\\\').replace("'", "\\'").replace('</', '<\\/').replace('\n', '\\n').replace('\r', '\\r').replace('\t', '\\t'))

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
#         #stats-bar {{ position: fixed; top: 10px; right: 15px; background: rgba(255, 255, 255, 0.95); padding: 8px; border-radius: 6px; box-shadow: 0 2px 8px rgba(0,0,0,0.15); z-index: 1000; display: flex; gap: 12px; align-items: center; font-family: Arial, sans-serif; flex-wrap: nowrap; overflow-x: auto; max-width: 90%; }}
#         .stat-item {{ display: flex; flex-direction: column; align-items: center; min-width: 65px; }}
#         .stat-icon {{ width: 24px; height: 24px; margin-bottom: 2px; display: flex; align-items: center; justify-content: center; }}
#         .stat-icon img {{ width: 100%; height: 100%; object-fit: contain; }}
#         .stat-value {{ font-weight: bold; color: #2c3e50; font-size: 14px; text-align: center; }}
#         .stat-label {{ font-size: 8px; color: #7f8c8d; text-align: center; white-space: nowrap; text-transform: uppercase; }}
#         .custom-popup {{ font-family: Arial; padding: 12px; min-width: 280px; background: white; border-radius: 6px; }}
#         .custom-popup h4 {{ margin: 0 0 10px 0; color: #2c3e50; font-size: 16px; font-weight: bold; }}
#         .custom-popup hr {{ margin: 8px 0; border-color: #ecf0f1; }}
#         .custom-popup .var-row {{ margin: 6px 0; padding: 4px 0; display: flex; justify-content: space-between; }}
#         .custom-popup .var-label {{ color: #2c3e50; font-weight: 600; font-size: 13px; min-width: 120px; }}
#         .custom-popup .var-value {{ color: #2c3e50; font-weight: bold; font-size: 14px; text-align: right; min-width: 80px; }}
#         .custom-popup .timestamp {{ font-size: 11px; color: #95a5a6; text-align: center; margin-top: 8px; }}
#         .status-online {{ color: #27ae60; font-weight: bold; }}
#         .status-offline {{ color: #e74c3c; font-weight: bold; }}
#         #loading {{ position: fixed; top: 0; left: 0; width: 100%; height: 100%; background: #0e1117; display: flex; justify-content: center; align-items: center; color: #3498db; font-family: Arial; font-size: 18px; z-index: 9999; transition: opacity 0.1s; }}
#         #loading.hidden {{ opacity: 0; pointer-events: none; }}
#         #debug-timestamp {{ position: fixed; bottom: 5px; right: 10px; background: rgba(0,0,0,0.7); color: #27ae60; padding: 3px 8px; font-family: monospace; font-size: 11px; border-radius: 3px; z-index: 1000; }}
#         .leaflet-control-zoom-all {{ background: #fff; border: 2px solid rgba(0,0,0,0.2); border-radius: 4px; box-shadow: 0 1px 5px rgba(0,0,0,0.4); cursor: pointer; margin-top: 5px; }}
#         .leaflet-control-zoom-all:hover {{ background: #f4f4f4; }}
#         .leaflet-control-zoom-all i {{ display: block; width: 30px; height: 30px; line-height: 30px; text-align: center; font-weight: bold; color: #333; font-size: 20px; }}
#     </style>
# </head>
# <body>
#     <div id="loading">Cargando...</div>
#     <div id="map"></div>
#     <div id="stats-bar"></div>
#     <div id="debug-timestamp">{timestamp_debug}</div>
    
#     <script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"></script>
#     <script>
#         const DATOS_INICIALES = {datos_json_safe};
#         let map = null;
#         let markers = new Map();
        
#         function limpiarUrl(url) {{ if (!url) return null; return url.trim().replace(/\\s+/g, '%20'); }}
#         function esOffline(enLinea) {{
#             if (enLinea === undefined || enLinea === null) return false;
#             const valor = String(enLinea).trim().toLowerCase();
#             return valor === '0' || valor === 'false' || valor === 'off';
#         }}
#         function obtenerNivelTanque(variables) {{
#             // Busca en las variables del dispositivo específico
#             const campos = ['Porcentaje (%)', 'Porcentaje', 'Nivel (%)', 'nivel_%', 'Nivel', 'nivel'];
#             for (let campo of campos) {{
#                 if (variables[campo] !== undefined) {{
#                     let v = parseFloat(variables[campo]);
#                     return Math.max(0, Math.min(100, isNaN(v) ? 0 : v));
#                 }}
#             }}
#             return 0;
#         }}

#         function getIconoUrl(tipo, enLinea, variables) {{
#             const tipos = DATOS_INICIALES.tipos || {{}};
#             const config = tipos[tipo] || tipos['generico'] || {{}};
            
#             // Lógica específica para tanques: mostrar nivel si existe
#             // Pero aquí solo devolvemos la URL del icono base
            
#             if (!enLinea) {{
#                 return limpiarUrl(config.icono_url_off) || limpiarUrl(config.icono_url);
#             }}
#             if (tipo === 'pozo' || tipo === 'bomba' || tipo === 'rebombeo') {{
#                 // Podríamos chequear "Estado del Arrancador" dentro de variables si fuera necesario
#                 return limpiarUrl(config.icono_url_on) || limpiarUrl(config.icono_url);
#             }}
#             return limpiarUrl(config.icono_url);
#         }}

#         function crearIconoCompuesto(estacion) {{
#             const dispositivos = estacion.dispositivos || [];
#             const enLinea = estacion.en_linea === 1;
#             const n_devs = dispositivos.length;
            
#             if (n_devs === 0) return L.divIcon({{html:'', iconSize:[0,0]}});

#             // Calcular tamaño del grid basado en cantidad de dispositivos
#             let cols = 1;
#             if (n_devs === 2 || n_devs === 4) cols = 2;
#             if (n_devs === 3) cols = 2; // 2 arriba, 1 abajo
#             if (n_devs > 4) cols = Math.ceil(Math.sqrt(n_devs));
            
#             const iconSize = 24; // Tamaño de cada iconito
#             const gap = 2;
#             const containerSize = (cols * iconSize) + ((cols - 1) * gap) + 4; // +4 padding
            
#             let iconsHtml = "";
#             dispositivos.forEach(dev => {{
#                 const url = getIconoUrl(dev.tipo, enLinea, dev.variables);
#                 const nivel = (dev.tipo === 'tanque' || dev.tipo === 'sensor') ? obtenerNivelTanque(dev.variables) : -1;
                
#                 let extraStyle = "";
#                 if (nivel >= 0) {{
#                     // Pequeño indicador de nivel sobre el icono si es tanque
#                     // Por simplicidad, solo mostramos el icono, el nivel sale en el popup
#                 }}
                
#                 if (url) {{
#                     iconsHtml += `<img src="${{url}}" style="width:${{iconSize}}px;height:${{iconSize}}px;object-fit:contain;background:transparent;border:none;">`;
#                 }} else {{
#                     const color = (DATOS_INICIALES.tipos[dev.tipo] || {{}}).color || '#7f8c8d';
#                     iconsHtml += `<div style="width:${{iconSize}}px;height:${{iconSize}}px;background:${{color}};border-radius:50%;"></div>`;
#                 }}
#             }});

#             // CORRECCIÓN DEL BORDE ROJO: Solo aplicar si está offline
#             const borderStyle = !enLinea ? 
#                 `border: 2px solid #e74c3c; box-shadow: 0 0 0 2px rgba(231, 76, 60, 0.4); background: rgba(0,0,0,0.6);` : 
#                 `background: transparent;`;

#             const gridTemplate = `repeat(${{cols}}, 1fr)`;
            
#             const htmlFinal = `
#                 <div style="
#                     display: grid;
#                     grid-template-columns: ${{gridTemplate}};
#                     gap: ${{gap}}px;
#                     align-items: center;
#                     justify-items: center;
#                     width: ${{containerSize}}px;
#                     height: auto;
#                     padding: 2px;
#                     border-radius: 6px;
#                     ${{borderStyle}}
#                 ">
#                     ${{iconsHtml}}
#                 </div>
#             `;

#             return L.divIcon({{
#                 html: htmlFinal,
#                 className: 'composite-icon-container',
#                 iconSize: [containerSize, containerSize],
#                 iconAnchor: [containerSize/2, containerSize/2],
#                 popupAnchor: [0, -(containerSize/2)]
#             }});
#         }}

#         function crearIcono(estacion) {{ return crearIconoCompuesto(estacion); }}
        
#         function crearPopupContent(estacion) {{
#             let html = `<div class="custom-popup"><h4>${{estacion.nombre || 'Estación'}}</h4><hr>`;
#             const offline = esOffline(estacion.en_linea);
#             const estadoLinea = offline ? '<span class="status-offline">Fuera de línea</span>' : '<span class="status-online">En línea</span>';
#             html += `<div class="var-row"><span class="var-label">Estado Global:</span><span class="var-value">${{estadoLinea}}</span></div><hr>`;
            
#             // Iterar sobre CADA dispositivo para mostrar sus variables específicas
#             if (estacion.dispositivos && estacion.dispositivos.length > 0) {{
#                 estacion.dispositivos.forEach((dev, idx) => {{
#                     html += `<div style="margin-bottom:10px; border-bottom:1px dashed #ccc; padding-bottom:5px;">
#                         <strong style="color:#2c3e50; text-transform:capitalize;">${{dev.tipo_detalle || dev.tipo}}</strong><br>`;
                    
#                     // Mostrar nivel si es tanque
#                     if (dev.tipo === 'tanque' || dev.tipo === 'sensor') {{
#                         const nivel = obtenerNivelTanque(dev.variables);
#                         html += `<div class="var-row"><span class="var-label">Nivel:</span><span class="var-value">${{nivel}}%</span></div>`;
#                     }}
                    
#                     // Mostrar Estado del Arrancador si existe
#                     if (dev.variables["Estado del Arrancador"]) {{
#                         const val = dev.variables["Estado del Arrancador"];
#                         const color = val === "Encendido" ? "#27ae60" : "#e74c3c";
#                         html += `<div class="var-row"><span class="var-label">Arrancador:</span><span style="color:${{color}};font-weight:bold;">${{val}}</span></div>`;
#                     }}

#                     // Otras variables
#                     for (const key in dev.variables) {{
#                         if (!['Estado del Arrancador', 'Nivel', 'nivel', 'Porcentaje (%)'].includes(key)) {{
#                             const value = dev.variables[key];
#                             html += `<div class="var-row"><span class="var-label">${{key}}:</span><span class="var-value">${{value}}</span></div>`;
#                         }}
#                     }}
#                     html += `</div>`;
#                 }});
#             }} else {{
#                 // Fallback por si no viene la estructura nueva
#                 for (const key in estacion) {{
#                     if (!['nombre', 'latitud', 'longitud', 'en_linea', 'dispositivos', 'estado_global', '_timestamp_actualizacion'].includes(key)) {{
#                          const value = typeof estacion[key] === 'number' ? estacion[key].toLocaleString('es-ES', {{ minimumFractionDigits: 2, maximumFractionDigits: 2 }}) : estacion[key];
#                          html += `<div class="var-row"><span class="var-label">${{key}}:</span><span class="var-value">${{value}}</span></div>`;
#                     }}
#                 }}
#             }}
            
#             html += `<hr><div class="timestamp">📅 ${new Date().toLocaleString('es-ES')}</div></div>`;
#             return html;
#         }}
        
#         function actualizarEstadisticas(datos) {{
#             // ... (Lógica de estadísticas igual que antes, omitida por brevedad pero funcional) ...
#             // Nota: Deberías adaptar esto para contar dispositivos individuales si lo deseas
#             const statsBar = document.getElementById('stats-bar');
#             if(!statsBar) return;
#             statsBar.innerHTML = '<div style="font-size:12px;color:#7f8c8d;">Estadísticas en actualización...</div>';
#         }}
        
#         function zoomATodosLosIconos() {{
#             if (!map || markers.size === 0) return;
#             const todasCoords = Array.from(markers.values()).map(m => m.getLatLng());
#             map.fitBounds(todasCoords, {{ padding: [40, 40] }});
#         }}
        
#         L.Control.ZoomAll = L.Control.extend({{
#             options: {{ position: 'topleft' }},
#             onAdd: function(map) {{
#                 const container = L.DomUtil.create('div', 'leaflet-bar leaflet-control leaflet-control-zoom-all');
#                 const button = L.DomUtil.create('a', 'leaflet-control-zoom-all', container);
#                 button.href = '#'; button.title = 'Ver todas las estaciones';
#                 button.innerHTML = '<i>⌂</i>';
#                 L.DomEvent.disableClickPropagation(button);
#                 L.DomEvent.on(button, 'click', function(e) {{ L.DomEvent.stopPropagation(e); L.DomEvent.preventDefault(e); zoomATodosLosIconos(); }});
#                 return container;
#             }}
#         }});
#         L.control.zoomAll = function(opts) {{ return new L.Control.ZoomAll(opts); }};
        
#         function initMap() {{
#             try {{
#                 map = L.map('map', {{ zoomControl: true, scrollWheelZoom: true, dragging: true }});
#                 L.tileLayer('https://{{s}}.basemaps.cartocdn.com/light_all/{{z}}/{{x}}/{{y}}{{r}}.png', {{ attribution: '', subdomains: 'abcd', maxZoom: 19 }}).addTo(map);
#                 L.control.zoomAll().addTo(map);
                
#                 const savedZoom = localStorage.getItem('scada_map_zoom');
#                 const savedCenter = localStorage.getItem('scada_map_center');
#                 const wasInitialized = localStorage.getItem('scada_map_initialized') === 'true';
#                 let hizoFitBounds = false;
                
#                 if (wasInitialized && savedZoom && savedCenter) {{
#                     try {{ const center = JSON.parse(savedCenter); map.setView([center.lat, center.lng], parseInt(savedZoom)); }} catch(e) {{}}
#                 }} else {{
#                     const todasCoords = [];
#                     DATOS_INICIALES.estaciones.forEach(est => {{
#                         if (est.latitud && est.longitud) todasCoords.push([parseFloat(est.latitud), parseFloat(est.longitud)]);
#                     }});
#                     if (todasCoords.length > 0) {{ map.fitBounds(todasCoords, {{ padding: [40, 40] }}); hizoFitBounds = true; }}
#                 }}
                
#                 DATOS_INICIALES.estaciones.forEach(estacion => {{
#                     if (!estacion.latitud || !estacion.longitud) return;
#                     const id = estacion.nombre || `${{estacion.latitud}},${{estacion.longitud}}`;
#                     const lat = parseFloat(estacion.latitud);
#                     const lng = parseFloat(estacion.longitud);
#                     const marker = L.marker([lat, lng], {{ icon: crearIcono(estacion) }})
#                         .bindPopup(crearPopupContent(estacion), {{ maxWidth: 350 }})
#                         .bindTooltip(estacion.nombre || 'Estación', {{ permanent: false, direction: 'top', opacity: 0.9 }})
#                         .addTo(map);
#                     markers.set(id, marker);
#                 }});
                
#                 if (!hizoFitBounds && markers.size > 0 && !wasInitialized) {{
#                     const todasCoords = Array.from(markers.values()).map(m => m.getLatLng());
#                     map.fitBounds(todasCoords, {{ padding: [40, 40] }});
#                     localStorage.setItem('scada_map_initialized', 'true');
#                 }}
                
#                 actualizarEstadisticas(DATOS_INICIALES);
#                 document.getElementById('loading').classList.add('hidden');
#                 window.map = map;
#             }} catch(e) {{
#                 document.getElementById('loading').innerHTML = `<div style="color:#e74c3c;text-align:center;padding:20px;">❌ Error: ${{e.message}}</div>`;
#                 console.error('Error:', e);
#             }}
#         }}
        
#         if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', initMap);
#         else initMap();
#     </script>
# </body>
# </html>
# """

# st.components.v1.html(html_completo, width=1920, height=1080, scrolling=False)
# time.sleep(60)
# st.rerun()


import streamlit as st
import requests
import json
import base64
from datetime import datetime
import os
import time

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
ICONO_PATH = os.path.join(SCRIPT_DIR, "ICONO CIATEQ 256.ico")

GITHUB_USER = "AlarmasCiateq"
REPO_NAME = "SCADA_T"
BRANCH = "main"


# ========================================
# OBTENER TOKEN DE GITHUB
# ========================================
def obtener_token_github():
    try:
        if hasattr(st, 'secrets') and "GITHUB_TOKEN" in st.secrets:
            return st.secrets["GITHUB_TOKEN"]
    except:
        pass
    return os.getenv("GITHUB_TOKEN", None)


# ========================================
# FUNCION PARA OBTENER EL FAVICON DESDE GITHUB
# ========================================
@st.cache_resource(show_spinner=False)
def obtener_favicon_github():

    # Si ya existe localmente → NO descargar otra vez
    if os.path.exists(ICONO_PATH):
        return ICONO_PATH

    try:
        token = obtener_token_github()
        ICON_PATH_REPO = "iconos/ICONO CIATEQ 256.ico"

        api_url = f"https://api.github.com/repos/{GITHUB_USER}/{REPO_NAME}/contents/{ICON_PATH_REPO}?ref={BRANCH}"

        headers = {
            "User-Agent": "SCADA-CIATEQ",
            "Accept": "application/vnd.github.v3.raw"
        }

        if token:
            headers["Authorization"] = f"token {token}"

        response = requests.get(api_url, headers=headers, timeout=10)
        response.raise_for_status()

        with open(ICONO_PATH, "wb") as f:
            f.write(response.content)

        return ICONO_PATH

    except Exception as e:
        print(f"Error cargando favicon: {e}")
        return ICONO_PATH


# ========================================
# CONFIGURACION DE PAGINA (UNA SOLA VEZ)
# ========================================
favicon_data = obtener_favicon_github()

st.set_page_config(
    page_title="SCADA CIATEQ",
    page_icon=favicon_data,
    layout="wide",
    initial_sidebar_state="collapsed"
)

st.markdown(f"""
<link rel="icon" href="{favicon_data}" type="image/x-icon">
<link rel="shortcut icon" href="{favicon_data}" type="image/x-icon">
""", unsafe_allow_html=True)



# CSS AGRESIVO
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
#loading {
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background: #0e1117;
    display: flex;
    justify-content: center;
    align-items: center;
    color: #3498db;
    font-family: Arial;
    font-size: 18px;
    z-index: 9999;
    transition: opacity 0.1s;
}
#loading.hidden {
    opacity: 0;
    pointer-events: none;
}
#debug-timestamp {
    position: fixed;
    bottom: 5px;
    right: 10px;
    background: rgba(0,0,0,0.7);
    color: #27ae60;
    padding: 3px 8px;
    font-family: monospace;
    font-size: 11px;
    border-radius: 3px;
    z-index: 1000;
}
</style>
""", unsafe_allow_html=True)

# ========================================
# CARGAR DATOS FRESH DE GITHUB
# ========================================
def cargar_datos_github(max_intentos=3):
    token = obtener_token_github()
    for intento in range(max_intentos):
        try:
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
            datos = json.loads(content_str)
            datos['_timestamp_actualizacion'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            return datos, True
        except Exception as e:
            print(f"Error cargando datos (intento {intento + 1}): {e}")
            if intento < max_intentos - 1:
                time.sleep(1)
                continue
            return None, False
    return None, False

# ========================================
# CARGAR DATOS
# ========================================
datos, exito = cargar_datos_github()
if not datos or not exito:
    st.markdown("""
    <div style="position:fixed;top:0;left:0;width:100%;height:100%;background:#0e1117;color:white;
    display:flex;justify-content:center;align-items:center;font-family:Arial;">
        <div style="text-align:center;padding:20px;">
            <h2>💧 SCADA Monitor</h2>
            <p style="color:#e74c3c; margin-top:15px;">Error: No se pudieron cargar los datos de GitHub</p>
            <p style="font-size:14px; margin-top:10px; color:#95a5a6;">Verifique conexion a internet</p>
        </div>
    </div>
    """, unsafe_allow_html=True)
    time.sleep(60)
    st.rerun()

# ========================================
# PREPARAR DATOS PARA HTML
# ========================================
tiempo_str = datetime.now().strftime('%H:%M:%S')
timestamp_debug = datos.get('_timestamp_actualizacion', tiempo_str)
datos_json_safe = json.dumps(datos, ensure_ascii=False)
datos_json_safe = (datos_json_safe.replace('\\', '\\\\')
    .replace("'", "\\'")
    .replace('</', '<\\/').replace('\n', '\\n')
    .replace('\r', '\\r').replace('\t', '\\t'))

# ========================================
# HTML + JAVASCRIPT
# ========================================
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
        body { font-family: Arial, sans-serif; background: #0e1117; overflow: hidden; height: 100vh; width: 100vw; }
        #map { position: absolute; top: 0; left: 0; width: 100%; height: 100%; z-index: 1; }
        #stats-bar {
            position: fixed;
            top: 10px;
            right: 15px;
            background: rgba(255, 255, 255, 0.95);
            padding: 8px;
            border-radius: 6px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.15);
            z-index: 1000;
            display: flex;
            gap: 12px;
            align-items: center;
            font-family: Arial, sans-serif;
            flex-wrap: nowrap;
            overflow-x: auto;
            max-width: 90%;
        }
        .stat-item {
            display: flex;
            flex-direction: column;
            align-items: center;
            min-width: 65px;
        }
        .stat-icon {
            width: 24px;
            height: 24px;
            margin-bottom: 2px;
            display: flex;
            align-items: center;
            justify-content: center;
        }
        .stat-icon img {
            width: 100%;
            height: 100%;
            object-fit: contain;
        }
        .stat-value {
            font-weight: bold;
            color: #2c3e50;
            font-size: 14px;
            text-align: center;
        }
        .stat-label {
            font-size: 8px;
            color: #7f8c8d;
            text-align: center;
            white-space: nowrap;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }
        .custom-popup {
            font-family: Arial;
            padding: 12px;
            min-width: 320px;
            background: white;
            border-radius: 6px;
        }
        .custom-popup h4 {
            margin: 0 0 10px 0;
            color: #2c3e50;
            font-size: 16px;
            font-weight: bold;
        }
        .custom-popup hr {
            margin: 8px 0;
            border-color: #ecf0f1;
        }
        .custom-popup .var-row {
            margin: 6px 0;
            padding: 4px 0;
            display: flex;
            justify-content: space-between;
        }
        .custom-popup .var-label {
            color: #2c3e50;
            font-weight: 600;
            font-size: 13px;
            min-width: 140px;
        }
        .custom-popup .var-value {
            color: #2c3e50;
            font-weight: bold;
            font-size: 14px;
            text-align: right;
            min-width: 80px;
        }
        .custom-popup .timestamp {
            font-size: 11px;
            color: #95a5a6;
            text-align: center;
            margin-top: 8px;
        }
        .status-online { color: #27ae60; font-weight: bold; }
        .status-offline { color: #e74c3c; font-weight: bold; }
        #loading {
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: #0e1117;
            display: flex;
            justify-content: center;
            align-items: center;
            color: #3498db;
            font-family: Arial;
            font-size: 18px;
            z-index: 9999;
            transition: opacity 0.1s;
        }
        #loading.hidden {
            opacity: 0;
            pointer-events: none;
        }
        #debug-timestamp {
            position: fixed;
            bottom: 5px;
            right: 10px;
            background: rgba(0,0,0,0.7);
            color: #27ae60;
            padding: 3px 8px;
            font-family: monospace;
            font-size: 11px;
            border-radius: 3px;
            z-index: 1000;
        }
        .leaflet-control-zoom-all {
            background: #fff;
            border: 2px solid rgba(0,0,0,0.2);
            border-radius: 4px;
            box-shadow: 0 1px 5px rgba(0,0,0,0.4);
            cursor: pointer;
            margin-top: 5px;
            transition: all 0.2s;
        }
        .leaflet-control-zoom-all:hover {
            background: #f4f4f4;
            box-shadow: 0 1px 7px rgba(0,0,0,0.45);
        }
        .leaflet-control-zoom-all:active {
            background: #e8e8e8;
        }
        .leaflet-control-zoom-all i {
            display: block;
            width: 30px;
            height: 30px;
            line-height: 30px;
            text-align: center;
            font-weight: bold;
            color: #333;
            font-size: 20px;
        }
        .leaflet-control-zoom-all:hover i {
            color: #2c3e50;
        }
        .leaflet-div-icon {
            background: transparent !important;
            border: none !important;
        }
        /* CAMBIO: Etiqueta de nombre - SOLO afecta el letrero, NO el icono */
        .station-label {
            background: rgba(255, 255, 255, 0.3);
            border: 1px solid rgba(0, 0, 0, 0.1);
            border-radius: 5px;
            padding: 0px 0px;
            font-size: 6px;
            font-weight: bold;
            color: #666666;
            white-space: wrap;
            /* overflow: hidden; */
            text-overflow: ellipsis;
            text-align: center;
            max-width: 90px;
            margin-bottom: 2px;
        }
    </style>
</head>
<body>
    <div id="loading">Cargando...</div>
    <div id="map"></div>
    <div id="stats-bar"></div>
    <div id="debug-timestamp">""" + timestamp_debug + """</div>
    <script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"></script>
    <script>
        (function() {
            'use strict';
            window.addEventListener('beforeunload', function() {
                if (window.map) {
                    try {
                        const zoom = window.map.getZoom();
                        const center = window.map.getCenter();
                        localStorage.setItem('scada_map_zoom', zoom.toString());
                        localStorage.setItem('scada_map_center', JSON.stringify({lat: center.lat, lng: center.lng}));
                        localStorage.setItem('scada_map_initialized', 'true');
                    } catch(e) {}
                }
            });
            const DATOS_INICIALES = """ + datos_json_safe + """;
            let map = null;
            let markers = new Map();
            function limpiarUrl(url) {
                if (!url) return null;
                return url.trim().replace(/\\s+/g, '%20');
            }
            function esOffline(enLinea) {
                if (enLinea === undefined || enLinea === null) return false;
                const valor = String(enLinea).trim().toLowerCase();
                return valor === '0' || valor === 'false' || valor === 'off' || valor === 'no';
            }
            function tieneAlarma(estacion) {
                try {
                    if (estacion["Alarma"] === undefined || estacion["Alarma"] === null) {
                        return false;
                    }
                    const valor = String(estacion["Alarma"]).trim().toLowerCase();
                    return valor === 'on' || valor === 'alarma' || valor === '1' || valor === 'true' || valor === 'si' || valor === 'yes';
                } catch(e) {
                    return false;
                }
            }
            function obtenerNiveles(estacion) {
                let nivelSuperficial = null;
                let nivelElevado = null;
                if (estacion["Nivel Tanque Superficial"] !== undefined) {
                    let v = parseFloat(estacion["Nivel Tanque Superficial"]);
                    if (!isNaN(v)) nivelSuperficial = Math.max(0, Math.min(100, v));
                }
                if (estacion["Nivel Tanque Elevado"] !== undefined) {
                    let v = parseFloat(estacion["Nivel Tanque Elevado"]);
                    if (!isNaN(v)) nivelElevado = Math.max(0, Math.min(100, v));
                }
                if (nivelSuperficial === null && nivelElevado === null) {
                    const camposGenericos = ['Porcentaje (%)', 'Porcentaje', 'Nivel (%)', 'nivel_%', 'Nivel', 'nivel'];
                    for (let campo of camposGenericos) {
                        if (estacion[campo] !== undefined && estacion[campo] !== null) {
                            let v = parseFloat(estacion[campo]);
                            if (!isNaN(v)) {
                                if (nivelElevado === null) nivelElevado = Math.max(0, Math.min(100, v));
                                else if (nivelSuperficial === null) nivelSuperficial = Math.max(0, Math.min(100, v));
                            }
                        }
                    }
                }
                return {
                    superficial: nivelSuperficial,
                    elevado: nivelElevado,
                    principal: (nivelElevado !== null) ? nivelElevado : (nivelSuperficial !== null ? nivelSuperficial : 0)
                };
            }
            function obtenerEstadoArrancador(estacion, tipo) {
                if (tipo === 'rebombeo') {
                    if (estacion["Estado del Arrancador Rebombeo 1"] !== undefined) {
                        return estacion["Estado del Arrancador Rebombeo 1"];
                    }
                    if (estacion["Estado del Arrancador Rebombeo 2"] !== undefined) {
                        return estacion["Estado del Arrancador Rebombeo 2"];
                    }
                }
                return estacion["Estado del Arrancador"] || "Apagado";
            }
            // ========================================
            // ESTILOS BASE - ICONOS 32x32 ORIGINALES
            // ========================================
            function getEstilosBase(alarma, offline) {
                let styles = 'position: relative; width: 32px; height: 32px; display: flex; align-items: center; justify-content: center; box-sizing: border-box;';
                styles += ' background: transparent; ';
                if (alarma) {
                    styles += ' background-color: rgba(255, 193, 7, 0.8); ';
                }
                if (offline) {
                    styles += ' border: 3px solid #e74c3c; ';
                } else {
                    styles += ' border: none; ';
                }
                return styles;
            }
            // ========================================
            // FUNCIONES PARA CREAR SUB-ICONOS (28x28)
            // ========================================
            function crearSubIconoTanque(estacion, tamaño = 28) {
                const niveles = obtenerNiveles(estacion);
                const nivel = niveles.principal;
                const tipos = DATOS_INICIALES.tipos || {};
                const config = tipos['tanque'] || tipos['generico'] || {};
                const iconoUrl = limpiarUrl(config.icono_url) || null;
                const alturaLlenado = Math.round((nivel / 100) * (tamaño - 4));
                if (iconoUrl) {
                    return `<div style="position:relative;width:${tamaño}px;height:${tamaño}px">
                        <div style="position:absolute;bottom:0;left:0;width:${tamaño}px;height:${alturaLlenado}px;background:rgba(52,152,219,0.85);"></div>
                        <img src="${iconoUrl}" width="${tamaño}" height="${tamaño}" style="position:absolute;top:0;left:0;z-index:1;">
                        <div style="position:absolute;bottom:2px;width:${tamaño}px;text-align:center;font-size:9px;color:blue;font-weight:bold;text-shadow:0 1px 2px rgba(0,0,0,0.8)">${Math.round(nivel)}%</div>
                    </div>`;
                } else {
                    const yInicio = (tamaño - 4) - alturaLlenado;
                    const svg = `<svg xmlns="http://www.w3.org/2000/svg" width="${tamaño}" height="${tamaño}" viewBox="0 0 ${tamaño} ${tamaño}">
                        <rect x="0" y="${yInicio}" width="${tamaño}" height="${alturaLlenado}" fill="rgba(52,152,219,0.85)"/>
                        <rect x="2" y="2" width="${tamaño-4}" height="${tamaño-4}" fill="#2c3e50"/>
                        <text x="${tamaño/2}" y="${tamaño/2 + 3}" font-family="Arial" font-size="8" fill="white" text-anchor="middle" font-weight="bold">${Math.round(nivel)}%</text>
                    </svg>`;
                    return `<div style="position:relative;width:${tamaño}px;height:${tamaño}px">${svg}</div>`;
                }
            }
            function crearSubIconoRio(estacion, tamaño = 28) {
                const niveles = obtenerNiveles(estacion);
                const nivel = niveles.principal;
                const tipos = DATOS_INICIALES.tipos || {};
                const config = tipos['sensor'] || tipos['generico'] || {};
                const iconoUrl = limpiarUrl(config.icono_url) || null;
                const alturaLlenado = Math.round((nivel / 100) * (tamaño - 4));
                if (iconoUrl) {
                    return `<div style="position:relative;width:${tamaño}px;height:${tamaño}px">
                        <div style="position:absolute;bottom:0;left:0;width:${tamaño}px;height:${alturaLlenado}px;background:rgba(52,152,219,0.85);"></div>
                        <img src="${iconoUrl}" width="${tamaño}" height="${tamaño}" style="position:absolute;top:0;left:0;z-index:1;">
                        <div style="position:absolute;bottom:2px;width:${tamaño}px;text-align:center;font-size:9px;color:blue;font-weight:bold;text-shadow:0 1px 2px rgba(0,0,0,0.8)">${Math.round(nivel)}%</div>
                    </div>`;
                } else {
                    const yInicio = (tamaño - 4) - alturaLlenado;
                    const svg = `<svg xmlns="http://www.w3.org/2000/svg" width="${tamaño}" height="${tamaño}" viewBox="0 0 ${tamaño} ${tamaño}">
                        <rect x="0" y="${yInicio}" width="${tamaño}" height="${alturaLlenado}" fill="rgba(52,152,219,0.85)"/>
                        <path d="M2 ${tamaño/2} Q${tamaño/2} ${tamaño/2 - 4} ${tamaño-2} ${tamaño/2} L${tamaño-2} ${tamaño-2} Q${tamaño/2} ${tamaño-4} 2 ${tamaño-2} Z" fill="#2c3e50"/>
                        <text x="${tamaño/2}" y="${tamaño/2 + 3}" font-family="Arial" font-size="8" fill="blue" text-anchor="middle" font-weight="bold">${Math.round(nivel)}%</text>
                    </svg>`;
                    return `<div style="position:relative;width:${tamaño}px;height:${tamaño}px">${svg}</div>`;
                }
            }
            function crearSubIconoBomba(estacion, tipo, tamaño = 28) {
                const offline = esOffline(estacion.en_linea);
                const alarma = tieneAlarma(estacion);
                const tipos = DATOS_INICIALES.tipos || {};
                const config = tipos[tipo] || tipos['generico'] || {};
                const estado = obtenerEstadoArrancador(estacion, tipo);
                let iconoUrl = null;
                if (estado === "Encendido") {
                    iconoUrl = limpiarUrl(config.icono_url_on) || limpiarUrl(config.icono_url) || null;
                } else {
                    iconoUrl = limpiarUrl(config.icono_url_off) || limpiarUrl(config.icono_url) || null;
                }
                const estilos = getEstilosBase(alarma, offline);
                if (iconoUrl) {
                    return `<div style="${estilos}">
                        <img src="${iconoUrl}" width="${tamaño}" height="${tamaño}" style="display:block;">
                    </div>`;
                } else {
                    const color = estado === "Encendido" ? '#27ae60' : '#e74c3c';
                    return `<div style="${estilos}">
                        <div style="width:${tamaño-6}px;height:${tamaño-6}px;border-radius:50%;background:${color};"></div>
                    </div>`;
                }
            }
            function crearSubIconoGenerico(estacion, tamaño = 28) {
                const offline = esOffline(estacion.en_linea);
                const alarma = tieneAlarma(estacion);
                const tipo = estacion.tipo || 'generico';
                const tipos = DATOS_INICIALES.tipos || {};
                const config = tipos[tipo] || tipos['generico'] || {};
                const iconoUrl = limpiarUrl(config.icono_url) || null;
                const color = config.color || '#7f8c8d';
                const estilos = getEstilosBase(alarma, offline);
                if (iconoUrl) {
                    return `<div style="${estilos}">
                        <img src="${iconoUrl}" width="${tamaño}" height="${tamaño}" style="display:block;">
                    </div>`;
                } else {
                    return `<div style="${estilos}">
                        <div style="width:${tamaño-6}px;height:${tamaño-6}px;border-radius:50%;background:${color};"></div>
                    </div>`;
                }
            }
            function crearSubIcono(estacion, tamaño = 28) {
                const tipo = estacion.tipo || 'generico';
                if (tipo === 'tanque') {
                    return crearSubIconoTanque(estacion, tamaño);
                } else if (tipo === 'sensor') {
                    return crearSubIconoRio(estacion, tamaño);
                } else if (tipo === 'pozo' || tipo === 'bomba' || tipo === 'rebombeo') {
                    return crearSubIconoBomba(estacion, tipo, tamaño);
                } else {
                    return crearSubIconoGenerico(estacion, tamaño);
                }
            }
            // ========================================
            // ICONO COMPUESTO - CON NOMBRE
            // ========================================
            function crearIconoCompuesto(estaciones) {
                if (!estaciones || estaciones.length === 0) return null;
                const count = estaciones.length;
                const cols = count === 1 ? 1 : 2;
                const rows = Math.ceil(count / 2);
                const iconSize = 28;
                const gap = 2;
                const totalWidth = (cols * iconSize) + ((cols - 1) * gap);
                const totalHeight = (rows * iconSize) + ((rows - 1) * gap);
                const nombre = estaciones[0].nombre || 'Estación';
                
                let subIconosHtml = '';
                let posicion = 0;
                for (let row = 0; row < rows; row++) {
                    for (let col = 0; col < cols; col++) {
                        if (posicion >= count) break;
                        const est = estaciones[posicion];
                        const left = col * (iconSize + gap);
                        const top = row * (iconSize + gap);
                        subIconosHtml += `<div style="position:absolute;left:${left}px;top:${top}px;">
                            ${crearSubIcono(est, iconSize)}
                        </div>`;
                        posicion++;
                    }
                }
                
                const htmlCompleto = `<div style="display:flex;flex-direction:column;align-items:center;">
                    <div class="station-label" title="${nombre}">${nombre}</div>
                    <div style="position: relative; width: ${totalWidth}px; height: ${totalHeight}px; background: transparent;">
                        ${subIconosHtml}
                    </div>
                </div>`;
                
                return L.divIcon({
                    html: htmlCompleto,
                    iconSize: [Math.max(totalWidth, 60), totalHeight + 18],
                    iconAnchor: [Math.max(totalWidth, 60) / 2, totalHeight + 18],
                    popupAnchor: [0, -(totalHeight + 18)],
                    className: 'icono-compuesto'
                });
            }
            
            // ========================================
            // ICONO SIMPLE - 32x32 + NOMBRE
            // ========================================
            function crearIconoSimple(estacion) {
                const tipo = estacion.tipo || 'generico';
                const offline = esOffline(estacion.en_linea);
                const alarma = tieneAlarma(estacion);
                const niveles = obtenerNiveles(estacion);
                const tipos = DATOS_INICIALES.tipos || {};
                const config = tipos[tipo] || tipos['generico'] || {};
                const tamaño = 32;
                const estilos = getEstilosBase(alarma, offline);
                const nombre = estacion.nombre || 'Estación';
                
                // TANQUE
                if (tipo === 'tanque') {
                    const iconoUrl = limpiarUrl(config.icono_url) || null;
                    const alturaLlenado = Math.round((niveles.principal / 100) * tamaño);
                    let iconoHtml = '';
                    if (iconoUrl) {
                        iconoHtml = `<div style="position:relative; width:${tamaño}px; height:${tamaño}px; ${estilos}">
                            <div style="position:absolute; bottom:0; left:0; width:100%; height:${alturaLlenado}px; background:rgba(52,152,219,0.85);"></div>
                            <img src="${iconoUrl}" width="${tamaño}" height="${tamaño}" style="position:relative; z-index:1;">
                            <div style="position:absolute; bottom:4px; width:100%; text-align:center; font-size:11px; color:blue; font-weight:bold; text-shadow:0 1px 2px rgba(0,0,0,0.8); z-index:2;">${Math.round(niveles.principal)}%</div>
                        </div>`;
                    } else {
                        const yInicio = tamaño - alturaLlenado;
                        const svg = `<svg xmlns="http://www.w3.org/2000/svg" width="${tamaño}" height="${tamaño}" viewBox="0 0 ${tamaño} ${tamaño}">
                            <rect x="0" y="${yInicio}" width="${tamaño}" height="${alturaLlenado}" fill="rgba(52,152,219,0.85)"/>
                            <rect x="2" y="2" width="${tamaño-4}" height="${tamaño-4}" fill="#2c3e50"/>
                            <text x="${tamaño/2}" y="${tamaño/2 + 3}" font-family="Arial" font-size="10" fill="white" text-anchor="middle" font-weight="bold">${Math.round(niveles.principal)}%</text>
                        </svg>`;
                        iconoHtml = `<div style="width:${tamaño}px; height:${tamaño}px; ${estilos}">${svg}</div>`;
                    }
                    return L.divIcon({
                        html: `<div style="display:flex;flex-direction:column;align-items:center;">
                            <div class="station-label" title="${nombre}">${nombre}</div>
                            ${iconoHtml}
                        </div>`,
                        iconSize: [Math.max(tamaño, 60), tamaño + 18],
                        iconAnchor: [Math.max(tamaño, 60) / 2, tamaño + 18],
                        popupAnchor: [0, -(tamaño + 18)],
                        className: 'icono-simple'
                    });
                }
                
                // SENSOR
                if (tipo === 'sensor') {
                    const iconoUrl = limpiarUrl(config.icono_url) || null;
                    const alturaLlenado = Math.round((niveles.principal / 100) * tamaño);
                    let iconoHtml = '';
                    if (iconoUrl) {
                        iconoHtml = `<div style="position:relative; width:${tamaño}px; height:${tamaño}px; ${estilos}">
                            <div style="position:absolute; bottom:0; left:0; width:100%; height:${alturaLlenado}px; background:rgba(52,152,219,0.85);"></div>
                            <img src="${iconoUrl}" width="${tamaño}" height="${tamaño}" style="position:relative; z-index:1;">
                            <div style="position:absolute; bottom:4px; width:100%; text-align:center; font-size:11px; color:blue; font-weight:bold; text-shadow:0 1px 2px rgba(0,0,0,0.8); z-index:2;">${Math.round(niveles.principal)}%</div>
                        </div>`;
                    } else {
                        const yInicio = tamaño - alturaLlenado;
                        const svg = `<svg xmlns="http://www.w3.org/2000/svg" width="${tamaño}" height="${tamaño}" viewBox="0 0 ${tamaño} ${tamaño}">
                            <rect x="0" y="${yInicio}" width="${tamaño}" height="${alturaLlenado}" fill="rgba(52,152,219,0.85)"/>
                            <path d="M2 ${tamaño/2} Q${tamaño/2} ${tamaño/2 - 4} ${tamaño-2} ${tamaño/2} L${tamaño-2} ${tamaño-2} Q${tamaño/2} ${tamaño-4} 2 ${tamaño-2} Z" fill="#2c3e50"/>
                            <text x="${tamaño/2}" y="${tamaño/2 + 3}" font-family="Arial" font-size="10" fill="blue" text-anchor="middle" font-weight="bold">${Math.round(niveles.principal)}%</text>
                        </svg>`;
                        iconoHtml = `<div style="width:${tamaño}px; height:${tamaño}px; ${estilos}">${svg}</div>`;
                    }
                    return L.divIcon({
                        html: `<div style="display:flex;flex-direction:column;align-items:center;">
                            <div class="station-label" title="${nombre}">${nombre}</div>
                            ${iconoHtml}
                        </div>`,
                        iconSize: [Math.max(tamaño, 60), tamaño + 18],
                        iconAnchor: [Math.max(tamaño, 60) / 2, tamaño + 18],
                        popupAnchor: [0, -(tamaño + 18)],
                        className: 'icono-simple'
                    });
                }
                
                // BOMBAS, POZOS, REBOMBEOS
                let iconoUrl = null;
                if (tipo === 'pozo' || tipo === 'bomba' || tipo === 'rebombeo') {
                    const estado = obtenerEstadoArrancador(estacion, tipo);
                    iconoUrl = estado === "Encendido"
                        ? limpiarUrl(config.icono_url_on) || limpiarUrl(config.icono_url)
                        : limpiarUrl(config.icono_url_off) || limpiarUrl(config.icono_url);
                } else {
                    iconoUrl = limpiarUrl(config.icono_url);
                }
                
                let iconoHtml = '';
                if (iconoUrl) {
                    iconoHtml = `<div style="width:${tamaño}px; height:${tamaño}px; ${estilos}">
                        <img src="${iconoUrl}" width="${tamaño}" height="${tamaño}" style="display:block;">
                    </div>`;
                } else {
                    iconoHtml = `<div style="
                        width: ${tamaño}px;
                        height: ${tamaño}px;
                        border-radius: 50%;
                        display: flex;
                        align-items: center;
                        justify-content: center;
                        ${estilos}
                    ">
                        <div style="width: 20px; height: 20px; border-radius: 50%; background: ${config.color || '#7f8c8d'};"></div>
                    </div>`;
                }
                
                return L.divIcon({
                    html: `<div style="display:flex;flex-direction:column;align-items:center;">
                        <div class="station-label" title="${nombre}">${nombre}</div>
                        ${iconoHtml}
                    </div>`,
                    iconSize: [Math.max(tamaño, 60), tamaño + 18],
                    iconAnchor: [Math.max(tamaño, 60) / 2, tamaño + 18],
                    popupAnchor: [0, -(tamaño + 18)],
                    className: 'icono-simple'
                });
            }
            
            function crearPopupContent(estaciones) {
                if (!estaciones || estaciones.length === 0) return '';
                const nombreEstacion = estaciones[0].nombre || 'Estación';
                let html = `<div class="custom-popup"><h4>${nombreEstacion}</h4><hr>`;
                const algunOffline = estaciones.some(est => esOffline(est.en_linea));
                const estadoLinea = algunOffline ? '<span class="status-offline">Fuera de linea</span>' : '<span class="status-online">En linea</span>';
                html += `<div class="var-row"><span class="var-label">Estado General:</span><span class="var-value">${estadoLinea}</span></div>`;
                const alarmasActivas = estaciones.filter(est => tieneAlarma(est));
                if (alarmasActivas.length > 0) {
                    html += `<div class="var-row"><span class="var-label" style="color:#f39c12;">⚠️ Alarma:</span><span class="var-value" style="color:#f39c12;font-weight:bold;">ACTIVA</span></div>`;
                }
                html += `<hr>`;
                estaciones.forEach((estacion, index) => {
                    const tipo = estacion.tipo || 'generico';
                    if (estaciones.length > 1 && index > 0) {
                        html += `<hr style="border-color: #bdc3c7;">`;
                    }
                    const tipoLabel = tipo.charAt(0).toUpperCase() + tipo.slice(1);
                    const alarmaLabel = tieneAlarma(estacion) ? '<span style="color:#f39c12;">⚠️</span> ' : '';
                    html += `<div style="font-weight:bold;color:#3498db;margin:8px 0 4px 0;">${alarmaLabel}${tipoLabel}</div>`;
                    if (tipo === 'tanque' || tipo === 'sensor') {
                        const niveles = obtenerNiveles(estacion);
                        if (niveles.elevado !== null) {
                            html += `<div class="var-row"><span class="var-label">Nivel Elevado:</span><span class="var-value">${Math.round(niveles.elevado)}%</span></div>`;
                        }
                        if (niveles.superficial !== null) {
                            html += `<div class="var-row"><span class="var-label">Nivel Superficial:</span><span class="var-value">${Math.round(niveles.superficial)}%</span></div>`;
                        }
                    } else if (tipo === 'pozo' || tipo === 'bomba' || tipo === 'rebombeo') {
                        const estadoBomba = obtenerEstadoArrancador(estacion, tipo);
                        const estadoTexto = estadoBomba === "Encendido" ?
                            '<span style="color:#27ae60;font-weight:bold;">Encendido</span>' :
                            '<span style="color:#e74c3c;font-weight:bold;">Apagado</span>';
                        html += `<div class="var-row"><span class="var-label">Estado del Arrancador:</span><span class="var-value">${estadoTexto}</span></div>`;
                    }
                    for (const key in estacion) {
                        if (!['nombre', 'latitud', 'longitud', 'tipo', 'estado_bomba', 'en_linea', 'icono', 'icono_url', 'icono_url_on', 'icono_url_off', 'Nivel', 'nivel', 'Porcentaje (%)', 'Porcentaje', 'Nivel Tanque Superficial', 'Nivel Tanque Elevado', 'Estado del Arrancador', 'Estado del Arrancador Rebombeo 1', 'Estado del Arrancador Rebombeo 2', 'Alarma', '_timestamp_actualizacion'].includes(key)) {
                            const value = typeof estacion[key] === 'number'
                                ? estacion[key].toLocaleString('es-ES', { minimumFractionDigits: 2, maximumFractionDigits: 2 })
                                : estacion[key];
                            html += `<div class="var-row"><span class="var-label">${key}:</span><span class="var-value">${value}</span></div>`;
                        }
                    }
                });
                html += `<hr><div class="timestamp">📅 ${new Date().toLocaleString('es-ES')}</div></div>`;
                return html;
            }
            function agruparEstacionesPorNombre(estaciones) {
                const grupos = new Map();
                estaciones.forEach(estacion => {
                    const nombre = estacion.nombre || `${estacion.latitud},${estacion.longitud}`;
                    if (!grupos.has(nombre)) {
                        grupos.set(nombre, []);
                    }
                    grupos.get(nombre).push(estacion);
                });
                return grupos;
            }
            function actualizarEstadisticas(datos) {
                if (!datos || !datos.estaciones) return;
                let total = 0, pozos_encendidos = 0, pozos_apagados = 0, tanques = 0;
                let bombas_encendidas = 0, bombas_apagadas = 0, rebombeos_encendidos = 0, rebombeos_apagados = 0;
                let sensores = 0, offline_count = 0, online = 0;
                datos.estaciones.forEach(estacion => {
                    total++;
                    const offline = esOffline(estacion.en_linea);
                    const tipo = estacion.tipo || 'generico';
                    if (offline) {
                        offline_count++;
                    } else {
                        online++;
                        if (tipo === 'pozo') {
                            const estado = obtenerEstadoArrancador(estacion, tipo);
                            if (estado === "Encendido") pozos_encendidos++; else pozos_apagados++;
                        } else if (tipo === 'tanque') {
                            tanques++;
                        } else if (tipo === 'bomba') {
                            const estado = obtenerEstadoArrancador(estacion, tipo);
                            if (estado === "Encendido") bombas_encendidas++; else bombas_apagadas++;
                        } else if (tipo === 'rebombeo') {
                            const estado = obtenerEstadoArrancador(estacion, tipo);
                            if (estado === "Encendido") rebombeos_encendidos++; else rebombeos_apagados++;
                        } else if (tipo === 'sensor') {
                            sensores++;
                        }
                    }
                });
                const tipos = datos.tipos || {};
                const stats = [
                    { tipo: 'total', value: total, label: 'Total' },
                    { tipo: 'pozo', estado: 1, value: pozos_encendidos, label: 'Pozos Enc.' },
                    { tipo: 'pozo', estado: 0, value: pozos_apagados, label: 'Pozos Apag.' },
                    { tipo: 'tanque', value: tanques, label: 'Tanques' },
                    { tipo: 'bomba', estado: 1, value: bombas_encendidas, label: 'Bombas Enc.' },
                    { tipo: 'bomba', estado: 0, value: bombas_apagadas, label: 'Bombas Apag.' },
                    { tipo: 'rebombeo', estado: 1, value: rebombeos_encendidos, label: 'Rebom. Enc.' },
                    { tipo: 'rebombeo', estado: 0, value: rebombeos_apagados, label: 'Rebom. Apag.' },
                    { tipo: 'sensor', value: sensores, label: 'Sensores Río' },
                    { tipo: 'offline', value: offline_count, label: 'Offline' },
                    { tipo: 'online', value: online, label: 'Online' },
                    { tipo: 'reloj', value: '""" + tiempo_str + """', label: 'Actualizado' }
                ];
                const statsBar = document.getElementById('stats-bar');
                if (!statsBar) return;
                statsBar.innerHTML = '';
                stats.forEach(stat => {
                    if (stat.value === 0 && !['total', 'online', 'offline', 'reloj'].includes(stat.tipo)) return;
                    const config = tipos[stat.tipo] || tipos['generico'] || {};
                    let iconoUrl = null;
                    if (stat.tipo === 'pozo' || stat.tipo === 'bomba' || stat.tipo === 'rebombeo') {
                        iconoUrl = stat.estado === 1 ? (limpiarUrl(config.icono_url_on) || limpiarUrl(config.icono_url)) : (limpiarUrl(config.icono_url_off) || limpiarUrl(config.icono_url));
                    } else if (stat.tipo === 'offline') {
                        iconoUrl = 'https://raw.githubusercontent.com/AlarmasCiateq/SCADA_T/main/iconos/Offline.svg';
                    } else if (stat.tipo === 'online') {
                        iconoUrl = 'https://raw.githubusercontent.com/AlarmasCiateq/SCADA_T/main/iconos/Online_Alarma.svg';
                    } else if (stat.tipo === 'total') {
                        iconoUrl = 'https://raw.githubusercontent.com/AlarmasCiateq/SCADA_T/main/iconos/transmite.svg';
                    } else if (stat.tipo === 'reloj') {
                        iconoUrl = 'https://raw.githubusercontent.com/AlarmasCiateq/SCADA_T/main/iconos/update.svg';
                    } else {
                        iconoUrl = limpiarUrl(config.icono_url);
                    }
                    const item = document.createElement('div');
                    item.className = 'stat-item';
                    let iconHtml = iconoUrl
                        ? `<div class="stat-icon"><img src="${iconoUrl}" alt="${stat.tipo}"></div>`
                        : `<div class="stat-icon" style="color:${config.color || '#7f8c8d'};font-size:20px;">⬤</div>`;
                    item.innerHTML = iconHtml + '<div class="stat-value">' + stat.value + '</div>' + '<div class="stat-label">' + stat.label + '</div>';
                    statsBar.appendChild(item);
                });
            }
            function zoomATodosLosIconos() {
                if (!map || markers.size === 0) return;
                const todasCoords = Array.from(markers.values()).map(m => m.getLatLng());
                map.fitBounds(todasCoords, { padding: [40, 40] });
                try {
                    localStorage.setItem('scada_map_zoom', map.getZoom().toString());
                    localStorage.setItem('scada_map_center', JSON.stringify({lat: map.getCenter().lat, lng: map.getCenter().lng}));
                } catch(e) {}
            }
            L.Control.ZoomAll = L.Control.extend({
                options: { position: 'topleft' },
                onAdd: function(mapInstance) {
                    const container = L.DomUtil.create('div', 'leaflet-bar leaflet-control leaflet-control-zoom-all');
                    const button = L.DomUtil.create('a', 'leaflet-control-zoom-all', container);
                    button.href = '#';
                    button.title = 'Ver todas las estaciones';
                    button.innerHTML = '<i>⌂</i>';
                    L.DomEvent.disableClickPropagation(button);
                    L.DomEvent.on(button, 'click', function(e) {
                        L.DomEvent.stopPropagation(e);
                        L.DomEvent.preventDefault(e);
                        zoomATodosLosIconos();
                    });
                    return container;
                }
            });
            L.control.zoomAll = function(opts) { return new L.Control.ZoomAll(opts); };
            function initMap() {
                try {
                    map = L.map('map', { zoomControl: true, scrollWheelZoom: true, dragging: true });
                    <!--L.tileLayer('https://{s}.basemaps.cartocdn.com/light_all/{z}/{x}/{y}{r}.png', {-->
                    <!--    attribution: '', subdomains: 'abcd', maxZoom: 19-->
                    <!--}).addTo(map);-->
                    L.tileLayer(
                        'https://server.arcgisonline.com/ArcGIS/rest/services/World_Topo_Map/MapServer/tile/{z}/{y}/{x}',
                        {
                            attribution: 'Tiles © Esri',
                            maxZoom: 19
                        }
                    ).addTo(map);                    
                    L.control.zoomAll().addTo(map);
                    const todasCoords = [];
                    DATOS_INICIALES.estaciones.forEach(est => {
                        if (est.latitud && est.longitud) todasCoords.push([parseFloat(est.latitud), parseFloat(est.longitud)]);
                    });
                    const savedZoom = localStorage.getItem('scada_map_zoom');
                    const savedCenter = localStorage.getItem('scada_map_center');
                    const wasInitialized = localStorage.getItem('scada_map_initialized') === 'true';
                    if (wasInitialized && savedZoom && savedCenter) {
                        try {
                            const center = JSON.parse(savedCenter);
                            map.setView([center.lat, center.lng], parseInt(savedZoom));
                        } catch(e) {
                            if (todasCoords.length > 0) map.fitBounds(L.latLngBounds(todasCoords), { padding: [40, 40] });
                        }
                    } else {
                        if (todasCoords.length > 0) {
                            map.fitBounds(L.latLngBounds(todasCoords), { padding: [40, 40] });
                            localStorage.setItem('scada_map_initialized', 'true');
                        }
                    }
                    const gruposEstaciones = agruparEstacionesPorNombre(DATOS_INICIALES.estaciones);
                    gruposEstaciones.forEach((estaciones, nombre) => {
                        if (estaciones.length === 0) return;
                        const primeraEstacion = estaciones[0];
                        if (!primeraEstacion.latitud || !primeraEstacion.longitud) return;
                        const lat = parseFloat(primeraEstacion.latitud);
                        const lng = parseFloat(primeraEstacion.longitud);
                        let icono = estaciones.length > 1 ? crearIconoCompuesto(estaciones) : crearIconoSimple(estaciones[0]);
                        const marker = L.marker([lat, lng], { icon: icono })
                            .bindPopup(crearPopupContent(estaciones), { maxWidth: 360 })
                            .addTo(map);
                        markers.set(nombre, marker);
                    });
                    actualizarEstadisticas(DATOS_INICIALES);
                    document.getElementById('loading').classList.add('hidden');
                    window.map = map;
                } catch(e) {
                    document.getElementById('loading').innerHTML = `<div style="color:#e74c3c;text-align:center;padding:20px;">❌ Error: ${e.message}</div>`;
                    console.error('Error:', e);
                }
            }
            if (document.readyState === 'loading') {
                document.addEventListener('DOMContentLoaded', initMap);
            } else {
                initMap();
            }
        })();
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
time.sleep(60)
st.rerun()

# CSS AGRESIVO
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
#loading {
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background: #0e1117;
    display: flex;
    justify-content: center;
    align-items: center;
    color: #3498db;
    font-family: Arial;
    font-size: 18px;
    z-index: 9999;
    transition: opacity 0.1s;
}
#loading.hidden {
    opacity: 0;
    pointer-events: none;
}
#debug-timestamp {
    position: fixed;
    bottom: 5px;
    right: 10px;
    background: rgba(0,0,0,0.7);
    color: #27ae60;
    padding: 3px 8px;
    font-family: monospace;
    font-size: 11px;
    border-radius: 3px;
    z-index: 1000;
}
/* Etiqueta de nombre - COMPACTA, truncada con ... */
.station-label {
    background: rgba(255, 255, 255, 0.85);
    border: 1px solid rgba(0, 0, 0, 0.2);
    border-radius: 3px;
    padding: 1px 4px;
    font-size: 9px;
    font-weight: bold;
    color: #2c3e50;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
    text-align: center;
    max-width: 70px;
    margin-bottom: 2px;
}
</style>
""", unsafe_allow_html=True)

# ========================================
# OBTENER TOKEN DE GITHUB
# ========================================
def obtener_token_github():
    try:
        if hasattr(st, 'secrets') and "GITHUB_TOKEN" in st.secrets:
            return st.secrets["GITHUB_TOKEN"]
    except:
        pass
    return os.getenv("GITHUB_TOKEN", None)

# ========================================
# CARGAR DATOS FRESH DE GITHUB
# ========================================
def cargar_datos_github(max_intentos=3):
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
            datos = json.loads(content_str)
            datos['_timestamp_actualizacion'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            return datos, True
        except Exception as e:
            print(f"Error cargando datos (intento {intento + 1}): {e}")
            if intento < max_intentos - 1:
                time.sleep(1)
                continue
            return None, False
    return None, False

# ========================================
# CARGAR DATOS
# ========================================
datos, exito = cargar_datos_github()
if not datos or not exito:
    st.markdown("""
    <div style="position:fixed;top:0;left:0;width:100%;height:100%;background:#0e1117;color:white;
    display:flex;justify-content:center;align-items:center;font-family:Arial;">
        <div style="text-align:center;padding:20px;">
            <h2>💧 SCADA Monitor</h2>
            <p style="color:#e74c3c; margin-top:15px;">Error: No se pudieron cargar los datos de GitHub</p>
            <p style="font-size:14px; margin-top:10px; color:#95a5a6;">Verifique conexion a internet</p>
        </div>
    </div>
    """, unsafe_allow_html=True)
    time.sleep(60)
    st.rerun()

# ========================================
# PREPARAR DATOS PARA HTML
# ========================================
tiempo_str = datetime.now().strftime('%H:%M:%S')
timestamp_debug = datos.get('_timestamp_actualizacion', tiempo_str)
datos_json_safe = json.dumps(datos, ensure_ascii=False)
datos_json_safe = (datos_json_safe.replace('\\', '\\\\')
    .replace("'", "\\'")
    .replace('</', '<\\/').replace('\n', '\\n')
    .replace('\r', '\\r').replace('\t', '\\t'))

# ========================================
# HTML + JAVASCRIPT
# ========================================
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
        body { font-family: Arial, sans-serif; background: #0e1117; overflow: hidden; height: 100vh; width: 100vw; }
        #map { position: absolute; top: 0; left: 0; width: 100%; height: 100%; z-index: 1; }
        #stats-bar {
            position: fixed;
            top: 10px;
            right: 15px;
            background: rgba(255, 255, 255, 0.95);
            padding: 8px;
            border-radius: 6px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.15);
            z-index: 1000;
            display: flex;
            gap: 12px;
            align-items: center;
            font-family: Arial, sans-serif;
            flex-wrap: nowrap;
            overflow-x: auto;
            max-width: 90%;
        }
        .stat-item {
            display: flex;
            flex-direction: column;
            align-items: center;
            min-width: 65px;
        }
        .stat-icon {
            width: 24px;
            height: 24px;
            margin-bottom: 2px;
            display: flex;
            align-items: center;
            justify-content: center;
        }
        .stat-icon img {
            width: 100%;
            height: 100%;
            object-fit: contain;
        }
        .stat-value {
            font-weight: bold;
            color: #2c3e50;
            font-size: 14px;
            text-align: center;
        }
        .stat-label {
            font-size: 8px;
            color: #7f8c8d;
            text-align: center;
            white-space: nowrap;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }
        .custom-popup {
            font-family: Arial;
            padding: 12px;
            min-width: 320px;
            background: white;
            border-radius: 6px;
        }
        .custom-popup h4 {
            margin: 0 0 10px 0;
            color: #2c3e50;
            font-size: 16px;
            font-weight: bold;
        }
        .custom-popup hr {
            margin: 8px 0;
            border-color: #ecf0f1;
        }
        .custom-popup .var-row {
            margin: 6px 0;
            padding: 4px 0;
            display: flex;
            justify-content: space-between;
        }
        .custom-popup .var-label {
            color: #2c3e50;
            font-weight: 600;
            font-size: 13px;
            min-width: 140px;
        }
        .custom-popup .var-value {
            color: #2c3e50;
            font-weight: bold;
            font-size: 14px;
            text-align: right;
            min-width: 80px;
        }
        .custom-popup .timestamp {
            font-size: 11px;
            color: #95a5a6;
            text-align: center;
            margin-top: 8px;
        }
        .status-online { color: #27ae60; font-weight: bold; }
        .status-offline { color: #e74c3c; font-weight: bold; }
        #loading {
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: #0e1117;
            display: flex;
            justify-content: center;
            align-items: center;
            color: #3498db;
            font-family: Arial;
            font-size: 18px;
            z-index: 9999;
            transition: opacity 0.1s;
        }
        #loading.hidden {
            opacity: 0;
            pointer-events: none;
        }
        #debug-timestamp {
            position: fixed;
            bottom: 5px;
            right: 10px;
            background: rgba(0,0,0,0.7);
            color: #27ae60;
            padding: 3px 8px;
            font-family: monospace;
            font-size: 11px;
            border-radius: 3px;
            z-index: 1000;
        }
        .leaflet-control-zoom-all {
            background: #fff;
            border: 2px solid rgba(0,0,0,0.2);
            border-radius: 4px;
            box-shadow: 0 1px 5px rgba(0,0,0,0.4);
            cursor: pointer;
            margin-top: 5px;
            transition: all 0.2s;
        }
        .leaflet-control-zoom-all:hover {
            background: #f4f4f4;
            box-shadow: 0 1px 7px rgba(0,0,0,0.45);
        }
        .leaflet-control-zoom-all:active {
            background: #e8e8e8;
        }
        .leaflet-control-zoom-all i {
            display: block;
            width: 30px;
            height: 30px;
            line-height: 30px;
            text-align: center;
            font-weight: bold;
            color: #333;
            font-size: 20px;
        }
        .leaflet-control-zoom-all:hover i {
            color: #2c3e50;
        }
        .leaflet-div-icon {
            background: transparent !important;
            border: none !important;
        }
    </style>
</head>
<body>
    <div id="loading">Cargando...</div>
    <div id="map"></div>
    <div id="stats-bar"></div>
    <div id="debug-timestamp">""" + timestamp_debug + """</div>
    <script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"></script>
    <script>
        (function() {
            'use strict';
            window.addEventListener('beforeunload', function() {
                if (window.map) {
                    try {
                        const zoom = window.map.getZoom();
                        const center = window.map.getCenter();
                        localStorage.setItem('scada_map_zoom', zoom.toString());
                        localStorage.setItem('scada_map_center', JSON.stringify({lat: center.lat, lng: center.lng}));
                        localStorage.setItem('scada_map_initialized', 'true');
                    } catch(e) {}
                }
            });
            const DATOS_INICIALES = """ + datos_json_safe + """;
            let map = null;
            let markers = new Map();
            function limpiarUrl(url) {
                if (!url) return null;
                return url.trim().replace(/\\s+/g, '%20');
            }
            function esOffline(enLinea) {
                if (enLinea === undefined || enLinea === null) return false;
                const valor = String(enLinea).trim().toLowerCase();
                return valor === '0' || valor === 'false' || valor === 'off' || valor === 'no';
            }
            function tieneAlarma(estacion) {
                try {
                    if (estacion["Alarma"] === undefined || estacion["Alarma"] === null) {
                        return false;
                    }
                    const valor = String(estacion["Alarma"]).trim().toLowerCase();
                    return valor === 'on' || valor === 'alarma' || valor === '1' || valor === 'true' || valor === 'si' || valor === 'yes';
                } catch(e) {
                    return false;
                }
            }
            function obtenerNiveles(estacion) {
                let nivelSuperficial = null;
                let nivelElevado = null;
                if (estacion["Nivel Tanque Superficial"] !== undefined) {
                    let v = parseFloat(estacion["Nivel Tanque Superficial"]);
                    if (!isNaN(v)) nivelSuperficial = Math.max(0, Math.min(100, v));
                }
                if (estacion["Nivel Tanque Elevado"] !== undefined) {
                    let v = parseFloat(estacion["Nivel Tanque Elevado"]);
                    if (!isNaN(v)) nivelElevado = Math.max(0, Math.min(100, v));
                }
                if (nivelSuperficial === null && nivelElevado === null) {
                    const camposGenericos = ['Porcentaje (%)', 'Porcentaje', 'Nivel (%)', 'nivel_%', 'Nivel', 'nivel'];
                    for (let campo of camposGenericos) {
                        if (estacion[campo] !== undefined && estacion[campo] !== null) {
                            let v = parseFloat(estacion[campo]);
                            if (!isNaN(v)) {
                                if (nivelElevado === null) nivelElevado = Math.max(0, Math.min(100, v));
                                else if (nivelSuperficial === null) nivelSuperficial = Math.max(0, Math.min(100, v));
                            }
                        }
                    }
                }
                return {
                    superficial: nivelSuperficial,
                    elevado: nivelElevado,
                    principal: (nivelElevado !== null) ? nivelElevado : (nivelSuperficial !== null ? nivelSuperficial : 0)
                };
            }
            function obtenerEstadoArrancador(estacion, tipo) {
                if (tipo === 'rebombeo') {
                    if (estacion["Estado del Arrancador Rebombeo 1"] !== undefined) {
                        return estacion["Estado del Arrancador Rebombeo 1"];
                    }
                    if (estacion["Estado del Arrancador Rebombeo 2"] !== undefined) {
                        return estacion["Estado del Arrancador Rebombeo 2"];
                    }
                }
                return estacion["Estado del Arrancador"] || "Apagado";
            }
            // ========================================
            // ESTILOS BASE - MANTIENE TAMAÑO ORIGINAL DEL ICONO (32x32)
            // ========================================
            function getEstilosBase(alarma, offline) {
                let styles = 'position: relative; width: 32px; height: 32px; display: flex; align-items: center; justify-content: center; box-sizing: border-box;';
                styles += ' background: transparent; ';
                if (alarma) {
                    styles += ' background-color: rgba(255, 193, 7, 0.8); ';
                }
                if (offline) {
                    styles += ' border: 3px solid #e74c3c; ';
                } else {
                    styles += ' border: none; ';
                }
                return styles;
            }
            // ========================================
            // FUNCIONES PARA CREAR SUB-ICONOS (28x28)
            // ========================================
            function crearSubIconoTanque(estacion, tamaño = 28) {
                const niveles = obtenerNiveles(estacion);
                const nivel = niveles.principal;
                const tipos = DATOS_INICIALES.tipos || {};
                const config = tipos['tanque'] || tipos['generico'] || {};
                const iconoUrl = limpiarUrl(config.icono_url) || null;
                const alturaLlenado = Math.round((nivel / 100) * (tamaño - 4));
                if (iconoUrl) {
                    return `<div style="position:relative;width:${tamaño}px;height:${tamaño}px">
                        <div style="position:absolute;bottom:0;left:0;width:${tamaño}px;height:${alturaLlenado}px;background:rgba(52,152,219,0.85);"></div>
                        <img src="${iconoUrl}" width="${tamaño}" height="${tamaño}" style="position:absolute;top:0;left:0;z-index:1;">
                        <div style="position:absolute;bottom:2px;width:${tamaño}px;text-align:center;font-size:9px;color:blue;font-weight:bold;text-shadow:0 1px 2px rgba(0,0,0,0.8)">${Math.round(nivel)}%</div>
                    </div>`;
                } else {
                    const yInicio = (tamaño - 4) - alturaLlenado;
                    const svg = `<svg xmlns="http://www.w3.org/2000/svg" width="${tamaño}" height="${tamaño}" viewBox="0 0 ${tamaño} ${tamaño}">
                        <rect x="0" y="${yInicio}" width="${tamaño}" height="${alturaLlenado}" fill="rgba(52,152,219,0.85)"/>
                        <rect x="2" y="2" width="${tamaño-4}" height="${tamaño-4}" fill="#2c3e50"/>
                        <text x="${tamaño/2}" y="${tamaño/2 + 3}" font-family="Arial" font-size="8" fill="white" text-anchor="middle" font-weight="bold">${Math.round(nivel)}%</text>
                    </svg>`;
                    return `<div style="position:relative;width:${tamaño}px;height:${tamaño}px">${svg}</div>`;
                }
            }
            function crearSubIconoRio(estacion, tamaño = 28) {
                const niveles = obtenerNiveles(estacion);
                const nivel = niveles.principal;
                const tipos = DATOS_INICIALES.tipos || {};
                const config = tipos['sensor'] || tipos['generico'] || {};
                const iconoUrl = limpiarUrl(config.icono_url) || null;
                const alturaLlenado = Math.round((nivel / 100) * (tamaño - 4));
                if (iconoUrl) {
                    return `<div style="position:relative;width:${tamaño}px;height:${tamaño}px">
                        <div style="position:absolute;bottom:0;left:0;width:${tamaño}px;height:${alturaLlenado}px;background:rgba(52,152,219,0.85);"></div>
                        <img src="${iconoUrl}" width="${tamaño}" height="${tamaño}" style="position:absolute;top:0;left:0;z-index:1;">
                        <div style="position:absolute;bottom:2px;width:${tamaño}px;text-align:center;font-size:9px;color:blue;font-weight:bold;text-shadow:0 1px 2px rgba(0,0,0,0.8)">${Math.round(nivel)}%</div>
                    </div>`;
                } else {
                    const yInicio = (tamaño - 4) - alturaLlenado;
                    const svg = `<svg xmlns="http://www.w3.org/2000/svg" width="${tamaño}" height="${tamaño}" viewBox="0 0 ${tamaño} ${tamaño}">
                        <rect x="0" y="${yInicio}" width="${tamaño}" height="${alturaLlenado}" fill="rgba(52,152,219,0.85)"/>
                        <path d="M2 ${tamaño/2} Q${tamaño/2} ${tamaño/2 - 4} ${tamaño-2} ${tamaño/2} L${tamaño-2} ${tamaño-2} Q${tamaño/2} ${tamaño-4} 2 ${tamaño-2} Z" fill="#2c3e50"/>
                        <text x="${tamaño/2}" y="${tamaño/2 + 3}" font-family="Arial" font-size="8" fill="blue" text-anchor="middle" font-weight="bold">${Math.round(nivel)}%</text>
                    </svg>`;
                    return `<div style="position:relative;width:${tamaño}px;height:${tamaño}px">${svg}</div>`;
                }
            }
            function crearSubIconoBomba(estacion, tipo, tamaño = 28) {
                const offline = esOffline(estacion.en_linea);
                const alarma = tieneAlarma(estacion);
                const tipos = DATOS_INICIALES.tipos || {};
                const config = tipos[tipo] || tipos['generico'] || {};
                const estado = obtenerEstadoArrancador(estacion, tipo);
                let iconoUrl = null;
                if (estado === "Encendido") {
                    iconoUrl = limpiarUrl(config.icono_url_on) || limpiarUrl(config.icono_url) || null;
                } else {
                    iconoUrl = limpiarUrl(config.icono_url_off) || limpiarUrl(config.icono_url) || null;
                }
                const estilos = getEstilosBase(alarma, offline);
                if (iconoUrl) {
                    return `<div style="${estilos}">
                        <img src="${iconoUrl}" width="${tamaño}" height="${tamaño}" style="display:block;">
                    </div>`;
                } else {
                    const color = estado === "Encendido" ? '#27ae60' : '#e74c3c';
                    return `<div style="${estilos}">
                        <div style="width:${tamaño-6}px;height:${tamaño-6}px;border-radius:50%;background:${color};"></div>
                    </div>`;
                }
            }
            function crearSubIconoGenerico(estacion, tamaño = 28) {
                const offline = esOffline(estacion.en_linea);
                const alarma = tieneAlarma(estacion);
                const tipo = estacion.tipo || 'generico';
                const tipos = DATOS_INICIALES.tipos || {};
                const config = tipos[tipo] || tipos['generico'] || {};
                const iconoUrl = limpiarUrl(config.icono_url) || null;
                const color = config.color || '#7f8c8d';
                const estilos = getEstilosBase(alarma, offline);
                if (iconoUrl) {
                    return `<div style="${estilos}">
                        <img src="${iconoUrl}" width="${tamaño}" height="${tamaño}" style="display:block;">
                    </div>`;
                } else {
                    return `<div style="${estilos}">
                        <div style="width:${tamaño-6}px;height:${tamaño-6}px;border-radius:50%;background:${color};"></div>
                    </div>`;
                }
            }
            function crearSubIcono(estacion, tamaño = 28) {
                const tipo = estacion.tipo || 'generico';
                if (tipo === 'tanque') {
                    return crearSubIconoTanque(estacion, tamaño);
                } else if (tipo === 'sensor') {
                    return crearSubIconoRio(estacion, tamaño);
                } else if (tipo === 'pozo' || tipo === 'bomba' || tipo === 'rebombeo') {
                    return crearSubIconoBomba(estacion, tipo, tamaño);
                } else {
                    return crearSubIconoGenerico(estacion, tamaño);
                }
            }
            // ========================================
            // ICONO COMPUESTO - CON NOMBRE COMPACTO
            // ========================================
            function crearIconoCompuesto(estaciones) {
                if (!estaciones || estaciones.length === 0) return null;
                const count = estaciones.length;
                const cols = count === 1 ? 1 : 2;
                const rows = Math.ceil(count / 2);
                const iconSize = 28;
                const gap = 2;
                const totalWidth = (cols * iconSize) + ((cols - 1) * gap);
                const totalHeight = (rows * iconSize) + ((rows - 1) * gap);
                const nombre = estaciones[0].nombre || 'Estación';
                
                let subIconosHtml = '';
                let posicion = 0;
                for (let row = 0; row < rows; row++) {
                    for (let col = 0; col < cols; col++) {
                        if (posicion >= count) break;
                        const est = estaciones[posicion];
                        const left = col * (iconSize + gap);
                        const top = row * (iconSize + gap);
                        subIconosHtml += `<div style="position:absolute;left:${left}px;top:${top}px;">
                            ${crearSubIcono(est, iconSize)}
                        </div>`;
                        posicion++;
                    }
                }
                
                const htmlCompleto = `<div style="display:flex;flex-direction:column;align-items:center;">
                    <div class="station-label" title="${nombre}">${nombre}</div>
                    <div style="position: relative; width: ${totalWidth}px; height: ${totalHeight}px; background: transparent;">
                        ${subIconosHtml}
                    </div>
                </div>`;
                
                return L.divIcon({
                    html: htmlCompleto,
                    iconSize: [Math.max(totalWidth, 60), totalHeight + 18],
                    iconAnchor: [Math.max(totalWidth, 60) / 2, totalHeight + 18],
                    popupAnchor: [0, -(totalHeight + 18)],
                    className: 'icono-compuesto'
                });
            }
            
            // ========================================
            // ICONO SIMPLE - TAMAÑO ORIGINAL 32x32 + NOMBRE COMPACTO
            // ========================================
            function crearIconoSimple(estacion) {
                const tipo = estacion.tipo || 'generico';
                const offline = esOffline(estacion.en_linea);
                const alarma = tieneAlarma(estacion);
                const niveles = obtenerNiveles(estacion);
                const tipos = DATOS_INICIALES.tipos || {};
                const config = tipos[tipo] || tipos['generico'] || {};
                const tamaño = 32;
                const estilos = getEstilosBase(alarma, offline);
                const nombre = estacion.nombre || 'Estación';
                
                // TANQUE
                if (tipo === 'tanque') {
                    const iconoUrl = limpiarUrl(config.icono_url) || null;
                    const alturaLlenado = Math.round((niveles.principal / 100) * tamaño);
                    let iconoHtml = '';
                    if (iconoUrl) {
                        iconoHtml = `<div style="position:relative; width:${tamaño}px; height:${tamaño}px; ${estilos}">
                            <div style="position:absolute; bottom:0; left:0; width:100%; height:${alturaLlenado}px; background:rgba(52,152,219,0.85);"></div>
                            <img src="${iconoUrl}" width="${tamaño}" height="${tamaño}" style="position:relative; z-index:1;">
                            <div style="position:absolute; bottom:4px; width:100%; text-align:center; font-size:11px; color:blue; font-weight:bold; text-shadow:0 1px 2px rgba(0,0,0,0.8); z-index:2;">${Math.round(niveles.principal)}%</div>
                        </div>`;
                    } else {
                        const yInicio = tamaño - alturaLlenado;
                        const svg = `<svg xmlns="http://www.w3.org/2000/svg" width="${tamaño}" height="${tamaño}" viewBox="0 0 ${tamaño} ${tamaño}">
                            <rect x="0" y="${yInicio}" width="${tamaño}" height="${alturaLlenado}" fill="rgba(52,152,219,0.85)"/>
                            <rect x="2" y="2" width="${tamaño-4}" height="${tamaño-4}" fill="#2c3e50"/>
                            <text x="${tamaño/2}" y="${tamaño/2 + 3}" font-family="Arial" font-size="10" fill="white" text-anchor="middle" font-weight="bold">${Math.round(niveles.principal)}%</text>
                        </svg>`;
                        iconoHtml = `<div style="width:${tamaño}px; height:${tamaño}px; ${estilos}">${svg}</div>`;
                    }
                    return L.divIcon({
                        html: `<div style="display:flex;flex-direction:column;align-items:center;">
                            <div class="station-label" title="${nombre}">${nombre}</div>
                            ${iconoHtml}
                        </div>`,
                        iconSize: [Math.max(tamaño, 60), tamaño + 18],
                        iconAnchor: [Math.max(tamaño, 60) / 2, tamaño + 18],
                        popupAnchor: [0, -(tamaño + 18)],
                        className: 'icono-simple'
                    });
                }
                
                // SENSOR
                if (tipo === 'sensor') {
                    const iconoUrl = limpiarUrl(config.icono_url) || null;
                    const alturaLlenado = Math.round((niveles.principal / 100) * tamaño);
                    let iconoHtml = '';
                    if (iconoUrl) {
                        iconoHtml = `<div style="position:relative; width:${tamaño}px; height:${tamaño}px; ${estilos}">
                            <div style="position:absolute; bottom:0; left:0; width:100%; height:${alturaLlenado}px; background:rgba(52,152,219,0.85);"></div>
                            <img src="${iconoUrl}" width="${tamaño}" height="${tamaño}" style="position:relative; z-index:1;">
                            <div style="position:absolute; bottom:4px; width:100%; text-align:center; font-size:11px; color:blue; font-weight:bold; text-shadow:0 1px 2px rgba(0,0,0,0.8); z-index:2;">${Math.round(niveles.principal)}%</div>
                        </div>`;
                    } else {
                        const yInicio = tamaño - alturaLlenado;
                        const svg = `<svg xmlns="http://www.w3.org/2000/svg" width="${tamaño}" height="${tamaño}" viewBox="0 0 ${tamaño} ${tamaño}">
                            <rect x="0" y="${yInicio}" width="${tamaño}" height="${alturaLlenado}" fill="rgba(52,152,219,0.85)"/>
                            <path d="M2 ${tamaño/2} Q${tamaño/2} ${tamaño/2 - 4} ${tamaño-2} ${tamaño/2} L${tamaño-2} ${tamaño-2} Q${tamaño/2} ${tamaño-4} 2 ${tamaño-2} Z" fill="#2c3e50"/>
                            <text x="${tamaño/2}" y="${tamaño/2 + 3}" font-family="Arial" font-size="10" fill="blue" text-anchor="middle" font-weight="bold">${Math.round(niveles.principal)}%</text>
                        </svg>`;
                        iconoHtml = `<div style="width:${tamaño}px; height:${tamaño}px; ${estilos}">${svg}</div>`;
                    }
                    return L.divIcon({
                        html: `<div style="display:flex;flex-direction:column;align-items:center;">
                            <div class="station-label" title="${nombre}">${nombre}</div>
                            ${iconoHtml}
                        </div>`,
                        iconSize: [Math.max(tamaño, 60), tamaño + 18],
                        iconAnchor: [Math.max(tamaño, 60) / 2, tamaño + 18],
                        popupAnchor: [0, -(tamaño + 18)],
                        className: 'icono-simple'
                    });
                }
                
                // BOMBAS, POZOS, REBOMBEOS
                let iconoUrl = null;
                if (tipo === 'pozo' || tipo === 'bomba' || tipo === 'rebombeo') {
                    const estado = obtenerEstadoArrancador(estacion, tipo);
                    iconoUrl = estado === "Encendido"
                        ? limpiarUrl(config.icono_url_on) || limpiarUrl(config.icono_url)
                        : limpiarUrl(config.icono_url_off) || limpiarUrl(config.icono_url);
                } else {
                    iconoUrl = limpiarUrl(config.icono_url);
                }
                
                let iconoHtml = '';
                if (iconoUrl) {
                    iconoHtml = `<div style="width:${tamaño}px; height:${tamaño}px; ${estilos}">
                        <img src="${iconoUrl}" width="${tamaño}" height="${tamaño}" style="display:block;">
                    </div>`;
                } else {
                    iconoHtml = `<div style="
                        width: ${tamaño}px;
                        height: ${tamaño}px;
                        border-radius: 50%;
                        display: flex;
                        align-items: center;
                        justify-content: center;
                        ${estilos}
                    ">
                        <div style="width: 20px; height: 20px; border-radius: 50%; background: ${config.color || '#7f8c8d'};"></div>
                    </div>`;
                }
                
                return L.divIcon({
                    html: `<div style="display:flex;flex-direction:column;align-items:center;">
                        <div class="station-label" title="${nombre}">${nombre}</div>
                        ${iconoHtml}
                    </div>`,
                    iconSize: [Math.max(tamaño, 60), tamaño + 18],
                    iconAnchor: [Math.max(tamaño, 60) / 2, tamaño + 18],
                    popupAnchor: [0, -(tamaño + 18)],
                    className: 'icono-simple'
                });
            }
            
            function crearPopupContent(estaciones) {
                if (!estaciones || estaciones.length === 0) return '';
                const nombreEstacion = estaciones[0].nombre || 'Estación';
                let html = `<div class="custom-popup"><h4>${nombreEstacion}</h4><hr>`;
                const algunOffline = estaciones.some(est => esOffline(est.en_linea));
                const estadoLinea = algunOffline ? '<span class="status-offline">Fuera de linea</span>' : '<span class="status-online">En linea</span>';
                html += `<div class="var-row"><span class="var-label">Estado General:</span><span class="var-value">${estadoLinea}</span></div>`;
                const alarmasActivas = estaciones.filter(est => tieneAlarma(est));
                if (alarmasActivas.length > 0) {
                    html += `<div class="var-row"><span class="var-label" style="color:#f39c12;">⚠️ Alarma:</span><span class="var-value" style="color:#f39c12;font-weight:bold;">ACTIVA</span></div>`;
                }
                html += `<hr>`;
                estaciones.forEach((estacion, index) => {
                    const tipo = estacion.tipo || 'generico';
                    if (estaciones.length > 1 && index > 0) {
                        html += `<hr style="border-color: #bdc3c7;">`;
                    }
                    const tipoLabel = tipo.charAt(0).toUpperCase() + tipo.slice(1);
                    const alarmaLabel = tieneAlarma(estacion) ? '<span style="color:#f39c12;">⚠️</span> ' : '';
                    html += `<div style="font-weight:bold;color:#3498db;margin:8px 0 4px 0;">${alarmaLabel}${tipoLabel}</div>`;
                    if (tipo === 'tanque' || tipo === 'sensor') {
                        const niveles = obtenerNiveles(estacion);
                        if (niveles.elevado !== null) {
                            html += `<div class="var-row"><span class="var-label">Nivel Elevado:</span><span class="var-value">${Math.round(niveles.elevado)}%</span></div>`;
                        }
                        if (niveles.superficial !== null) {
                            html += `<div class="var-row"><span class="var-label">Nivel Superficial:</span><span class="var-value">${Math.round(niveles.superficial)}%</span></div>`;
                        }
                    } else if (tipo === 'pozo' || tipo === 'bomba' || tipo === 'rebombeo') {
                        const estadoBomba = obtenerEstadoArrancador(estacion, tipo);
                        const estadoTexto = estadoBomba === "Encendido" ?
                            '<span style="color:#27ae60;font-weight:bold;">Encendido</span>' :
                            '<span style="color:#e74c3c;font-weight:bold;">Apagado</span>';
                        html += `<div class="var-row"><span class="var-label">Estado del Arrancador:</span><span class="var-value">${estadoTexto}</span></div>`;
                    }
                    for (const key in estacion) {
                        if (!['nombre', 'latitud', 'longitud', 'tipo', 'estado_bomba', 'en_linea', 'icono', 'icono_url', 'icono_url_on', 'icono_url_off', 'Nivel', 'nivel', 'Porcentaje (%)', 'Porcentaje', 'Nivel Tanque Superficial', 'Nivel Tanque Elevado', 'Estado del Arrancador', 'Estado del Arrancador Rebombeo 1', 'Estado del Arrancador Rebombeo 2', 'Alarma', '_timestamp_actualizacion'].includes(key)) {
                            const value = typeof estacion[key] === 'number'
                                ? estacion[key].toLocaleString('es-ES', { minimumFractionDigits: 2, maximumFractionDigits: 2 })
                                : estacion[key];
                            html += `<div class="var-row"><span class="var-label">${key}:</span><span class="var-value">${value}</span></div>`;
                        }
                    }
                });
                html += `<hr><div class="timestamp">📅 ${new Date().toLocaleString('es-ES')}</div></div>`;
                return html;
            }
            function agruparEstacionesPorNombre(estaciones) {
                const grupos = new Map();
                estaciones.forEach(estacion => {
                    const nombre = estacion.nombre || `${estacion.latitud},${estacion.longitud}`;
                    if (!grupos.has(nombre)) {
                        grupos.set(nombre, []);
                    }
                    grupos.get(nombre).push(estacion);
                });
                return grupos;
            }
            function actualizarEstadisticas(datos) {
                if (!datos || !datos.estaciones) return;
                let total = 0, pozos_encendidos = 0, pozos_apagados = 0, tanques = 0;
                let bombas_encendidas = 0, bombas_apagadas = 0, rebombeos_encendidos = 0, rebombeos_apagados = 0;
                let sensores = 0, offline_count = 0, online = 0;
                datos.estaciones.forEach(estacion => {
                    total++;
                    const offline = esOffline(estacion.en_linea);
                    const tipo = estacion.tipo || 'generico';
                    if (offline) {
                        offline_count++;
                    } else {
                        online++;
                        if (tipo === 'pozo') {
                            const estado = obtenerEstadoArrancador(estacion, tipo);
                            if (estado === "Encendido") pozos_encendidos++; else pozos_apagados++;
                        } else if (tipo === 'tanque') {
                            tanques++;
                        } else if (tipo === 'bomba') {
                            const estado = obtenerEstadoArrancador(estacion, tipo);
                            if (estado === "Encendido") bombas_encendidas++; else bombas_apagadas++;
                        } else if (tipo === 'rebombeo') {
                            const estado = obtenerEstadoArrancador(estacion, tipo);
                            if (estado === "Encendido") rebombeos_encendidos++; else rebombeos_apagados++;
                        } else if (tipo === 'sensor') {
                            sensores++;
                        }
                    }
                });
                const tipos = datos.tipos || {};
                const stats = [
                    { tipo: 'total', value: total, label: 'Total' },
                    { tipo: 'pozo', estado: 1, value: pozos_encendidos, label: 'Pozos Enc.' },
                    { tipo: 'pozo', estado: 0, value: pozos_apagados, label: 'Pozos Apag.' },
                    { tipo: 'tanque', value: tanques, label: 'Tanques' },
                    { tipo: 'bomba', estado: 1, value: bombas_encendidas, label: 'Bombas Enc.' },
                    { tipo: 'bomba', estado: 0, value: bombas_apagadas, label: 'Bombas Apag.' },
                    { tipo: 'rebombeo', estado: 1, value: rebombeos_encendidos, label: 'Rebom. Enc.' },
                    { tipo: 'rebombeo', estado: 0, value: rebombeos_apagados, label: 'Rebom. Apag.' },
                    { tipo: 'sensor', value: sensores, label: 'Sensores Río' },
                    { tipo: 'offline', value: offline_count, label: 'Offline' },
                    { tipo: 'online', value: online, label: 'Online' },
                    { tipo: 'reloj', value: '""" + tiempo_str + """', label: 'Actualizado' }
                ];
                const statsBar = document.getElementById('stats-bar');
                if (!statsBar) return;
                statsBar.innerHTML = '';
                stats.forEach(stat => {
                    if (stat.value === 0 && !['total', 'online', 'offline', 'reloj'].includes(stat.tipo)) return;
                    const config = tipos[stat.tipo] || tipos['generico'] || {};
                    let iconoUrl = null;
                    if (stat.tipo === 'pozo' || stat.tipo === 'bomba' || stat.tipo === 'rebombeo') {
                        iconoUrl = stat.estado === 1 ? (limpiarUrl(config.icono_url_on) || limpiarUrl(config.icono_url)) : (limpiarUrl(config.icono_url_off) || limpiarUrl(config.icono_url));
                    } else if (stat.tipo === 'offline') {
                        iconoUrl = 'https://raw.githubusercontent.com/AlarmasCiateq/SCADA_T/main/iconos/Offline.svg';
                    } else if (stat.tipo === 'online') {
                        iconoUrl = 'https://raw.githubusercontent.com/AlarmasCiateq/SCADA_T/main/iconos/Online_Alarma.svg';
                    } else if (stat.tipo === 'total') {
                        iconoUrl = 'https://raw.githubusercontent.com/AlarmasCiateq/SCADA_T/main/iconos/transmite.svg';
                    } else if (stat.tipo === 'reloj') {
                        iconoUrl = 'https://raw.githubusercontent.com/AlarmasCiateq/SCADA_T/main/iconos/update.svg';
                    } else {
                        iconoUrl = limpiarUrl(config.icono_url);
                    }
                    const item = document.createElement('div');
                    item.className = 'stat-item';
                    let iconHtml = iconoUrl
                        ? `<div class="stat-icon"><img src="${iconoUrl}" alt="${stat.tipo}"></div>`
                        : `<div class="stat-icon" style="color:${config.color || '#7f8c8d'};font-size:20px;">⬤</div>`;
                    item.innerHTML = iconHtml + '<div class="stat-value">' + stat.value + '</div>' + '<div class="stat-label">' + stat.label + '</div>';
                    statsBar.appendChild(item);
                });
            }
            function zoomATodosLosIconos() {
                if (!map || markers.size === 0) return;
                const todasCoords = Array.from(markers.values()).map(m => m.getLatLng());
                map.fitBounds(todasCoords, { padding: [40, 40] });
                try {
                    localStorage.setItem('scada_map_zoom', map.getZoom().toString());
                    localStorage.setItem('scada_map_center', JSON.stringify({lat: map.getCenter().lat, lng: map.getCenter().lng}));
                } catch(e) {}
            }
            L.Control.ZoomAll = L.Control.extend({
                options: { position: 'topleft' },
                onAdd: function(mapInstance) {
                    const container = L.DomUtil.create('div', 'leaflet-bar leaflet-control leaflet-control-zoom-all');
                    const button = L.DomUtil.create('a', 'leaflet-control-zoom-all', container);
                    button.href = '#';
                    button.title = 'Ver todas las estaciones';
                    button.innerHTML = '<i>⌂</i>';
                    L.DomEvent.disableClickPropagation(button);
                    L.DomEvent.on(button, 'click', function(e) {
                        L.DomEvent.stopPropagation(e);
                        L.DomEvent.preventDefault(e);
                        zoomATodosLosIconos();
                    });
                    return container;
                }
            });
            L.control.zoomAll = function(opts) { return new L.Control.ZoomAll(opts); };
            function initMap() {
                try {
                    map = L.map('map', { zoomControl: true, scrollWheelZoom: true, dragging: true });
                    <!--L.tileLayer('https://{s}.basemaps.cartocdn.com/light_all/{z}/{x}/{y}{r}.png', { -->
                    <!-    attribution: '', subdomains: 'abcd', maxZoom: 19 -->
                    <!-}).addTo(map);-->
                    L.tileLayer(
                        'https://server.arcgisonline.com/ArcGIS/rest/services/World_Topo_Map/MapServer/tile/{z}/{y}/{x}',
                        {
                            attribution: 'Tiles © Esri',
                            maxZoom: 19
                        }
                    ).addTo(map);
                    L.control.zoomAll().addTo(map);
                    const todasCoords = [];
                    DATOS_INICIALES.estaciones.forEach(est => {
                        if (est.latitud && est.longitud) todasCoords.push([parseFloat(est.latitud), parseFloat(est.longitud)]);
                    });
                    const savedZoom = localStorage.getItem('scada_map_zoom');
                    const savedCenter = localStorage.getItem('scada_map_center');
                    const wasInitialized = localStorage.getItem('scada_map_initialized') === 'true';
                    if (wasInitialized && savedZoom && savedCenter) {
                        try {
                            const center = JSON.parse(savedCenter);
                            map.setView([center.lat, center.lng], parseInt(savedZoom));
                        } catch(e) {
                            if (todasCoords.length > 0) map.fitBounds(L.latLngBounds(todasCoords), { padding: [40, 40] });
                        }
                    } else {
                        if (todasCoords.length > 0) {
                            map.fitBounds(L.latLngBounds(todasCoords), { padding: [40, 40] });
                            localStorage.setItem('scada_map_initialized', 'true');
                        }
                    }
                    const gruposEstaciones = agruparEstacionesPorNombre(DATOS_INICIALES.estaciones);
                    gruposEstaciones.forEach((estaciones, nombre) => {
                        if (estaciones.length === 0) return;
                        const primeraEstacion = estaciones[0];
                        if (!primeraEstacion.latitud || !primeraEstacion.longitud) return;
                        const lat = parseFloat(primeraEstacion.latitud);
                        const lng = parseFloat(primeraEstacion.longitud);
                        let icono = estaciones.length > 1 ? crearIconoCompuesto(estaciones) : crearIconoSimple(estaciones[0]);
                        const marker = L.marker([lat, lng], { icon: icono })
                            .bindPopup(crearPopupContent(estaciones), { maxWidth: 360 })
                            .addTo(map);
                        markers.set(nombre, marker);
                    });
                    actualizarEstadisticas(DATOS_INICIALES);
                    document.getElementById('loading').classList.add('hidden');
                    window.map = map;
                } catch(e) {
                    document.getElementById('loading').innerHTML = `<div style="color:#e74c3c;text-align:center;padding:20px;">❌ Error: ${e.message}</div>`;
                    console.error('Error:', e);
                }
            }
            if (document.readyState === 'loading') {
                document.addEventListener('DOMContentLoaded', initMap);
            } else {
                initMap();
            }
        })();
    </script>
</body>
</html>
"""

st.components.v1.html(
    html_completo,
    width=1920,
    height=1000,
    scrolling=False
)
time.sleep(60)
st.rerun()
