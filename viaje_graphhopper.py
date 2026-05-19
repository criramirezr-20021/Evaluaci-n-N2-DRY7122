import requests
import urllib.parse

# 1. API Key de Graphhopper
api_key = "e4009da4-72d9-4690-9acf-2e816a20d9bb"

# 2. URLs de la API
geocode_api = "https://graphhopper.com/api/1/geocode?"

while True:
    print("\n" + "="*50)
    # Requerimiento: Solicitar Ciudad de Origen y Destino, y letra 'q' para salir
    origen = input("Ingrese Ciudad de Origen (o 'q' para salir): ")
    if origen.lower() == 'q':
        print("Finalizando el programa...")
        break

    destino = input("Ingrese Ciudad de Destino (o 'q' para salir): ")
    if destino.lower() == 'q':
        print("Finalizando el programa...")
        break

    # 3. Obtener coordenadas (Latitud y Longitud) de las ciudades
    url_origen = geocode_api + urllib.parse.urlencode({"q": origen, "limit": "1", "key": api_key})
    url_destino = geocode_api + urllib.parse.urlencode({"q": destino, "limit": "1", "key": api_key})

    req_origen = requests.get(url_origen)
    req_destino = requests.get(url_destino)
    datos_origen = req_origen.json()
    datos_destino = req_destino.json()

    # Validar que se encontraron resultados
    if len(datos_origen["hits"]) == 0 or len(datos_destino["hits"]) == 0:
        print("Error: No se encontró una de las ciudades. Intente nuevamente.")
        continue

    lat_origen = datos_origen["hits"][0]["point"]["lat"]
    lng_origen = datos_origen["hits"][0]["point"]["lng"]
    lat_destino = datos_destino["hits"][0]["point"]["lat"]
    lng_destino = datos_destino["hits"][0]["point"]["lng"]

    # 4. Obtener la ruta entre los dos puntos
    url_ruta = f"https://graphhopper.com/api/1/route?point={lat_origen},{lng_origen}&point={lat_destino},{lng_destino}&vehicle=car&locale=es&instructions=true&key={api_key}"
    
    req_ruta = requests.get(url_ruta)
    datos_ruta = req_ruta.json()

    if "paths" not in datos_ruta:
        print("Error al calcular la ruta.")
        continue

    # 5. Cálculos solicitados
    ruta = datos_ruta["paths"][0]
    
    # Distancia en kilómetros
    distancia_km = ruta["distance"] / 1000.0
    
    # Duración en horas, minutos y segundos
    tiempo_ms = ruta["time"]
    segundos_totales = int(tiempo_ms / 1000)
    horas = segundos_totales // 3600
    minutos = (segundos_totales % 3600) // 60
    segundos = segundos_totales % 60
    
    # Combustible requerido (Se asume estándar de 12 km por litro)
    litros_combustible = distancia_km / 12.0

    # 6. Mostrar resultados (Requerimiento: Todos los valores con dos decimales)
    print("\n--- RESUMEN DEL VIAJE ---")
    print(f"Ruta: {origen.capitalize()} a {destino.capitalize()}")
    print(f"Distancia: {distancia_km:.2f} km")
    print(f"Duración: {horas:02d} horas, {minutos:02d} minutos y {segundos:02d} segundos")
    print(f"Combustible requerido: {litros_combustible:.2f} litros")
    
    # 7. Imprimir la narrativa del viaje
    print("\n--- NARRATIVA DEL VIAJE (RUTA) ---")
    for instruccion in ruta["instructions"]:
        texto = instruccion["text"]
        dist_instruccion_km = instruccion["distance"] / 1000.0
        # Imprimir instrucción con distancia a 2 decimales
        print(f"- {texto} ({dist_instruccion_km:.2f} km)")