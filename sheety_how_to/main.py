import os
from dotenv import load_dotenv
import requests
from datetime import datetime as dt

def get_user_input():
    prompt = input("Tell me what you did today: ")
    return prompt

def get_nutritionix_data(prompt):
    load_dotenv()
    app_id = os.getenv("NUTRIONIX_ID")
    api_key = os.getenv("NUTRIONIX_API_KEY")

    domain = "https://trackapi.nutritionix.com"
    end_point = "/v2/natural/exercise"

    url = f"{domain}{end_point}"
    headers = {
        "x-app-id": app_id,
        "x-app-key": api_key,
        "Content-Type": "application/json"
        }
    
    # prompt = f"ran 5 miles and walked 2 miles"

    response = requests.post(url, headers=headers, json={"query": prompt})
    response.raise_for_status()

    data = response.json()

    return data

def process_data(data):

    exercises = []

    for exercise in data['exercises']:
        exercises.append((exercise['name'], exercise['duration_min'], exercise['nf_calories']))

    return exercises

def processing_time():

    datetime_format = dt.now().strftime("%d/%m/%Y %H:%M:%S")
    container = datetime_format.split(" ")
    return container[0], container[1]

class Activity:
    def __init__(self, date, time, exercise, duration, calories):
        self.date = date
        self.time = time
        self.exercise = exercise
        self.duration = duration
        self.calories = calories

    def input_sheety(self):
        return {
            "workout": {
                "date": self.date,
                "time": self.time,
                "exercise": self.exercise,
                "duration": self.duration,
                "calories": self.calories
            }
        }

    def __str__(self):
        return f"date: {self.date}, time: {self.time}, exercise: {self.exercise}, duration: {self.duration}, calories: {self.calories}"
    
def sheety_part(activity):
    spreadsheet_url = os.getenv("SHEETY_URL")
    token = os.getenv("SHEETY_TOKEN")

    headers_sheet = {
        "Authorization": f"Bearer {token}"
    }

    json_workout = activity.input_sheety()

    response_sheet = requests.post(spreadsheet_url, json=json_workout, headers=headers_sheet)
    response_sheet.raise_for_status()

            
if __name__ == "__main__":

    date_today, time_today = processing_time()
    input_data = get_user_input()
    data_nutritionix = get_nutritionix_data(input_data)
    
    data_processed = process_data(data_nutritionix)
    activities = [Activity(date_today, time_today, exercise[0], exercise[1], exercise[2]) for exercise in data_processed]
    for activity in activities:
        sheety_part(activity)
