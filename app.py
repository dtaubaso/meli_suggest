from datetime import datetime
import requests, time, logging
import streamlit as st

# Configurar logging
logging.basicConfig(
    level=logging.INFO,  # Nivel mínimo para registrar
    format='%(asctime)s - %(levelname)s - %(message)s'  # Formato de los mensajes de log
)

year = datetime.now().strftime("%Y")
meses = ["0", "enero", "febrero", "marzo", "abril", "mayo", "junio", "julio",
         "agosto", "septiembre", "octubre", "noviembre", "diciembre"]
mes = meses[int(datetime.now().strftime("%m"))]


pais_dict = {
    "Argentina": "MLA",
    "México": "MLM",
    "Perú": "MPE",
    "Chile": "MLC",
    "Paraguay": "MPY",
    "Panamá": "MPA",
    "Costa Rica": "MCR",
    "Bolivia": "MBO",
    "Honduras": "MHN",
    "Venezuela": "MLV",
    "Nicaragua": "MNI",
    "El Salvador": "MSV",
    "Ecuador": "MEC",
    "Brasil": "MLB",
    "Colombia": "MCO",
    "Uruguay": "MLU",
    "Guatemala": "MGT"
}

def get_suggestions(kw, id):

    letters = ['',year, mes, 'a','b','c','d','e','f','g','h',
            'i','j','k','l','m','n','o','p','k','r'
            ,'s','t','u','v','w','x','y','z',
            '1','2','3','4','5','6','7','8','9']

    suggested = []
    for letter in letters:
        query = f'{kw} {letter}'
        url = f"https://http2.mlstatic.com/resources/sites/{id}/autosuggest?api_version=2&q={query}"
        res = requests.get(url)
        t = [a['q'] for a in res.json()['suggested_queries']]
        if t:
            suggested.extend(t)
    return suggested

# Función para restablecer los campos de entrada
def reset_fields():
    st.session_state.keyword = ''
    st.session_state.pais = ''
    st.session_state.resultados = []
    st.session_state.search_performed = False
    st.rerun()  # Recargar la aplicación para actualizar la UI


# Inicializar los estados de los campos si no existen
if 'keyword' not in st.session_state:
    st.session_state.keyword = ''
if 'id' not in st.session_state:
    st.session_state.pais = ''
if 'resultados' not in st.session_state:
    st.session_state.resultados = []
if 'search_performed' not in st.session_state:
    st.session_state.search_performed = False


st.set_page_config(
    layout="centered",
    initial_sidebar_state="expanded",
    page_title="MeLi Suggest",
    page_icon="🔍️",
)
st.sidebar.empty()
st.title("MeLi Suggest 🔍")
st.session_state.keyword = st.text_input("Ingrese un término de búsqueda", st.session_state.keyword)
pais_opcion = st.selectbox("Seleccione un país:", list(pais_dict.keys()))
st.session_state.pais = pais_dict[pais_opcion]

st.write("")
try:
    if st.button("Buscar"):

            if st.session_state.keyword and st.session_state.pais:
                with st.spinner('Obteniendo sugerencias...'):
                    st.session_state.resultados = get_suggestions(st.session_state.keyword, st.session_state.pais)
                st.session_state.search_performed = True
            else:
                st.error("Complete todos los campos")
    if st.session_state.resultados:
        st.write("Resultados:")
        for i, resultado in enumerate(st.session_state.resultados):
            st.write(f"{i+1} - {resultado}")

    # Crear el contenido para el archivo de texto
        resultados_texto = "\n".join([res for res in st.session_state.resultados])
        
        kw_name = st.session_state.keyword.replace(" ", "_")
        # Botón para descargar el archivo de texto
        st.write("")
        st.download_button(
            label="Descargar resultados",
            data=resultados_texto,
            file_name= f'resultados_{kw_name}_{int(time.time())}.txt',  # Usar el timestamp Unix en el nombre del archivo
            mime='text/plain'
        )
    elif st.session_state.search_performed:
        st.write("No se encontraron resultados")
except Exception as e:
    st.error("Ocurrió un error")
    logging.error(f"Ocurrió un error: {e}")
    logging.exception("Detalle de la excepción:")


