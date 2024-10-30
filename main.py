import re
import requests
from bs4 import BeautifulSoup
from fastapi import FastAPI
import redis
import time
import json
import os


HOST_REDIS = os.environ['HOST_REDIS']
PORT_REDIS = os.environ['PORT_REDIS']
PASSWD_REDIS = os.environ['PASSWD_REDIS']
redis_client = redis.StrictRedis(host=HOST_REDIS, port=PORT_REDIS, password=PASSWD_REDIS, db=0)


def scrape_data():
    start_time = time.time()
    url = "https://versus.com/es/graphics-card"
    
    # Construir una clave única para almacenar en Redis
    redis_key = "grafica_data"

    # Intentar obtener los datos de Redis
    cached_data = redis_client.get(redis_key)

    if cached_data:

        elapsed_time = time.time() - start_time
        print(elapsed_time)
        # Si los datos están en Redis, devolverlos convertidos de JSON
        return json.loads(cached_data.decode("UTF-8"))

    else:
    # Si no están en Redis, hacer el web scraping
        start_time = time.time()
        r = requests.get(url)
        graficas_data = []

        if r.status_code == 200:
            html = BeautifulSoup(r.text, "html.parser")
            div_graficas = html.find_all('div', {'class': 'Item__item___3X46y'})

            for div_grafica in div_graficas:
                titulo = div_grafica.find('p', {'class': 'Item__name___1fPgt'}).getText().strip()

                # Extracting price
                price_element = div_grafica.find('div', {'class': 'Item__price___3wrAA'})
                precio = None
                if price_element:
                    precio_text = price_element.text.strip()
                    precio_match = re.search(r'([\d.,]+)', precio_text)
                    if precio_match:
                        precio = float(precio_match.group(1).replace(',', '.'))

                # Extracting TFLOPS and RAM using regex
                card_props = div_grafica.find('ul', {'class': 'Item__cardProps___Hxy-F'})
                tflops = "No especificado"
                ram = "No especificado"
                if card_props:
                    props = card_props.find_all('li', {'class': 'cardProp'})
                    for prop in props:
                        prop_value = prop.find('div', {'class': 'Item__cardPropValue___39nXp'}).getText().strip()

                        # Using regex to match TFLOPS and RAM
                        if re.search(r'\d+(\.\d+)?\s*TFLOPS', prop_value):
                            tflops = re.search(r'(\d+(\.\d+)?)\s*TFLOPS', prop_value).group(1)
                        elif re.search(r'\d+\s*GB', prop_value):
                            ram = re.search(r'(\d+)\s*GB', prop_value).group(1)

                # Append the data to the list
                graficas_data.append({
                    'modelo': titulo,
                    'ram': ram,
                    'tflops': tflops,
                    'precio': precio
                })

            # Almacenar los datos en Redis para futuras consultas
            redis_client.set(redis_key, json.dumps(graficas_data), ex=3600)  # Almacena durante 1 hora (3600 segundos)
            elapsed_time = time.time() - start_time
        return graficas_data

# Test the function
#if __name__ == "__main__":
    #data = scrape_data()
    #for item in data:
        #print(item)


# Configuración básica de FastAPI
app = FastAPI()

@app.get("/graficas")
async def get_graficas():
    data = scrape_data()
    return data

# Ejecución del servidor FastAPI
if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host='0.0.0.0', port=8000)