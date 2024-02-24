import pandas as pd
from bs4 import BeautifulSoup
import requests
from datetime import datetime
import pytz
from win10toast import ToastNotifier  # Importa la biblioteca para mostrar notificaciones
import time


# Obtener la página de noticias más leídas
url = "https://www.labrujula24.com/"
response = requests.get(url)
soup = BeautifulSoup(response.text, 'html.parser')

# Encontrar los elementos de las noticias más leídas
mas_leidas_div = soup.find('div', id='mvp-post-more-wrap')

# Inicializar listas para almacenar los enlaces y títulos
links = []
titulos = []

# Buscar los elementos de las noticias más leídas
for noticia in mas_leidas_div.find_all('div', class_='mvp-post-more-text left relative'):
    # Extraer el enlace de la noticia
    link = noticia.find_previous('a')['href']
    links.append(link)
    
    # Extraer el texto de la noticia más leída
    texto_nota = noticia.text.strip()
    
    # Separar el texto utilizando "</span></div><p>" como separador y agregar un espacio
    separado = texto_nota.split("</span></div><p>")
    titulo = separado[-1].strip()  # El título será el último elemento después de la separación
    
    # Agregar un espacio antes de cada transición de minúscula a mayúscula
    titulo_con_espacios = ""
    for i in range(len(titulo) - 1):
        titulo_con_espacios += titulo[i]
        if titulo[i].islower() and titulo[i + 1].isupper():
            titulo_con_espacios += " "
    titulo_con_espacios += titulo[-1]  # Agregar el último carácter
    
    titulos.append(titulo_con_espacios)

# Convertir la hora local a la hora de Argentina
hora_argentina = datetime.now(pytz.timezone('America/Argentina/Buenos_Aires'))

# Obtener la fecha y hora de ejecución
fecha_hora_ejecucion = hora_argentina.strftime("%Y-%m-%d %H:%M:%S")

# Crear el DataFrame con los datos extraídos
df = pd.DataFrame({"link": links, "titulo": titulos})

# Agregar la fecha, hora de ejecución e índice
df["fecha"] = fecha_hora_ejecucion.split()[0]
df["hora_ejecucion"] = fecha_hora_ejecucion.split()[1]  # Extraer solo la hora
df["indice"] = range(1, len(df) + 1)

# Guardar el DataFrame como archivo Parquet
nombre_archivo = "labrujula_top/scrap_top_labrujula_" + datetime.now().strftime("%Y-%m-%d_%H-%M-%S") + ".parquet"
df.to_parquet(nombre_archivo)

# Mostrar el DataFrame resultante
print("DataFrame guardado como:", nombre_archivo)

# Función para enviar la notificación
def enviar_notificacion():
    toaster = ToastNotifier()
    toaster.show_toast("Ejecución del Scraper", "El código se ha ejecutado exitosamente.", duration=10)

# Llama a la función de enviar_notificacion para mostrar la notificación
enviar_notificacion()

