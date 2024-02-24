from win10toast import ToastNotifier  # Importa la biblioteca para mostrar notificaciones
import pandas as pd
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from datetime import datetime
import pytz

# Función para obtener la hora actual en Argentina
def obtener_hora_actual():
    # Obtener la zona horaria de Argentina
    tz = pytz.timezone('America/Argentina/Buenos_Aires')
    # Obtener la hora actual en Argentina
    hora_actual = datetime.now(tz)
    # Formatear la hora en formato de 12 horas sin minutos ni segundos
    hora_formateada = hora_actual.strftime("%I %p")
    return hora_formateada

# Configuración del navegador
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-gpu')
chrome_options.add_argument('--disable-dev-shm-usage')

# Inicializa el navegador
driver = webdriver.Chrome(options=chrome_options)

# URL de la página
url = "https://www.lanueva.com/"
driver.get(url)

# Espera a que la sección de noticias más leídas cargue completamente
try:
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "nota__contador")))
except:
    print("No se pudo cargar la sección de noticias más leídas.")

# Obtener todos los elementos nota__contador
try:
    elementos_contador = driver.find_elements(By.CLASS_NAME, "nota__contador")
except:
    print("No se encontraron elementos 'nota__contador'.")

# Inicializar listas para almacenar los títulos y los enlaces
titulos = []
enlaces = []

# Iterar sobre los elementos nota__contador
for contador in elementos_contador:
    print("Comenzando a procesar un contador")
    try:
        # Encontrar el siguiente elemento nota__body
        body = contador.find_element(By.XPATH, "./following-sibling::div[contains(@class, 'nota__body')]")
        
        # Ejecutar un script de JavaScript para encontrar todos los elementos nota__titulo-item dentro de nota__body
        titulos_items = body.find_elements(By.CLASS_NAME, "nota__titulo-item")
        
        # Obtener los títulos y los enlaces de cada título y agregarlos a las listas
        for titulo_item in titulos_items:
            enlace = titulo_item.find_element(By.TAG_NAME, "a").get_attribute("href")
            titulo = titulo_item.text.strip()
            titulos.append(titulo)
            enlaces.append(enlace)
        
        print(f"Títulos y enlaces encontrados: {titulos_items}")
    except Exception as e:
        print(f"Error al procesar el contador: {str(e)}")

    # Esperar un momento antes de pasar al siguiente contador
    time.sleep(2)

# Cerrar el navegador
driver.quit()

# Crear un DataFrame con los títulos y los enlaces
df = pd.DataFrame({
    "titulo": titulos,
    "link": enlaces
})

# Agregar la fecha actual y el índice
df["fecha"] = datetime.now().strftime("%Y-%m-%d")
df["hora_ejecucion"] = obtener_hora_actual()
df["indice"] = range(1, len(df) + 1)

# Agregar la columna 'categoria' según las condiciones especificadas
df["categoria"] = ["mas_leida" if i < 5 else "mas_comentada" for i in range(len(df))]

# Guardar el DataFrame como archivo Parquet
nombre_archivo = "lanueva_top/scrap_top_lanueva_" + datetime.now().strftime("%Y-%m-%d_%H-%M-%S") + ".parquet"
df.to_parquet(nombre_archivo)

# Mostrar el DataFrame resultante
print("DataFrame guardado como:", nombre_archivo)

# Función para enviar la notificación
def enviar_notificacion():
    toaster = ToastNotifier()
    toaster.show_toast("Ejecución del Scraper", "El código se ha ejecutado exitosamente.", duration=10)

# Llama a la función de enviar_notificacion para mostrar la notificación
enviar_notificacion()

