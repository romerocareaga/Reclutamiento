import pandas as pd
from sklearn.tree import DecisionTreeClassifier
import streamlit as st

# Definir la URL del archivo Excel
file_url = 'https://github.com/romerocareaga/Reclutamiento/raw/24d92d5edfc0925001dddf2e192d41e2da920094/DB_Seguridad_1.xlsx'

# Cargar el archivo Excel en un DataFrame
@st.cache_data
def load_data(url):
    df = pd.read_excel(url)
    return df

df = load_data(file_url)

# Definir las variables independientes (características) y la variable objetivo
X = df[['Edad', 'dia_ult_trab', 'ult_trab_seg', 'years_seg', 'confianza', 'general']]
y = df['se_queda']

# Crear el modelo de árbol de decisión
model = DecisionTreeClassifier()

# Entrenar el modelo con los datos de entrenamiento
model.fit(X, y)

# Presentación
def imprimir_cuadro(texto):
    longitud = len(texto) + 4
    borde = '+' + '-' * longitud + '+'
    contenido = f"| {texto} |"
    
    st.text(borde)
    st.text(contenido)
    st.text(borde)

# Texto a imprimir en el cuadro
texto = "Solución con AI de pre-calificación de candidatos\n Elaborado por: Marketing A3\nVersión: 1.0"

# Llama a la función para imprimir el cuadro
imprimir_cuadro(texto)

# Solicitar al usuario que ingrese los datos a través de la interfaz de Streamlit
Nombre = st.text_input("Por favor, ingresa el nombre del candidato:")
Edad = st.number_input("Por favor, ingrese la edad:", min_value=0, max_value=120, step=1)
dia_ult_trab = st.number_input("Por favor, ingrese los días desde su último empleo:", min_value=0, step=1)
ult_trab_seg = st.radio("¿El último empleo fue en seguridad? 1=Sí, 0=No", (1, 0))
years_seg = st.number_input("Por favor, ingrese los años de experiencia:", min_value=0, step=1)
confianza = st.number_input("Por favor, ingrese el resultado del examen de confianza:", min_value=0, max_value=100, step=1)
general = st.number_input("Por favor, ingrese el resultado del examen general:", min_value=0, max_value=100, step=1)

# Crear un diccionario con los datos ingresados
datos = {
    "Edad": [Edad],
    "dia_ult_trab": [dia_ult_trab],
    "ult_trab_seg": [ult_trab_seg],
    "years_seg": [years_seg],
    "confianza": [confianza],
    "general": [general],
}

# Crear un DataFrame a partir del diccionario
df_cuestionario = pd.DataFrame(datos)

# Realizar predicciones en los datos ingresados
if st.button("Calcular"):
    prediccion = model.predict(df_cuestionario)

    # Verificar si el candidato tiene altas probabilidades de permanecer
    if prediccion == 1:
        st.text("+-----------------------------------------------------------------------------+")
        st.success(f"{Nombre}: tiene altas probabilidades de permanecer")
        st.text("+-----------------------------------------------------------------------------+")
    else:
        st.text("+-----------------------------------------------------------------------------+")
        st.error(f"{Nombre}: No es un buen candidato")
        st.text("+-----------------------------------------------------------------------------+")
