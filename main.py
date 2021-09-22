from database import send_cars
from database import print_cars_from_db
from database import get_token
from database import remove_cars
from database import create_race
from database import create_results
import requests
import json
import time
import asyncio
from error import OutOfGazError, TooMuchFuelError
from race import Race
from car import Car


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