from database import send_cars
from database import print_cars_from_db
from database import get_token
from database import remove_cars
import requests
import json
import time
import asyncio
from error import OutOfGazError, TooMuchFuelError
from race import Race
from car import Car

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
           
def create_results(token: str, race: Race, results: list[tuple]) -> None:
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
        if isinstance(result[0], OutOfGazError):
            unranked.append(result)
        else:
            ranked.append(result)
    ranked_name = [
        {"time": car[0], "name": car[1].name}
        for car in ranked
    ]
    for car in ranked_name:
        response = requests.get(
            url="http://localhost:1337/cars",
            params={"name": car['name']},
            headers={'Authorization': token}
        )
        requests.post(
            url="http://localhost:1337/results",
            data=json.dumps({
                'time': round(car['time'], 3),
                'ranked': 'true',
                'car': response.json()[0]['id'],
                'race': race_id.json()[0]['id']
            }),
            headers={
                'Authorization': token,	
                'Content-Type': 'application/json',
            }
        )



if __name__ == "__main__":
    tuture = Car("Renault", "Max", 10, 10, 10, 10, 250, 10, 10)
    toto = Car("Tesla", "Paul", 10, 10, 10, 10, 210, 10, 12)
    carglass = Car("BMW", "Leo", 10, 10, 10, 10, 200, 162, 14)
    titi = Car("Peugeot", "Dede", 10, 10, 10, 10, 200, 150, 10)
    niglo = Car("2ch", "Andre", 10, 10, 10, 10, 50, 10, 10)
    voiture = Car("Ferrari", "Fisenzo", 10, 10, 10, 10, 50, 10, 100)
    ferrari = Car("Pedalo", "Patrick", 10, 10, 10, 10, 150, 90 , 11)
    try:
        token = get_token('toto@toto.com', 'mialet30')
    except Exception as e:
        print(f"{e}")
        raise
    remove_cars(token)
    try:
        send_cars(token, [tuture, toto, carglass, titi, niglo, voiture, ferrari])
    except Exception as e:
        print(f"{e}")
        raise
    # create_race(token, "Le Man", [tuture, toto])
    # try:
    #     print_cars_from_db(token)
    # except Exception as e:
    #     print(f"{e}")
    #     raise
    # remove_cars(token)
    # print_cars_from_db(token)
    race = Race("Le Man", tuture, toto)
    results = asyncio.run(race.run())
    create_race(token, race)
    create_results(token, race, results)
    
    # test = asyncio.run(race.run())
    # print(test)