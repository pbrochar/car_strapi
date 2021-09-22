from car import Car
import requests
import json
from pprint import pprint

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