
import streamlit as st
import pymongo
from pymongo import MongoClient
import os
from dotenv import load_dotenv

# Cargar variables de entorno (para credenciales de MongoDB)
load_dotenv()

def connect_to_mongodb():
    """Conectar a MongoDB Atlas usando la cadena de conexión"""
    connection_string = os.getenv("MONGODB_CONNECTION_STRING")
    if not connection_string:
        st.error("Error: No se encontró la variable de entorno MONGODB_CONNECTION_STRING")
        return None

    try:
        client = MongoClient(connection_string)
        # Verificar la conexión
        client.admin.command('ping')
        return client
    except Exception as e:
        st.error(f"Error conectando a MongoDB Atlas: {e}")
        return None

def query_theaters_by_city(city_name):
    """Consultar teatros en la base de datos sample_mflix por nombre de ciudad"""
    try:
        # Conectar a MongoDB
        client = connect_to_mongodb()
        if not client:
            return None

        # Acceder a la base de datos sample_mflix
        db = client.sample_mflix

        # Acceder a la colección de teatros
        theaters_collection = db.theaters

        # Consultar teatros por ciudad
        query = {"location.address.city": city_name}
        theaters = list(theaters_collection.find(query).limit(5))

        # Obtener conteo total
        total_count = theaters_collection.count_documents(query)

        # Cerrar conexión
        client.close()

        return theaters, total_count

    except Exception as e:
        st.error(f"Error al consultar MongoDB: {e}")
        return None, 0

# Configuración de la página Streamlit
st.set_page_config(page_title="Buscador de Teatros", page_icon="🎭")
st.title("🎭 Buscador de Teatros por Ciudad")
st.write("Esta aplicación busca teatros en la base de datos sample_mflix de MongoDB por nombre de ciudad.")

# Campo de entrada para la ciudad
city_name = st.text_input("Nombre de la ciudad:", value="Chicago")

# Botón de búsqueda
if st.button("Buscar Teatros"):
    if city_name:
        with st.spinner(f"Buscando teatros en {city_name}..."):
            theaters, total_count = query_theaters_by_city(city_name)

            if theaters:
                st.success(f"Se encontraron {total_count} teatros en {city_name}")
                st.write(f"Mostrando los primeros 5 resultados:")

                for i, theater in enumerate(theaters, 1):
                    with st.expander(f"Teatro #{i}: {theater.get('location', {}).get('address', {}).get('street1', 'Sin dirección')}"):
                        st.write(f"**ID:** {theater.get('_id')}")
                        st.write(f"**Teatro ID:** {theater.get('theaterId')}")
                        st.write(f"**Dirección:** {theater.get('location', {}).get('address', {}).get('street1')}")
                        st.write(f"**Ciudad:** {theater.get('location', {}).get('address', {}).get('city')}")
                        st.write(f"**Estado:** {theater.get('location', {}).get('address', {}).get('state')}")
                        st.write(f"**Código postal:** {theater.get('location', {}).get('address', {}).get('zipcode')}")
            else:
                st.warning(f"No se encontraron teatros en {city_name} o hubo un error en la consulta.")
    else:
        st.warning("Por favor ingresa un nombre de ciudad.")

st.divider()
st.write("Nota: Esta aplicación requiere una conexión a MongoDB Atlas con acceso a la base de datos sample_mflix.")
