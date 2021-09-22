import asyncio
from error import OutOfGazError
from car import Car
from typing import Optional, Tuple


class Race:
    def __init__(
            self, name, *args: list[Car]
    ):
        self.name = name
        self.cars: list[Car] = args
    
    def __iter__(self):
        for car in self.cars:
            yield dict(car)

    def _print_results(self, results: list[dict]) -> None:
        """
        The result list is divided into two lists: the list of ranked cars and the list of unranked cars.
        Depending on the grading_unit, the ranked list is sorted by time (grading_unit = 's') or by distance (grading_unit = 'm')
        """
        ranked, unranked = [], []
        for result in results: # split results in two list : ranked and if necessary unranked cars
            if isinstance(result["car"], OutOfGazError):
                unranked.append(result)
            else:
                ranked.append(result)
        # Sort the two list, if unit_in_time is False the distance covered is calculated from the race time and the maximum_speed of the car.
        # For the unranked car, sort is only done by distance covered.
        unit_in_time = ranked[0]["unit_in_time"]
        ranked.sort(
            key= lambda car_ranked: None if car_ranked["unit_in_time"] is True else car_ranked["move_time"] * car_ranked["car"].maximum_speed,
            reverse=not unit_in_time
        )
        unranked.sort(
            key=lambda car_unranked: car_unranked['move_time'] * car_unranked['car'].maximum_speed,
            reverse=True
        )
        rank = 1
        if ranked:
            print("=== RANKED ===")
            for car in ranked:
                print(f"Rank {rank} -> {'TIME' if unit_in_time is True else 'DISTANCE'} : {round(car['move_time'], 3) if unit_in_time is True else car['car'].maximum_speed} {'s' if unit_in_time is True else 'm'} -> Car : {car['car'].model} - {car['car'].name}")
                rank += 1
        if unranked:
            print("=== UNRANKED ===")    
            for car in unranked:
                print(f"Rank {rank} -> DISTANCE : {round(car['move_time'] * car['car'].maximum_speed, 3)} m -> Car : {car['car'].model} - {car['car'].name} ")
                rank += 1
    
    def full_gas(self) -> None:
        for car in self.cars:
            car.put_fuel()

    async def run(self, distance: Optional[int] = None) -> list[Tuple]:
        """
        Method to start the race with all the cars.
        If no distance is specified then the race will be run until the fuel is exhausted.
        If there is no precise distance then the ranking will be done on the distance covered (grading_unit = 'm'), otherwise, on the time (grading_unit = 's')
        The results are then put in the form of a list[tuple] containing the race time and the corresponding car
        """
        move_times = await asyncio.gather(*[
            car.move_on(duration=None if distance is None else distance / car.maximum_speed)
            for car in self.cars     
        ], return_exceptions=True)
        results = [
            {
                "move_time" : move_time,
                "car" : car,
                "unit_in_time": False if distance is None or isinstance(move_times, OutOfGazError) else True,
            }
               for car, move_time in zip(self.cars, move_times)
        ]
        self._print_results(results)
        return results
    