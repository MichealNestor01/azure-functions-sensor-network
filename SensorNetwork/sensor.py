from numpy.random import default_rng
from random import randint 

class Sensor:
    # random number generator, used to generate
    # nromally random changes in our sensour values
    __rng = default_rng().normal
    __mu, __sigma = 0, 0.1
    # setup the range of values for each attribute
    __temp_range = [8, 15]
    __wind_range = [15, 25]
    __humid_range = [40, 70]
    __CO2_range = [500, 1500]

    def __init__(self, sensorId: int) -> None:
        self.id = sensorId
        # each attributes starts at a random point in the range
        self.temp = randint(self.__temp_range[0], self.__temp_range[1])
        self.wind = randint(self.__wind_range[0], self.__wind_range[1])
        self.humid = randint(self.__humid_range[0], self.__humid_range[1])
        self.CO2 = randint(self.__CO2_range[0], self.__CO2_range[1])

    # get random scalar value between -1 and 1
    def __get_random_scalar(self) -> float:
        random_scalar = -2
        while random_scalar < -1 or random_scalar > 1:
            random_scalar = self.__rng(self.__mu, self.__sigma, 1)[0]
        return random_scalar

    # gets a reasonable value to change by
    def __get_reasonable_increment(self, sample_range: list[int], current_value: int) -> int:
        # can decrease or increase value
        pos_neg_scalar = 1 if self.__get_random_scalar() > 0.5 else -1 
        # get a random scalar we can use to get a reasonable increment
        random_scalar = self.__get_random_scalar()
        # sample the range of possible increments
        increment_range = sample_range[1] - sample_range[0]
        # get the increment
        increment = pos_neg_scalar * int(round(increment_range*random_scalar))
        # check that current + increment does not breach the range
        if current_value + increment > sample_range[1]:
            return sample_range[1] - current_value
        elif current_value + increment < sample_range[0]:
            return sample_range[0] - current_value
        return increment
    
    # change the sensor values but a random but normally distributed amount
    # this ensures that sensors values will be random but not irativc.
    def change_temp(self) -> None:
        self.temp += self.__get_reasonable_increment(self.__temp_range, self.temp)

    def change_wind(self) -> None:
        self.wind += self.__get_reasonable_increment(self.__wind_range, self.wind)

    def change_humid(self) -> None:
        self.humid += self.__get_reasonable_increment(self.__humid_range, self.humid)

    def change_CO2(self) -> None:
        self.CO2 += self.__get_reasonable_increment(self.__CO2_range, self.CO2)

    # update all of the sensors values
    def update(self) -> None:
        self.change_temp()
        self.change_wind()
        self.change_humid()
        self.change_CO2()

    # return all attributes as an array 
    def get_sensor_values_as_array(self) -> list[int]:
        return [
            self.temp,
            self.wind,
            self.humid,
            self.CO2
        ]

    # return all attributes as a dict 
    def get_sensor_values_as_dict(self) -> dict[str, int]:
        return {
            "temp": self.temp,
            "wind": self.wind,
            "humid": self.humid,
            "CO2": self.CO2
        }
    
    # string representation 
    def __str__(self) -> str:
        return str(f"Sensor {self.id}:" +
               f"\tTemparature: {self.temp} Degrees Celsius" +
               f"\tWind: {self.wind}mph" +
               f"\tRelative Humidity: {self.humid}%" +
               f"\tCO2 Level: {self.CO2}ppm")