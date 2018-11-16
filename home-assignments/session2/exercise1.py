import subprocess
from weather import Weather, Unit

try:
    import click
except ModuleNotFoundError:
    subprocess.call(['pip', 'install', 'click'])
    import click


@click.command()
@click.option('--city', required=True, help='get weather forecast for this city')
@click.option("--forecast", required=False, default="TODAY", help="TODAY or TODAY+n for future forecast, n = [1-9]",
              show_default=True)
@click.option('-c', 'unit', flag_value='CELSIUS', default=True)
@click.option('-f', 'unit', flag_value='FAHRENHEIT')


def main(city, unit, forecast):
    try:
        invoke_request_to_weather_api(city, unit)
        print_weather_by_city(city, unit, forecast)
    except AttributeError:
        print("No data for the requested city",city, "or no such city exist")



def invoke_request_to_weather_api(city, unit):
    weather = Weather(unit=getattr(Unit, unit))
    city_weather_info = weather.lookup_by_location(city)
    return city_weather_info


def number_of_forecast_days(forecast):
    if forecast == "TODAY" or forecast == None:
        num_desired_forecast = 1
    else:
        num_desired_forecast = int(forecast.split('TODAY+')[1]) + 1
        if num_desired_forecast > 10:
            print("Weather API can only show upcoming 9 days. Please type: --forecast TODAY+[1-9] (without brackets)\n")
            exit(1)
    return num_desired_forecast


def print_weather_by_city(city, unit, forecast):
    num_desired_forecast = number_of_forecast_days(forecast)
    city_weather_info = invoke_request_to_weather_api(city, unit)
    for num, forecast in enumerate(city_weather_info.forecast[:num_desired_forecast]):
        if num == 0:
            begin_sentence_with = f'The weather in {city_weather_info.location.city} today is'
        else:
            begin_sentence_with = forecast.date
        print(f'{begin_sentence_with} {forecast.text} with temperatures trailing from' \
              f' 'f'{forecast.low}-{forecast.high} {unit}.')
        if num == 0 and num_desired_forecast > 1:
            print(f'\nForecast for the next {num_desired_forecast - 1} days: \n')


if __name__ == "__main__":
    main()