import streamlit as st
import folium
from folium.plugins import MarkerCluster
import requests
import json
import time
from datetime import datetime
import pandas as pd
from streamlit_folium import folium_static

# Configuración de la página
st.set_page_config(
    page_title="Monitoreo de Estaciones",
    page_icon="🛢️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Función para cargar datos desde GitHub
@st.cache_data(ttl=300)  # Cache por 5 minutos
def cargar_datos_github(url_github):
    try:
        response = requests.get(url_github)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        st.error(f"Error al cargar datos: {e}")
        return None

# Función para crear iconos según el estado
def crear_icono(tipo, estado):
    if tipo == "pozo":
        if estado == 1:  # Encendido
            return folium.Icon(icon='water-pump', prefix='fa', color='green', icon_color='white')
        else:  # Apagado
            return folium.Icon(icon='water-pump', prefix='fa', color='red', icon_color='white')
    elif tipo == "tanque":
        if estado == 1:
            return folium.Icon(icon='tint', prefix='fa', color='blue', icon_color='white')
        else:
            return folium.Icon(icon='tint', prefix='fa', color='gray', icon_color='white')
    else:
        return folium.Icon(icon='info-sign', prefix='glyphicon', color='orange')

# Función para crear tooltip con información detallada
def crear_tooltip(estacion):
    tooltip_html = f"""
    <div style="font-family: Arial, sans-serif; padding: 10px; min-width: 250px;">
        <h4 style="color: #1f77b4; margin-bottom: 10px;">{estacion.get('nombre', 'Estación')}</h4>
        <hr style="border: 1px solid #ddd; margin: 8px 0;">
        <table style="width: 100%; font-size: 12px;">
    """
    
    # Agregar variables al tooltip
    for key, value in estacion.items():
        if key not in ['nombre', 'latitud', 'longitud', 'tipo', 'icono']:
            tooltip_html += f"""
            <tr>
                <td style="padding: 4px; font-weight: bold;">{key}:</td>
                <td style="padding: 4px; text-align: right;">{value}</td>
            </tr>
            """
    
    # Agregar fecha y hora de actualización
    tooltip_html += f"""
            <tr>
                <td style="padding: 4px; font-weight: bold;">Última actualización:</td>
                <td style="padding: 4px; text-align: right;">{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</td>
            </tr>
        </table>
    </div>
    """
    
    return folium.Tooltip(tooltip_html, sticky=True)

# Función principal para crear el mapa
def crear_mapa(datos):
    if not datos or 'estaciones' not in datos:
        st.warning("No hay datos disponibles")
        return None
    
    # Calcular centro del mapa
    latitudes = [est['latitud'] for est in datos['estaciones']]
    longitudes = [est['longitud'] for est in datos['estaciones']]
    centro_mapa = [sum(latitudes)/len(latitudes), sum(longitudes)/len(longitudes)]
    
    # Crear mapa
    mapa = folium.Map(
        location=centro_mapa,
        zoom_start=12,
        tiles='OpenStreetMap',
        control_scale=True
    )
    
    # Agregar cluster de marcadores
    marker_cluster = MarkerCluster().add_to(mapa)
    
    # Agregar marcadores para cada estación
    for estacion in datos['estaciones']:
        try:
            # Obtener datos de la estación
            nombre = estacion.get('nombre', 'Estación sin nombre')
            lat = estacion.get('latitud')
            lon = estacion.get('longitud')
            tipo = estacion.get('tipo', 'otro')
            estado = estacion.get('estado_bomba', 0)  # 1 = encendido, 0 = apagado
            
            if lat is None or lon is None:
                continue
            
            # Crear marcador con icono y tooltip
            icono = crear_icono(tipo, estado)
            tooltip = crear_tooltip(estacion)
            
            folium.Marker(
                location=[lat, lon],
                popup=nombre,
                tooltip=tooltip,
                icon=icono
            ).add_to(marker_cluster)
            
        except Exception as e:
            st.warning(f"Error al procesar estación {estacion.get('nombre', 'Desconocida')}: {e}")
    
    # Agregar leyenda
    leyenda_html = '''
    <div style="position: fixed; 
                bottom: 50px; right: 50px; 
                background-color: white; 
                padding: 15px; 
                border-radius: 5px;
                box-shadow: 0 0 10px rgba(0,0,0,0.2);
                z-index: 9999;">
        <h4 style="margin: 0 0 10px 0;">Leyenda</h4>
        <div style="display: flex; align-items: center; margin: 5px 0;">
            <i class="fa fa-water-pump" style="color: green; font-size: 20px; margin-right: 10px;"></i>
            <span>Pozo Encendido</span>
        </div>
        <div style="display: flex; align-items: center; margin: 5px 0;">
            <i class="fa fa-water-pump" style="color: red; font-size: 20px; margin-right: 10px;"></i>
            <span>Pozo Apagado</span>
        </div>
        <div style="display: flex; align-items: center; margin: 5px 0;">
            <i class="fa fa-tint" style="color: blue; font-size: 20px; margin-right: 10px;"></i>
            <span>Tanque Lleno</span>
        </div>
        <div style="display: flex; align-items: center; margin: 5px 0;">
            <i class="fa fa-tint" style="color: gray; font-size: 20px; margin-right: 10px;"></i>
            <span>Tanque Vacío</span>
        </div>
    </div>
    '''
    
    mapa.get_root().html.add_child(folium.Element(leyenda_html))
    
    return mapa

# Interfaz principal
def main():
    st.title("🛢️ Sistema de Monitoreo de Estaciones")
    
    # Sidebar para configuración
    with st.sidebar:
        st.header("⚙️ Configuración")
        
        # URL del archivo JSON en GitHub
        url_default = "https://raw.githubusercontent.com/tu-usuario/tu-repo/main/datos_estaciones.json"
        url_github = st.text_input(
            "URL del archivo JSON en GitHub:",
            value=url_default,
            help="Pega la URL raw de tu archivo JSON en GitHub"
        )
        
        # Opciones de visualización
        st.subheader("📊 Opciones")
        mostrar_datos = st.checkbox("Mostrar datos en tabla", value=True)
        auto_actualizar = st.checkbox("Auto-actualizar cada 5 minutos", value=True)
        
        # Botón de actualización manual
        if st.button("🔄 Actualizar ahora"):
            st.cache_data.clear()
            st.rerun()
    
    # Cargar datos
    with st.spinner("Cargando datos..."):
        datos = cargar_datos_github(url_github)
    
    if datos:
        # Mostrar información general
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Total de Estaciones", len(datos.get('estaciones', [])))
        with col2:
            pozos_activos = sum(1 for e in datos['estaciones'] if e.get('tipo') == 'pozo' and e.get('estado_bomba') == 1)
            st.metric("Pozos Activos", pozos_activos)
        with col3:
            ultima_actualizacion = datetime.now().strftime("%H:%M:%S")
            st.metric("Última Actualización", ultima_actualizacion)
        
        # Crear y mostrar mapa
        mapa = crear_mapa(datos)
        
        if mapa:
            # Mostrar mapa
            folium_static(mapa, width=1200, height=600)
            
            # Mostrar datos en tabla si se selecciona
            if mostrar_datos:
                st.subheader("📋 Datos de Estaciones")
                
                # Convertir datos a DataFrame
                df_data = []
                for estacion in datos['estaciones']:
                    row = {
                        'Nombre': estacion.get('nombre', ''),
                        'Tipo': estacion.get('tipo', ''),
                        'Estado': '🟢 Activo' if estacion.get('estado_bomba', 0) == 1 else '🔴 Inactivo',
                        'Latitud': estacion.get('latitud', ''),
                        'Longitud': estacion.get('longitud', ''),
                    }
                    
                    # Agregar otras variables
                    for key, value in estacion.items():
                        if key not in ['nombre', 'tipo', 'estado_bomba', 'latitud', 'longitud', 'icono']:
                            row[key] = value
                    
                    df_data.append(row)
                
                df = pd.DataFrame(df_data)
                st.dataframe(df, use_container_width=True)
        
        # Auto-actualización
        if auto_actualizar:
            st.info("🔄 Auto-actualización activada - La página se actualizará en 5 minutos")
            time.sleep(300)  # 5 minutos
            st.cache_data.clear()
            st.rerun()
    else:
        st.error("❌ No se pudieron cargar los datos. Verifica la URL y el formato del archivo JSON.")

# Ejecutar aplicación
if __name__ == "__main__":
    main()
