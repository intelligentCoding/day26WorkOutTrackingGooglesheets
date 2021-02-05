from datetime import datetime
import requests
import os
from dotenv import load_dotenv

exercise_endpoint = "https://trackapi.nutritionix.com/v2/natural/exercise"
sheety_endpoint = "https://api.sheety.co/85189b3d66f4d8d73849a00f61b10da8/copyOfMyWorkouts/workouts"
exercise_text = input("Tell me which exercises you did: ")
load_dotenv('.env')
headers = {
    "x-app-id": os.getenv("APP_ID"),
    "x-app-key": os.getenv("API_KEY"),
}
parameters = {
    "query": exercise_text,
    "gender": os.getenv("GENDER"),
    "weight_kg": os.getenv("WEIGHT_KG"),
    "height_cm": os.getenv("HEIGHT_CM"),
    "age": os.getenv("AGE")
}

response = requests.post(exercise_endpoint, json=parameters, headers=headers)
result = response.json()
print(result)

# set up today's date
today_date = datetime.now().strftime("%d/%m/%Y")
now_time = datetime.now().strftime("%X")

bearer_headers = {
    "Authorization": f"Bearer {os.getenv('TOKEN')}",
    "Content-Type": "application/json",
}
print(bearer_headers)
for exercise in result["exercises"]:
    sheet_inputs = {
        "workout": {
            "date": today_date,
            "time": now_time,
            "exercise": exercise["name"].title(),
            "duration": exercise["duration_min"],
            "calories": exercise["nf_calories"]
        }
    }

    sheet_response = requests.post(sheety_endpoint, json=sheet_inputs, headers=bearer_headers)

    print(sheet_response.text)

