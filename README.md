# API para Web Scraping de Tarjetas Gráficas

Este proyecto despliega una API utilizando **FastAPI** en un clúster de **Kubernetes**. La API realiza **web scraping** para obtener información de tarjetas gráficas desde una página web conocida. Los datos obtenidos se almacenan temporalmente en **Redis** para mejorar el rendimiento, y el servicio está gestionado por un **proxy inverso Nginx**.

---

## Descripción de la lógica de la API

1. **Consulta de datos:**
   - La API accede a una página que contiene un catálogo extenso de tarjetas gráficas.
   - Si los datos solicitados no están en la caché de **Redis**, la API realiza **web scraping** utilizando la biblioteca **BeautifulSoup** para extraer la información necesaria.

2. **Caché con Redis:**
   - Los datos obtenidos se almacenan en Redis con una clave específica y un tiempo de expiración definido (TTL).
   - Esto reduce las consultas repetidas al sitio web, optimizando la velocidad y el consumo de recursos.

3. **Despliegue:**
   - El proyecto está desplegado en un clúster de Kubernetes, con un diseño escalable y administrado mediante **Nginx** como proxy inverso.

---

## Tecnologías utilizadas

- **FastAPI**: Framework para construir la API.
- **BeautifulSoup**: Biblioteca de Python para analizar y extraer datos de HTML.
- **Redis**: Sistema de caché en memoria para acelerar el acceso a los datos.
- **Kubernetes**: Para el despliegue y gestión de contenedores.
- **Nginx**: Proxy inverso para distribuir y administrar las solicitudes.

---

## Características principales

- **Web Scraping**: Uso de **BeautifulSoup** para extraer datos de una página web en tiempo real.
- **Caché Inteligente**: Implementación de **Redis** para almacenar temporalmente los datos extraídos.
- **Escalabilidad**: Despliegue en un clúster de **Kubernetes**, lo que permite escalar según la carga.
- **Gestión eficiente**: Uso de **Nginx** para equilibrar las cargas y administrar el tráfico de la API.

---

## Ejemplo de la API

Este proyecto combina **BeautifulSoup** y **FastAPI** para mostrar cómo se pueden construir APIs con funcionalidad de web scraping.

### API

![Ejemplo de datos extraídos](https://i.ibb.co/z5xCjgk/grafocas.png)

---

## Interfaz de Kubernetes

La API está desplegada y gestionada dentro de un clúster de Kubernetes. A continuación, un ejemplo del tablero de control (dashboard):

![Dashboard de Kubernetes](https://i.ibb.co/bFkJ9G0/kubernete.png)

---

## Instalación y uso

### Requisitos previos

- **Python 3.8+**
- **Docker** y **kubectl**
- Clúster de **Kubernetes** en ejecución.



