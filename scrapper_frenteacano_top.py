import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from datetime import datetime
import pytz
from win10toast import ToastNotifier  # Importa la biblioteca para mostrar notificaciones
import time

# Configurar el navegador
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-gpu')
chrome_options.add_argument('--disable-dev-shm-usage')

# Inicializar el navegador
driver = webdriver.Chrome(options=chrome_options)

# Obtener la página de noticias más leídas
url = "https://frenteacano.com.ar/"
driver.get(url)

# Esperar a que los elementos estén presentes en la página
wait = WebDriverWait(driver, 10)
mas_leidas_div = wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'widget-masleidas')))

# Obtener los enlaces y títulos de las noticias más leídas
links = []
titulos = []

# Buscar los elementos de las noticias más leídas dentro de la clase "widget-masleidas"
titulos_div = mas_leidas_div.find_elements(By.CLASS_NAME, 'noticia__titular')
for titulo_div in titulos_div:
    # Extraer el enlace y el título de la noticia
    link_element = titulo_div.find_element(By.TAG_NAME, 'a')
    link = link_element.get_attribute('href')
    titulo = link_element.text.strip()
    
    # Agregar el enlace y el título a las listas
    links.append(link)
    titulos.append(titulo)

# Cerrar el navegador
driver.quit()

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
nombre_archivo = "frenteacano_top/scrap_top_frenteacano_" + datetime.now().strftime("%Y-%m-%d_%H-%M-%S") + ".parquet"
df.to_parquet(nombre_archivo)

# Mostrar el DataFrame resultante
print("DataFrame guardado como:", nombre_archivo)

# Función para enviar la notificación
def enviar_notificacion():
    toaster = ToastNotifier()
    toaster.show_toast("Ejecución del Scraper", "El código se ha ejecutado exitosamente.", duration=10)

# Llama a la función de enviar_notificacion para mostrar la notificación
enviar_notificacion()