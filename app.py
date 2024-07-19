import streamlit as st
import requests

# Título de la aplicación
st.title('Get tracking link')

# Entrada para el token
token = st.text_input('Introduce el Token')

# Entrada para el claim ID
claim_id = st.text_input('Introduce el Claim ID')

# Botón para ejecutar la solicitud
if st.button('Obtener Sharing Link'):
    if not token or not claim_id:
        st.error("Por favor, introduce el Token y el Claim ID")
    else:
        # URL de la API
        url = f'https://b2b.taxi.yandex.net/b2b/cargo/integration/v2/claims/performer-position?claim_id={claim_id}'
        
        # Encabezados
        headers = {
            'Authorization': f'Bearer {token}'
        }
        
        # Realizar la solicitud
        response = requests.get(url, headers=headers)
        
        if response.status_code == 200:
            data = response.json()
            # Buscar el enlace de "sharing_link"
            sharing_link = None
            for point in data.get('route_points', []):
                if point.get('type') == 'destination' and 'sharing_link' in point:
                    sharing_link = point['sharing_link']
                    break
            
            if sharing_link:
                st.success(f'Sharing Link: {sharing_link}')
                st.write(f'[Link]({sharing_link})')
            else:
                st.error('No se encontró el "sharing_link" en la respuesta.')
        else:
            st.error(f'Error en la solicitud: {response.status_code}')
