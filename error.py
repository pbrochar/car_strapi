class CarError(Exception):
    pass

class OutOfGazError(CarError):
    def __init__(self, message: str, move_time: int):
        super().__init__(message)
        self.move_time = move_time

class TooMuchFuelError(CarError):
    pass