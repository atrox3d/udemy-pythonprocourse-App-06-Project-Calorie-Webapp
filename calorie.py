from temperature import Temperature


class Calorie:
    """
    Represent amount of calories calculated with
    BMR = 10 * weight + 6.25 * height - 5 * age - 10 * temperature
    """
    def __init__(self, weight, height, age, temperature):
        self.weight = weight
        self.height = height
        self.age = age
        self.temperature = temperature

    def calculate(self):
        bmr = 10 * self.weight + 6.25 * self.height - 5 * self.age - 10 * self.temperature
        return bmr


if __name__ == '__main__':
    country = input('Insert your country: ')
    city = input('Insert your city: ')
    temperature = Temperature(country=country, city=city).get()
    print('Your location temperature is: ', temperature)

    weight = float(input('Insert your weight: '))
    height = float(input('Insert your height: '))
    age = float(input('Insert your age: '))
    calorie = Calorie(temperature=temperature, weight=98, height=175, age=52)
    print('Your calories are: ', calorie.calculate())

