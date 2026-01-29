import streamlit as st
import folium
import requests
import json
from datetime import datetime
import hashlib

# Configuración minimalista
st.set_page_config(
    page_title="SCADA Monitor",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# CSS limpio - solo para el botón de actualización
st.markdown("""
    <style>
    [data-testid="stSidebar"] { display: none; }
    [data-testid="stHeader"] { display: none; }
    .block-container { padding: 0; max-width: 100%; margin: 0; }
    .stApp { background-color: #0e1117; }
    
    /* Botón de actualización discreto */
    #update-btn {
        position: fixed;
        top: 10px;
        left: 10px;
        z-index: 1000;
        background: rgba(52, 152, 219, 0.9);
        color: white;
        border: none;
        width: 40px;
        height: 40px;
        border-radius: 20px;
        font-size: 18px;
        cursor: pointer;
        box-shadow: 0 2px 10px rgba(0,0,0,0.3);
    }
    #update-btn:hover {
        background: rgba(41, 128, 185, 0.95);
    }
    </style>
    """, unsafe_allow_html=True)

# Cargar datos SIN cache
def cargar_datos():
    try:
        url = "https://raw.githubusercontent.com/AlarmasCiateq/SCADA_T/main/datos_estaciones.json"
        response = requests.get(f"{url}?t={int(datetime.now().timestamp()*1000)}", timeout=5)
        response.raise_for_status()
        return response.json()
    except:
        return None

# Crear icono (mismo ícono, color según estado)
def crear_icono(tipo, estado, en_linea):
    color = 'black' if en_linea == 0 else (
        'green' if (tipo in ['pozo', 'bomba'] and estado == 1) else
        'red' if (tipo in ['pozo', 'bomba'] and estado == 0) else
        'blue' if (tipo == 'tanque' and estado == 1) else
        'gray' if tipo == 'tanque' else
        'purple' if tipo == 'sensor' else
        'orange'
    )
    
    iconos = {
        'pozo': ('tint', 'fa'),
        'tanque': ('water', 'fa'),
        'bomba': ('cog', 'fa'),
        'sensor': ('microchip', 'fa')
    }
    icon, prefix = iconos.get(tipo, ('info-sign', 'glyphicon'))
    return folium.Icon(icon=icon, prefix=prefix, color=color, icon_color='white')

# Generar HTML del mapa COMPLETO (estático)
def generar_html_mapa(datos):
    if not datos or 'estaciones' not in datos:
        return None, {}
    
    # Calcular bounds
    bounds = []
    for e in datos['estaciones']:
        if 'latitud' in e and 'longitud' in e:
            bounds.append([e['latitud'], e['longitud']])
    
    if not bounds:
        return None, {}
    
    # Centro
    centro = [sum(b[0] for b in bounds)/len(bounds), sum(b[1] for b in bounds)/len(bounds)]
    
    # Mapa
    mapa = folium.Map(
        location=centro,
        zoom_start=10,
        tiles='CartoDB positron',
        control_scale=False,
        prefer_canvas=True,
        zoom_control=True,
        scrollWheelZoom=True
    )
    
    # Estadísticas
    stats = {'total':0, 'activos':0, 'inactivos':0, 'tanques':0, 'offline':0}
    
    # Marcadores
    for e in datos['estaciones']:
        if 'latitud' not in e or 'longitud' not in e:
            continue
        
        stats['total'] += 1
        en_linea = e.get('en_linea', 1)
        tipo = e.get('tipo', 'otro')
        estado = e.get('estado_bomba', e.get('estado', 0))
        
        if en_linea == 0:
            stats['offline'] += 1
        elif tipo == 'pozo':
            stats['activos' if estado == 1 else 'inactivos'] += 1
        elif tipo == 'tanque':
            stats['tanques'] += 1
        
        # Popup HTML limpio
        popup_html = f"""
        <div style="font-family: Arial, sans-serif; padding: 12px; min-width: 280px; background: white; border-radius: 6px;">
            <h4 style="margin: 0 0 10px 0; color: #2c3e50;">{e.get('nombre', 'Estación')}</h4>
            <hr style="margin: 8px 0; border-color: #ecf0f1;">
        """
        for k, v in e.items():
            if k not in ['nombre', 'latitud', 'longitud', 'tipo', 'estado_bomba', 'en_linea', 'icono']:
                val = f"{v:,.2f}" if isinstance(v, (float, int)) else str(v)
                popup_html += f"""
                <div style="margin: 6px 0; padding: 4px 0; display: flex; justify-content: space-between;">
                    <span style="color: #7f8c8d; font-size: 13px;">{k}:</span>
                    <span style="font-weight: bold; color: #2c3e50;">{val}</span>
                </div>
                """
        popup_html += f"""
            <hr style="margin: 8px 0; border-color: #ecf0f1;">
            <div style="font-size: 11px; color: #95a5a6; text-align: center;">
                📅 {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
            </div>
        </div>
        """
        
        folium.Marker(
            location=[e['latitud'], e['longitud']],
            popup=folium.Popup(popup_html, max_width=320),
            tooltip=e.get('nombre', ''),
            icon=crear_icono(tipo, estado, en_linea)
        ).add_to(mapa)
    
    # Ajustar zoom para todas las estaciones
    mapa.fit_bounds(bounds, padding=(40, 40))
    
    # Estadísticas como control HTML dentro del mapa
    stats_html = f"""
    <div style="
        position: fixed;
        top: 10px;
        right: 15px;
        background: rgba(255, 255, 255, 0.92);
        padding: 8px 15px;
        border-radius: 8px;
        box-shadow: 0 2px 10px rgba(0,0,0,0.15);
        font-family: Arial, sans-serif;
        font-size: 13px;
        z-index: 1000;
        display: grid;
        grid-template-columns: repeat(6, auto);
        gap: 12px;
        align-items: center;
    ">
        <div><div style="font-weight:bold;color:#2c3e50">📡 {stats['total']}</div><div style="font-size:9px;color:#7f8c8d">Total</div></div>
        <div><div style="font-weight:bold;color:#27ae60">🟢 {stats['activos']}</div><div style="font-size:9px;color:#7f8c8d">Activos</div></div>
        <div><div style="font-weight:bold;color:#e74c3c">🔴 {stats['inactivos']}</div><div style="font-size:9px;color:#7f8c8d">Inactivos</div></div>
        <div><div style="font-weight:bold;color:#3498db">🔵 {stats['tanques']}</div><div style="font-size:9px;color:#7f8c8d">Tanques</div></div>
        <div><div style="font-weight:bold;color:#000">⚫ {stats['offline']}</div><div style="font-size:9px;color:#7f8c8d">Offline</div></div>
        <div><div style="font-weight:bold;color:#2c3e50">🕐 {datetime.now().strftime('%H:%M')}</div><div style="font-size:9px;color:#7f8c8d">Actualizado</div></div>
    </div>
    """
    
    mapa.get_root().html.add_child(folium.Element(stats_html))
    
    return mapa._repr_html_(), stats

# Interfaz principal
def main():
    # Botón de actualización (fuera del mapa)
    st.markdown('<button id="update-btn" onclick="window.location.reload();">🔄</button>', unsafe_allow_html=True)
    
    # Cargar datos
    datos = cargar_datos()
    if not datos:
        st.error("⚠️ No se pudieron cargar los datos. Verifica el archivo en GitHub.")
        st.stop()
    
    # Generar HTML del mapa
    html_mapa, stats = generar_html_mapa(datos)
    if not html_mapa:
        st.error("⚠️ No hay coordenadas válidas en los datos.")
        st.stop()
    
    # Mostrar mapa HTML estático (NO se rerenderiza al interactuar)
    st.components.v1.html(
        html_mapa,
        width=1920,
        height=1080,
        scrolling=False
    )

if __name__ == "__main__":
    main()
