#import subprocess
#subprocess.call(['pip', 'install', 'weather-api'])
from sys import argv
import datetime
import time
from weather import Weather, Unit

weather = Weather(unit=Unit.CELSIUS)


def weather_info_by_city(city):
    city_weather_info = weather.lookup_by_location(city)
    city_forecasts = city_weather_info.forecast
    weather_description = city_forecasts[0].text
    weather_low_temp = city_forecasts[0].low
    weather_high_temp = city_forecasts[0].high
    return weather_description, weather_low_temp, weather_high_temp


def write_weather_by_city_to_file(city):
    weather_description, weather_low_temp, weather_high_temp = weather_info_by_city(city)
    with open("{}weather_in_{}.txt".format("", city), "w") as text_file:
        print(
            "The weather in {} today is {} with temperature trailing from {}-{} Celsius".format(city, weather_description,
                                                                                             weather_low_temp,
                                                                                             weather_high_temp),
                                                                                             file=text_file)


def main():
    if len(argv) == 2:
        city = argv[1]
        weather_info_by_city(city)
        write_weather_by_city_to_file(city)


if __name__ == "__main__":
    main()