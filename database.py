from car import Car
import requests
import json
from race import Race
from error import OutOfGazError

def get_token(identifier: str, password: str) -> str:
    auth = requests.post(
		url="http://localhost:1337/auth/local",
		data={
			'identifier': identifier, 
			'password': password,
		}
    )
    auth.raise_for_status()
    token = 'Bearer ' + auth.json()['jwt']
    return token

   
def send_cars(token: str, cars: list[Car]) -> None:
    for car in cars:
        car_sent = requests.post(
            url="http://localhost:1337/cars",
            data=json.dumps(dict(car)),
            headers={
                'Authorization': token,	
                'Content-Type': 'application/json',
            }
        )
        car_sent.raise_for_status()

def remove_cars(token: str) -> None:
    cars = requests.get(
		url="http://localhost:1337/cars",
		headers={"Authorization": token},
    )
    car_dict = cars.json()
    for car in car_dict:
        requests.delete(
			url="http://localhost:1337/cars" + f"/{car['id']}",
			headers={"Authorization": token},
        )

def print_cars_from_db(token: str) -> None:
    cars = requests.get(
		url="http://localhost:1337/cars",
		headers={"Authorization": token}
    )
    cars.raise_for_status()
    print(cars.json())
   
 
def create_race(token: str, race: Race) -> None:
    response = requests.get(
        url="http://localhost:1337/cars",
        params={"name": [
        	car.name
        	for car in race.cars
    	]},
        headers={'Authorization': token}
    )
    response = requests.post(
        url="http://localhost:1337/races",
        data=json.dumps({
            'name' : race.name,
            'cars': [
				car['id']
				for car in response.json()
			]
        }),
        headers={
            'Authorization': token,	
            'Content-Type': 'application/json',
        }
    )
    
def _put_results_in_db(token: str, cars: list[dict], race_id: str) -> None:
    cars = [
        {
            "time": car['move_time'].move_time if isinstance(car['move_time'], OutOfGazError) else car['move_time'], 
            "name": car['car'].name,
            "car": car['car'],
            "ranked": False if isinstance(car['move_time'], OutOfGazError) else True,
            "unit_in_time": car['unit_in_time'],
        }
        for car in cars
    ]
    for car in cars:
        response = requests.get(
            url="http://localhost:1337/cars",
            params={"name": car['name']},
            headers={'Authorization': token}
        )
        requests.post(
            url="http://localhost:1337/results",
            data=json.dumps({
                'time': round(car['time'], 3) if car['unit_in_time'] is True else None,
                'distance': car['time'] * car['car'].maximum_speed if car['unit_in_time'] is False else None,
                'ranked': car['ranked'],
                'car': response.json()[0]['id'],
                'race': race_id
            }),
            headers={
                'Authorization': token,	
                'Content-Type': 'application/json',
            }
        )
    
    
def create_results(token: str, race: Race, results: list[dict]) -> None:
    response = requests.get(
        url="http://localhost:1337/races",
        params={"name": race.name},
        headers={
            'Authorization': token,	
            'Content-Type': 'application/json',
        }
    )
    race_id = response.json()[0]['id']
    _put_results_in_db(token, results, race_id)

