import time
import io
import os
import win32clipboard
import win32con
import pandas as pd
from PIL import Image
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

def copiar_imagen_al_portapapeles(ruta_imagen):
    image = Image.open(ruta_imagen)
    output = io.BytesIO()
    image.convert("RGB").save(output, "BMP")
    data = output.getvalue()[14:]
    output.close()

    win32clipboard.OpenClipboard()
    win32clipboard.EmptyClipboard()
    win32clipboard.SetClipboardData(win32con.CF_DIB, data)
    win32clipboard.CloseClipboard()

def enviar_imagen_paste(campo_mensaje):
    campo_mensaje.send_keys(Keys.CONTROL, 'v')  # Ctrl+V para pegar la imagen
    time.sleep(4)  # Espera a que la imagen se pegue

def esperar_y_comprobar():
    start_time = time.time()
    while True:
        try:
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "div[contenteditable='true'][tabindex='3']"))
            )
            print("Campo de búsqueda encontrado, continuando...")
            break
        except Exception as e:
            elapsed_time = time.time() - start_time
            if elapsed_time > 120:  # 2 minutos en segundos
                print("No se encontró el campo de búsqueda en 2 minutos. Cerrando el programa...")
                driver.quit()
                exit()
            time.sleep(5)  # Esperar un poco antes de volver a comprobar

def enviar_mensaje(numero, ruta_carpeta_imagenes, texto):
    url = f'https://web.whatsapp.com/send?phone={numero}'
    driver.get(url)

    try:
        WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "div[contenteditable='true'][tabindex='10']"))
        )
        
        campo_mensaje = driver.find_element(By.CSS_SELECTOR, "div[contenteditable='true'][tabindex='10']")
        
        campo_mensaje.send_keys(texto)
        time.sleep(1)  # Esperar antes de agregar las imágenes
        
        for archivo in os.listdir(ruta_carpeta_imagenes):
            if archivo.lower().endswith(('.png', '.jpg', '.jpeg', '.gif')):  # Filtra solo imágenes
                ruta_imagen = os.path.join(ruta_carpeta_imagenes, archivo)
                print(f"Preparando imagen para enviar: {archivo}")
                
                copiar_imagen_al_portapapeles(ruta_imagen)
                enviar_imagen_paste(campo_mensaje)
                
                print(f"Imagen {archivo} añadida al chat.")

        send_button = driver.find_element(By.CSS_SELECTOR, 'span[data-icon="send"]')
        WebDriverWait(driver, 15).until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'span[data-icon="send"]')))
        send_button.click()
        print(f"Todas las imágenes y el mensaje enviados a {numero}")

    except Exception as e:
        print(f"Error al enviar mensaje a {numero}: {e}")

    finally:
        time.sleep(5)  # Esperar antes de pasar al siguiente número

def limpiar_numero(numero):
    # Limpiar y normalizar el número de teléfono
    return ''.join(filter(lambda x: x.isdigit() or x in "+()-", numero)).strip()

def leer_configuracion():
    with open('config.txt', 'r') as config_file:
        lineas = config_file.readlines()
        ruta_excel = lineas[0].strip()
        ruta_texto = lineas[1].strip()
        ruta_imagenes = lineas[2].strip()
    return ruta_excel, ruta_texto, ruta_imagenes

ruta_excel, ruta_texto, ruta_imagenes = leer_configuracion()

service = Service(executable_path=ChromeDriverManager().install())
options = Options()
driver = webdriver.Chrome(service=service, options=options)

driver.get('https://web.whatsapp.com')

esperar_y_comprobar()

df = pd.read_excel(ruta_excel, header=None)  # Leer el Excel sin encabezado
numeros = [limpiar_numero(str(numero)) for numero in df[0] if limpiar_numero(str(numero))]  # Limpiar y filtrar números

with open(ruta_texto, 'r', encoding='utf-8') as file:
    texto = file.read().strip()

for numero in numeros:
    enviar_mensaje(numero, ruta_imagenes, texto)

driver.quit()
