import streamlit as st
import folium
from folium.plugins import MarkerCluster
import requests
import json
import time
from datetime import datetime
from streamlit_folium import st_folium

# Configuración de la página
st.set_page_config(
    page_title="Monitoreo de Estaciones",
    page_icon="🛢️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS personalizado
st.markdown("""
    <style>
    .stApp {
        background-color: #f0f2f6;
    }
    .metric-card {
        background-color: white;
        padding: 15px;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
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
        st.error(f"Error al cargar datos: {e}")
        return None
    except json.JSONDecodeError as e:
        st.error(f"Error en el formato JSON: {e}")
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
    else:
        return folium.Icon(icon='info-sign', prefix='glyphicon', color='orange')

# Función para crear popup con información detallada
def crear_popup(estacion):
    popup_html = f"""
    <div style="font-family: Arial, sans-serif; padding: 15px; min-width: 300px;">
        <h3 style="color: #1f77b4; margin-top: 0;">{estacion.get('nombre', 'Estación')}</h3>
        <hr style="border: 1px solid #ddd; margin: 10px 0;">
    """
    
    # Agregar variables al popup
    for key, value in estacion.items():
        if key not in ['nombre', 'latitud', 'longitud', 'tipo', 'estado', 'estado_bomba', 'icono']:
            popup_html += f"""
            <div style="margin: 8px 0;">
                <strong>{key}:</strong> {value}
            </div>
            """
    
    # Agregar fecha y hora de actualización
    popup_html += f"""
        <hr style="border: 1px solid #ddd; margin: 10px 0;">
        <div style="font-size: 11px; color: #666;">
            Última actualización: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
        </div>
    </div>
    """
    
    return folium.Popup(popup_html, max_width=400)

# Función principal para crear el mapa
def crear_mapa(datos):
    if not datos or 'estaciones' not in datos:
        st.warning("No hay datos disponibles")
        return None
    
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
        st.error("No se encontraron coordenadas válidas")
        return None
    
    centro_mapa = [sum(latitudes)/len(latitudes), sum(longitudes)/len(longitudes)]
    
    # Crear mapa
    mapa = folium.Map(
        location=centro_mapa,
        zoom_start=12,
        tiles='OpenStreetMap',
        control_scale=True,
        prefer_canvas=True
    )
    
    # Agregar cluster de marcadores
    marker_cluster = MarkerCluster(
        name='Estaciones',
        overlay=True,
        control=True,
        icon_create_function=None
    ).add_to(mapa)
    
    # Contadores para estadísticas
    stats = {
        'total': 0,
        'pozos_activos': 0,
        'pozos_inactivos': 0,
        'tanques': 0,
        'bombas_activas': 0
    }
    
    # Agregar marcadores para cada estación
    for estacion in datos['estaciones']:
        try:
            # Obtener datos de la estación
            nombre = estacion.get('nombre', 'Estación sin nombre')
            lat = estacion.get('latitud')
            lon = estacion.get('longitud')
            tipo = estacion.get('tipo', 'otro')
            estado = estacion.get('estado_bomba', estacion.get('estado', 0))
            
            if lat is None or lon is None:
                st.warning(f"Estación {nombre} sin coordenadas válidas")
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
                tooltip=nombre,
                icon=icono
            ).add_to(marker_cluster)
            
        except Exception as e:
            st.warning(f"Error al procesar estación {estacion.get('nombre', 'Desconocida')}: {e}")
    
    # Agregar control de capas
    folium.LayerControl().add_to(mapa)
    
    return mapa, stats

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
        auto_actualizar = st.checkbox("Auto-actualizar cada 5 minutos", value=True)
        
        # Botón de actualización manual
        if st.button("🔄 Actualizar ahora", type="primary"):
            st.cache_data.clear()
            st.rerun()
        
        st.markdown("---")
        st.markdown("**Instrucciones:**")
        st.markdown("1. Sube tu archivo JSON a GitHub")
        st.markdown("2. Copia la URL 'raw'")
        st.markdown("3. Pégala arriba")
        st.markdown("4. ¡Listo!")
    
    # Cargar datos
    with st.spinner("Cargando datos..."):
        datos = cargar_datos_github(url_github)
    
    if datos:
        # Crear y mostrar mapa
        resultado = crear_mapa(datos)
        
        if resultado:
            mapa, stats = resultado
            
            # Mostrar estadísticas
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.metric("Total Estaciones", stats['total'])
            with col2:
                st.metric("Pozos Activos", stats['pozos_activos'], 
                         delta=f"+{stats['pozos_activos']}" if stats['pozos_activos'] > 0 else None)
            with col3:
                st.metric("Tanques", stats['tanques'])
            with col4:
                ultima_actualizacion = datetime.now().strftime("%H:%M:%S")
                st.metric("Última Actualización", ultima_actualizacion)
            
            # Mostrar mapa
            st_folium(mapa, width=1200, height=600, returned_objects=[])
            
            # Mostrar datos en tabla
            with st.expander("📋 Ver datos detallados"):
                st.subheader("Datos de Estaciones")
                
                # Mostrar datos en formato de lista
                for idx, estacion in enumerate(datos['estaciones'], 1):
                    with st.container():
                        col_a, col_b = st.columns([2, 3])
                        
                        with col_a:
                            st.markdown(f"**{idx}. {estacion.get('nombre', 'Sin nombre')}**")
                            st.markdown(f"📍 {estacion.get('latitud', 'N/A')}, {estacion.get('longitud', 'N/A')}")
                            estado = estacion.get('estado_bomba', estacion.get('estado', 0))
                            estado_emoji = "🟢" if estado == 1 else "🔴"
                            st.markdown(f"{estado_emoji} {'Activo' if estado == 1 else 'Inactivo'}")
                        
                        with col_b:
                            for key, value in estacion.items():
                                if key not in ['nombre', 'latitud', 'longitud', 'tipo', 'estado', 'estado_bomba', 'icono']:
                                    st.text(f"{key}: {value}")
                        
                        st.markdown("---")
        
        # Auto-actualización
        if auto_actualizar:
            st.info(f"🔄 Auto-actualización activada - Próxima actualización en 5 minutos")
            
            # Crear un contador regresivo
            countdown_placeholder = st.empty()
            for i in range(300, 0, -1):
                countdown_placeholder.text(f"Próxima actualización en: {i//60}:{i%60:02d}")
                time.sleep(1)
            
            st.cache_data.clear()
            st.rerun()
    else:
        st.error("❌ No se pudieron cargar los datos. Verifica la URL y el formato del archivo JSON.")
        
        # Mostrar ejemplo de formato JSON
        with st.expander("📋 Formato JSON esperado"):
            st.code("""
{
  "estaciones": [
    {
      "nombre": "Estación Pozo 1",
      "tipo": "pozo",
      "estado_bomba": 1,
      "latitud": 19.283352119712312,
      "longitud": -99.65310428742922,
      "Presión": 2.5,
      "Flujo Instantáneo": 10.69,
      "Corriente Prom.": 126.40,
      "Voltaje Prom.": 429.25,
      "Potencia Activa": 23.14
    }
  ]
}
""", language="json")

# Ejecutar aplicación
if __name__ == "__main__":
    main()
