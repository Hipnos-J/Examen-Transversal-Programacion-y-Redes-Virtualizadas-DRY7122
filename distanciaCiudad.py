import requests
import urllib.parse

API_KEY = "7nMLkh6X6ocWdLjKEU0EEssVQdxLj7JT"  

def obtener_ruta():
    while True:
        print("\n- Calcula tu de Viaje de Chile-Argentina (o presione 's' para salir) ---")
        origen = input("Ciudad de Origen: ")
        if origen.lower() == 's': break
       
        destino = input("Ciudad de Destino: ")
        if destino.lower() == 's': break
       
        print("\nSeleccione medio de transporte:")
        print("1. Auto ")
        print("2. Bicicleta ")
        print("3. Caminando ")
        opcion = input("Opción: ")
       
        if opcion == '1': transporte = "fastest"
        elif opcion == '2': transporte = "bicycle"
        elif opcion == '3': transporte = "pedestrian"
        else:
            print("Opción inválida, usando Auto por defecto.")
            transporte = "fastest"

        url = f"https://www.mapquestapi.com/directions/v2/route?key={API_KEY}&from={origen}&to={destino}&routeType={transporte}"
       
        try:
            response = requests.get(url).json()
            status = response["info"]["statuscode"]
           
            if status == 0:
                route = response["route"]
                distancia_millas = route["distance"]
                distancia_km = distancia_millas * 1.60934
                tiempo_formateado = route["formattedTime"]
               
                print("\n================ RESULTADOS ================")
                print(f"Origen: {origen} -> Destino: {destino}")
                print(f"Distancia en Millas: {distancia_millas:.2f} mi")
                print(f"Distancia en Kilómetros: {distancia_km:.2f} km")
                print(f"Duración del viaje: {tiempo_formateado}")
                print("============================================")
               
                print("\nNarrativa del viaje:")
                for leg in route["legs"]:
                    for maneuver in leg["maneuvers"]:
                        print(f"- {maneuver['narrative']}")
            else:
                print(f"Error de MapQuest (Código {status}): Verifique las ciudades ingresadas.")
        except Exception as e:
            print(f"Ocurrió un error en la conexión: {e}")

obtener_ruta()