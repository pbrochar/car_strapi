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
    try:
        auth.raise_for_status()
    except Exception as e:
        raise
    token = 'Bearer ' + auth.json()['jwt']
    return (token)

   
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
        try:
            car_sent.raise_for_status()
        except Exception as e:
            raise

def remove_cars(token: str) -> None:
    cars = requests.get(
            url="http://localhost:1337/cars",
            headers={
                'Authorization': token,
            }
    )
    car_dict = cars.json()
    for car in car_dict:
        car_rem = requests.delete(
                    url="http://localhost:1337/cars" + f"/{car['id']}",
                    headers={
                        'Authorization': token,
                    },
        )

def print_cars_from_db(token: str) -> None:
    cars = requests.get(
            url="http://localhost:1337/cars",
            headers={'Authorization': token}
    )
    try:
        cars.raise_for_status()
    except Exception as e:
        raise
    print(cars.json())
   
 
def create_race(token: str, race: Race) -> None:
    response = requests.get(
        url="http://localhost:1337/cars",
        headers={'Authorization': token}
    )
    car_names = [
        car.name
        for car in race.cars
    ]
    ids = [ 
        car['id']
        for car in response.json()
        if car['name'] in car_names
    ]
    response = requests.post(
        url="http://localhost:1337/races",
        data=json.dumps({
            'name' : race.name,
            'cars': ids,
        }),
        headers={
            'Authorization': token,	
            'Content-Type': 'application/json',
        }
    )
    
def _put_results_in_db(token: str, cars: list[dict], ranked: bool, race_id: str) -> None:
    cars = [
        {
            "time": car['move_time'], 
            "name": car['car'].name,
            "car": car['car'],
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
                'ranked': ranked,
                'car': response.json()[0]['id'],
                'race': race_id
            }),
            headers={
                'Authorization': token,	
                'Content-Type': 'application/json',
            }
        )
    
    
def create_results(token: str, race: Race, results: list[dict]) -> None:
    race_id = requests.get(
        url="http://localhost:1337/races",
        params={"name": race.name},
        headers={
            'Authorization': token,	
            'Content-Type': 'application/json',
        }
    )
    ranked, unranked = [], []
    for result in results: # split results in two list : ranked and if necessary unranked cars
        if isinstance(result['car'], OutOfGazError):
            unranked.append(result)
        else:
            ranked.append(result)
    if ranked:
        _put_results_in_db(token, ranked, True, race_id.json()[0]['id'])
    if unranked:
        _put_results_in_db(token, ranked, False, race_id.json()[0]['id'])

