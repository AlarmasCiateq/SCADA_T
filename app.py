import streamlit as st
import folium
import requests
import json
import time
from datetime import datetime
from streamlit_folium import st_folium

# Configuración de la página - SIN SIDEBAR
st.set_page_config(
    page_title="SCADA Monitor",
    page_icon="🛢️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# CSS para tema oscuro y pantalla completa
st.markdown("""
    <style>
    /* Eliminar sidebar */
    [data-testid="stSidebar"] {
        display: none;
    }
    
    /* Fondo oscuro */
    .stApp {
        background-color: #0e1117;
        color: #ffffff;
    }
    
    /* Ocultar botones de Streamlit */
    button[kind="header"] {
        display: none;
    }
    
    /* Header minimalista */
    .main-header {
        background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
        padding: 5px 20px;
        border-radius: 8px;
        margin-bottom: 10px;
        box-shadow: 0 2px 10px rgba(0, 0, 0, 0.5);
    }
    
    /* Estadísticas */
    .stats-container {
        background: rgba(26, 26, 46, 0.8);
        padding: 8px;
        border-radius: 6px;
        margin-bottom: 10px;
        border: 1px solid #2d3748;
    }
    
    /* Texto blanco */
    h1, h2, h3, h4, h5, h6, p, div, span, li, ul {
        color: #ffffff !important;
    }
    
    /* Ocultar footer de Streamlit */
    footer {
        display: none !important;
    }
    
    /* Contenedor del mapa */
    .map-container {
        margin-top: 5px;
    }
    </style>
    """, unsafe_allow_html=True)

# Función para cargar datos desde GitHub
@st.cache_data(ttl=300)  # Cache por 5 minutos
def cargar_datos_github(url_github):
    try:
        headers = {'User-Agent': 'Mozilla/5.0'}
        response = requests.get(url_github, headers=headers, timeout=10)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        return None
    except json.JSONDecodeError:
        return None

# Función para crear iconos según el estado
def crear_icono(tipo, estado):
    if tipo == "pozo":
        if estado == 1:  # Encendido
            return folium.Icon(icon='tint', prefix='fa', color='green', icon_color='white')
        else:  # Apagado
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

# Función para crear popup con información detallada
def crear_popup(estacion):
    popup_html = f"""
    <div style="font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; 
                padding: 15px; min-width: 320px; background: #1a1a2e; color: #ffffff;">
        <h3 style="color: #4da6ff; margin-top: 0; font-size: 18px;">
            <i class="fa fa-tint"></i> {estacion.get('nombre', 'Estación')}
        </h3>
        <hr style="border: 1px solid #2d3748; margin: 10px 0;">
    """
    
    # Agregar variables al popup
    for key, value in estacion.items():
        if key not in ['nombre', 'latitud', 'longitud', 'tipo', 'estado', 'estado_bomba', 'icono']:
            # Formatear valores numéricos
            if isinstance(value, (int, float)):
                formatted_value = f"{value:,.2f}"
            else:
                formatted_value = str(value)
            
            popup_html += f"""
            <div style="margin: 8px 0; padding: 5px; background: rgba(45, 55, 72, 0.3); 
                        border-radius: 4px; border-left: 3px solid #4da6ff;">
                <strong style="color: #a0aec0; font-size: 13px;">{key}:</strong> 
                <span style="color: #ffffff; font-weight: 500; float: right;">
                    {formatted_value}
                </span>
                <div style="clear: both;"></div>
            </div>
            """
    
    # Agregar fecha y hora de actualización
    popup_html += f"""
        <hr style="border: 1px solid #2d3748; margin: 10px 0;">
        <div style="font-size: 11px; color: #718096; text-align: center;">
            📅 Última actualización: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
        </div>
    </div>
    """
    
    return folium.Popup(popup_html, max_width=400)

# Función principal para crear el mapa
def crear_mapa(datos):
    if not datos or 'estaciones' not in datos:
        return None, {}
    
    # Calcular centro del mapa
    latitudes = []
    longitudes = []
    
    for estacion in datos['estaciones']:
        lat = estacion.get('latitud')
        lon = estacion.get('longitud')
        if lat is not None and lon is not None:
            latitudes.append(lat)
            longitudes.append(lon)
    
    if not latitudes or not longitudes:
        return None, {}
    
    centro_mapa = [sum(latitudes)/len(latitudes), sum(longitudes)/len(longitudes)]
    
    # Crear mapa con estilo minimalista (CartoDB dark_matter)
    mapa = folium.Map(
        location=centro_mapa,
        zoom_start=12,
        tiles='CartoDB dark_matter',  # Mapa oscuro minimalista
        control_scale=False,
        prefer_canvas=True,
        zoom_control=True,
        scrollWheelZoom=True,
        dragging=True
    )
    
    # Contadores para estadísticas
    stats = {
        'total': 0,
        'pozos_activos': 0,
        'pozos_inactivos': 0,
        'tanques': 0,
        'bombas_activas': 0
    }
    
    # Agregar marcadores individuales (SIN CLUSTER)
    for estacion in datos['estaciones']:
        try:
            nombre = estacion.get('nombre', 'Estación sin nombre')
            lat = estacion.get('latitud')
            lon = estacion.get('longitud')
            tipo = estacion.get('tipo', 'otro')
            estado = estacion.get('estado_bomba', estacion.get('estado', 0))
            
            if lat is None or lon is None:
                continue
            
            stats['total'] += 1
            
            # Actualizar estadísticas
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
            
            # Crear marcador con icono y popup
            icono = crear_icono(tipo, estado)
            popup = crear_popup(estacion)
            
            folium.Marker(
                location=[lat, lon],
                popup=popup,
                tooltip=f"📍 {nombre}",
                icon=icono
            ).add_to(mapa)
            
        except Exception as e:
            continue
    
    return mapa, stats

# Interfaz principal
def main():
    # Header minimalista (1% de la pantalla)
    st.markdown('<div class="main-header">', unsafe_allow_html=True)
    col1, col2, col3, col4, col5 = st.columns([2, 1, 1, 1, 1])
    
    with col1:
        st.markdown("### 🛢️ SCADA Monitor - Sistema de Monitoreo")
    
    # Cargar datos automáticamente (sin input del usuario)
    URL_GITHUB = "https://raw.githubusercontent.com/AlarmasCiateq/SCADA_T/main/datos_estaciones.json"
    datos = cargar_datos_github(URL_GITHUB)
    
    if datos:
        # Crear y mostrar mapa
        mapa, stats = crear_mapa(datos)
        
        if mapa:
            # Mostrar estadísticas minimalistas
            with st.container():
                st.markdown('<div class="stats-container">', unsafe_allow_html=True)
                col_a, col_b, col_c, col_d, col_e = st.columns(5)
                
                with col_a:
                    st.metric("📡 Estaciones", stats['total'])
                with col_b:
                    st.metric("🟢 Pozos Activos", stats['pozos_activos'])
                with col_c:
                    st.metric("🔴 Pozos Inactivos", stats['pozos_inactivos'])
                with col_d:
                    st.metric("🔵 Tanques", stats['tanques'])
                with col_e:
                    ultima_actualizacion = datetime.now().strftime("%H:%M:%S")
                    st.metric("🕐 Actualizado", ultima_actualizacion)
                
                st.markdown('</div>', unsafe_allow_html=True)
            
            # Mostrar mapa (99% de la pantalla)
            st.markdown('<div class="map-container">', unsafe_allow_html=True)
            st_folium(
                mapa, 
                width=1900,  # FullHD width
                height=950,  # FullHD height menos espacio para header
                returned_objects=[],
                key="mapa_scada"
            )
            st.markdown('</div>', unsafe_allow_html=True)
        
        # Auto-actualización silenciosa cada 5 minutos
        time.sleep(300)
        st.cache_data.clear()
        st.rerun()
    else:
        # Pantalla de carga/error minimalista
        st.markdown("""
            <div style="text-align: center; padding: 100px; background: rgba(26, 26, 46, 0.9);">
                <h1 style="color: #4da6ff; font-size: 48px;">🛢️ SCADA Monitor</h1>
                <p style="color: #a0aec0; font-size: 18px; margin-top: 20px;">
                    Cargando datos del sistema...
                </p>
                <div style="margin-top: 30px; color: #718096;">
                    ⏳ Esperando actualización desde SCADA
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        # Reintentar en 10 segundos
        time.sleep(10)
        st.cache_data.clear()
        st.rerun()

# Ejecutar aplicación
if __name__ == "__main__":
    main()
