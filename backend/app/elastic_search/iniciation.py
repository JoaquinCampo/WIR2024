import time
import requests
import simplejson

def check_elasticsearch():
    url = "http://localhost:9200/_cluster/health"
    while True:
        try:
            response = requests.get(url)
            if response.status_code == 200:
                health_status = response.json().get("status")
                if health_status == "green" or health_status == "yellow":
                    print("Elasticsearch está listo.")
                    break
                else:
                    print(simplejson.dumps(response, indent=4, sort_keys=True))
                    print("Esperando a que Elasticsearch esté listo...")
            else:
                print("Error al verificar el estado de Elasticsearch:", response.status_code)
        except requests.ConnectionError:
            print("Esperando a que Elasticsearch esté listo...")
        time.sleep(10)

if __name__ == "__main__":
    check_elasticsearch()
