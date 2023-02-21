import os
from dotenv import load_dotenv
import requests
import datetime as dt

load_dotenv()

today = dt.datetime.now()
date = today.strftime('%d/%m/%Y')
time = today.strftime('%H:%M:%S')
API_KEY = os.environ.get('NUTRITION_API_KEY')
API_ID = os.environ.get('NUTRITION_API_ID')
NUTRITION_ENDPOINT = 'https://trackapi.nutritionix.com/v2/natural/exercise'
SHEETY_ENDPOINT = 'https://api.sheety.co/f815ba6ce1cba94add578cc6ac62487c/workoutNivaan/workouts'
exercises = []
durations = []
kcal = []

headers = {
    'x-app-id': API_ID,
    'x-app-key': API_KEY,
    'x-remote-user-id': '0'
}

parameters = {
    "query": input("Please input your exercise regime below:\n"),
    'gender': input('Please input your biological gender (male/female)').lower(),
    'weight_kg': float(input('Please input your weight in KG')),
    'height_cm': float(input('Please input your height in cm')),
    'age': int(input('Please input your age'))
}

response = requests.post(url=NUTRITION_ENDPOINT, headers=headers, json=parameters)
print(response.json())
data = response.json()['exercises']

for i in range(len(data)):
    exercises.append(data[i]['name'])
    durations.append(data[i]['duration_min'])
    kcal.append(data[i]['nf_calories'])

# Output: ['running', 'push-up'] [515.48, 149.91] [40, 30]

for i in range(len(exercises)):
    sheety_data = {
        'workout': {
            'date': date,
            'time': time,
            'exercise': exercises[i],
            'duration': str(durations[i]),
            'calories': str(kcal[i])
        }
    }

    header1 = {
        'Authorization': os.environ.get('SHEETY_KEY')
    }

    response1 = requests.post(url=SHEETY_ENDPOINT, json=sheety_data, headers=header1)
    print(response1.text)
