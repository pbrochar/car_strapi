from typing import Optional
from error import OutOfGazError, TooMuchFuelError
import asyncio

class Car:
    def __init__ (
            self,
            model: str,
            name: str,
            weight: int,
            length: int,
            height: int,
            width: int,
            maximum_speed: int,
            tank_size: int,
            average_consumption: int,
    ):
        self.model = model
        self.name = name
        
        self.weight = weight
        self.length = length
        self.height = height
        self.width = width
        
        self.maximum_speed = maximum_speed
        self.tank_size = tank_size
        self.average_consumption = average_consumption
        if self.average_consumption <= 0:
            raise ValueError('average_consumption can\'t be less than or equal to 0.')
        self._fuel_quantity = tank_size

    def __iter__(self):
        """
        Allows to create a dictionary from the dict() function.
        """
        
        yield 'model', self.model
        yield 'name', self.name
        yield 'weight', self.weight
        yield 'lenght', self.length
        yield 'height', self.height
        yield 'width', self.width
        yield 'maximum_speed', self.maximum_speed
        yield 'tank_size', self.tank_size
        yield 'average_consumption', self.average_consumption
        yield 'gas', self.gas

    def __lt__(self, other: "Car") -> bool:
        return self._get_volume() < other._get_volume()
    
    def __gt__(self, other: "Car") -> bool:
        return self._get_volume() > other._get_volume()

    def __eq__(self, other: "Car") -> bool:
        return self._get_volume() == other._get_volume()

    def __ne__(self, other: "Car") -> bool:
        return self._get_volume() != other._get_volume()
    
    def _get_volume(self) -> int:
        return self.length * self.width * self.length
    
    async def move_on(self, duration: Optional[int] = None) -> int:
        """
        This function allows the car to move forward.
        If the time is not specified, the car will move forward until the tank is empty.
        The specified time cannot be greater than the capacity of the car, 
        in this case it will move forward until the tank is empty and an exception OutOfGazError will be raise.
        """
        
        maximum_move_time = self.gas / self.average_consumption
        if duration is None:
            move_time = maximum_move_time
        elif duration < maximum_move_time:
            move_time = duration
        else:
            await asyncio.sleep(maximum_move_time)
            raise OutOfGazError("No Gaz", move_time=maximum_move_time)
        await asyncio.sleep(move_time)
        return move_time
        
    def put_fuel(self, quantity: Optional[int] = None) -> None:
        """
        This function allows to add a quantity of fuel in the car.
        You can't add a negative amount.
        If no amount is specified, then the tank will be filled up completely.
        """
        
        if quantity is None:
            self.gas = self.tank_size
        elif quantity < 0:
            raise ValueError("you can't add a negative value.")
        else:
            self.gas += quantity
        
    @property
    def gas(self) -> int:
        return self._fuel_quantity

    @gas.setter
    def gas(self, quantity: int) -> None:
        if quantity < 0:
            raise ValueError("gas can't be less than 0.")
        elif quantity > self.tank_size:
            self._fuel_quantity = self.tank_size
            raise TooMuchFuelError("fuel_quantity can\'t be greater than tank_size")
        else:
            self._fuel_quantity = quantity