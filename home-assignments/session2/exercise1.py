#!/usr/bin/python3

import subprocess

try:
    import click
    from weather import Weather, Unit
except ModuleNotFoundError:
    subprocess.call(['pip3', 'install', 'click'])
    subprocess.call(['pip3', 'install', 'weather-api'])
    import click
    from weather import Weather, Unit


@click.command()
@click.option('--city', required=True, help='get weather forecast for this city')
@click.option("--forecast", required=False, default="TODAY", help="TODAY or TODAY+n for future forecast, n = [1-9]",
              show_default=True)
@click.option('--unit', type=click.Choice(['c', 'f']), default="c", help='Temperature Unit Type', show_default=True)
def main(city, unit, forecast):
    try:
        invoke_request_to_weather_api(city, unit)
        print_weather_by_city(city, unit, forecast)
    except AttributeError:
        print("No data for the requested city", city, "or no such city exist")


def invoke_request_to_weather_api(city, unit):
    if unit == 'c':
        unit = 'CELSIUS'
    elif unit == 'f':
        unit = 'FAHRENHEIT'
    weather = Weather(unit=getattr(Unit, unit))
    city_weather_info = weather.lookup_by_location(city)
    return city_weather_info, unit


def number_of_forecast_days(forecast):
    forecast_as_list = forecast.split('+')
    if len(forecast_as_list) == 1:
        return 1
    num_desired_forecast = int(forecast_as_list[1])+1
    if num_desired_forecast > 10:
        print("Weather API can only show upcoming 9 days. Please type: --forecast TODAY+[1-9] (without brackets)")
        exit(1)
    return num_desired_forecast


def print_weather_by_city(city, unit, forecast):
    num_desired_forecast = number_of_forecast_days(forecast)
    city_weather_info, unit = invoke_request_to_weather_api(city, unit)
    for num, forecast in enumerate(city_weather_info.forecast[:num_desired_forecast]):
        if num == 0:
            begin_sentence_with = f'The weather in {city_weather_info.location.city} today is'
        else:
            begin_sentence_with = forecast.date
        print(f'{begin_sentence_with} {forecast.text} with temperatures trailing from'
              f' 'f'{forecast.low}-{forecast.high} {unit}.')
        if num == 0 and num_desired_forecast > 1:
            print(f'\nForecast for the next {num_desired_forecast - 1} days: \n')


if __name__ == "__main__":
    main()
