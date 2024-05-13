import time
import requests


def check_elasticsearch():
    url = "http://localhost:9200/_cluster/health"
    while True:
        try:
            response = requests.get(url)
            if response.status_code == 200 and '"status":"green"' in response.text:
                print("Elasticsearch está listo.")
                break
            else:
                print("Esperando a que Elasticsearch esté listo...")
        except requests.ConnectionError:
            print("Esperando a que Elasticsearch esté listo...")
        time.sleep(10)


if __name__ == "__main__":
    check_elasticsearch()
