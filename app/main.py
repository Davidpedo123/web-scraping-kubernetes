import re
import requests
from bs4 import BeautifulSoup
from fastapi import FastAPI
import redis
import time
import json
import os
from config import redis_client



# Función principal para realizar scraping de datos de tarjetas gráficas.
def scrape_data():
    start_time = time.time()  # Registrar el tiempo de inicio para medir la ejecución.
    url = "https://versus.com/es/graphics-card"  # URL de la página a scrapear.
    redis_key = "grafica_data"  # Clave para almacenar los datos en Redis.

    # Intentar obtener los datos almacenados en caché en Redis.
    cached_data = redis_client.get(redis_key)

    if cached_data:
        # Si los datos están en Redis, calcular el tiempo y devolverlos.
        elapsed_time = time.time() - start_time
        print(f"Tiempo de recuperación desde Redis: {elapsed_time:.2f} segundos.")
        return json.loads(cached_data.decode("UTF-8"))

    else:
        # Si los datos no están en Redis, realizar el scraping.
        r = requests.get(url)  # Realizar la solicitud HTTP.
        graficas_data = []

        if r.status_code == 200:  # Verificar que la respuesta sea exitosa.
            html = BeautifulSoup(r.text, "html.parser")  # Parsear el contenido HTML.
            div_graficas = html.find_all('div', {'class': 'Item__item___3X46y'})  # Encontrar las tarjetas gráficas.

            for div_grafica in div_graficas:
                # Extraer el modelo de la tarjeta gráfica.
                titulo = div_grafica.find('p', {'class': 'Item__name___1fPgt'}).getText().strip()

                # Extraer el precio si está disponible.
                price_element = div_grafica.find('div', {'class': 'Item__price___3wrAA'})
                precio = None
                if price_element:
                    precio_text = price_element.text.strip()
                    precio_match = re.search(r'([\d.,]+)', precio_text)
                    if precio_match:
                        # Convertir el precio a un número flotante.
                        precio = float(precio_match.group(1).replace(',', '.'))

                # Extraer las especificaciones de TFLOPS y RAM utilizando expresiones regulares.
                card_props = div_grafica.find('ul', {'class': 'Item__cardProps___Hxy-F'})
                tflops = "No especificado"
                ram = "No especificado"
                if card_props:
                    props = card_props.find_all('li', {'class': 'cardProp'})
                    for prop in props:
                        prop_value = prop.find('div', {'class': 'Item__cardPropValue___39nXp'}).getText().strip()

                        # Buscar valores específicos de TFLOPS.
                        if re.search(r'\d+(\.\d+)?\s*TFLOPS', prop_value):
                            tflops = re.search(r'(\d+(\.\d+)?)\s*TFLOPS', prop_value).group(1)
                        # Buscar valores de RAM.
                        elif re.search(r'\d+\s*GB', prop_value):
                            ram = re.search(r'(\d+)\s*GB', prop_value).group(1)

                # Agregar los datos procesados a la lista.
                graficas_data.append({
                    'modelo': titulo,
                    'ram': ram,
                    'tflops': tflops,
                    'precio': precio
                })

            # Almacenar los datos en Redis con un tiempo de expiración de 1 hora.
            redis_client.set(redis_key, json.dumps(graficas_data), ex=3600)
            elapsed_time = time.time() - start_time
            print(f"Tiempo de scraping y almacenamiento en Redis: {elapsed_time:.2f} segundos.")
        return graficas_data

# Configuración básica de FastAPI.
app = FastAPI()

@app.get("/graficas")
async def get_graficas():
    """
    Endpoint para obtener datos de tarjetas gráficas.
    Si los datos están en Redis, se recuperan desde allí.
    Si no, se realiza el scraping en tiempo real.
    """
    data = scrape_data()
    return data

# Ejecución del servidor FastAPI.
if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host='0.0.0.0', port=8000)