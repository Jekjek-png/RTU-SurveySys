from fastapi import FastAPI
import csv

app = FastAPI()

@app.get("/services")
def get_services():
    services = []
    with open("Services.csv", newline="") as file:
        reader = csv.DictReader(file)
        for row in reader:
            services.append({
                "service_id": row["service_id"],
                "service_name": row["service_name"]
            })
    return {"services": services}
