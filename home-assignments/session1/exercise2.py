import subprocess

try:
    import requests
    import pytemperature
    from pycountry_convert import country_alpha2_to_country_name
except ModuleNotFoundError:
    subprocess.call(['pip', 'install', 'requests'])
    subprocess.call(['pip', 'install', 'pytemperature'])
    subprocess.call(['pip', 'install', 'pycountry_convert'])
    import requests
    import pytemperature
    from pycountry_convert import country_alpha2_to_country_name


location_by_ip_api_url = 'http://ip-api.com/json'
weather_api_url = 'http://api.openweathermap.org/data/2.5/weather?q={city}&APPID=dec07a75427862501fb3e97181ac04e8'
worldwide_cities = ["Paris", "Tokyo", "London", "Rome", "Oga", "Sydney", "Istanbul", "Seoul", "Singapore", "Bangkok"]


def current_location(location_by_ip_url):
    response = requests.get(location_by_ip_url)
    json_response = response.json()
    city = json_response["city"]
    country = json_response["country"]
    return city, country


def weather_request(weatherapi_url):
    response = requests.get(weatherapi_url)
    json_data = response.json()
    return json_data


def write_my_city_weather_to_file(my_city, my_country, weather_description, weather_temperature):
    # Writes the weather info in my city to file
    with open("{}weather_in_{}.txt".format("", my_city), "w") as text_file:
        print("Want to know what's the weather in", my_city, "? Go to the text file created!")
        print("The weather in {}, {}: {} with temperature of {} Celsius degrees".format(my_city, my_country,
                                                                                        weather_description,
                                                                                        int(weather_temperature)),
                                                                                        file=text_file)


def check_weather_in_listed_cities(worldwide_cities):
    for city in worldwide_cities:
        custom_weather_api_url = weather_api_url.replace("{city}", city)
        weather_request_data = weather_request(custom_weather_api_url)
        weather_temperature = pytemperature.k2c(weather_request_data["main"]["temp"])
        country_code = weather_request_data["sys"]["country"]
        country_name = country_alpha2_to_country_name(country_code)
        print("The weather in", city, ', ' + country_name, "is", int(weather_temperature), "Celsius degrees.")


def main():
    my_city, my_country = current_location(location_by_ip_api_url)
    custom_weather_api_url = weather_api_url.replace("{city}", my_city)
    weather_request_data = weather_request(custom_weather_api_url)
    weather_description = weather_request_data["weather"][0]["description"]
    weather_temperature = pytemperature.k2c(weather_request_data["main"]["temp"])
    write_my_city_weather_to_file(my_city, my_country, weather_description, weather_temperature)
    check_weather_in_listed_cities(worldwide_cities)


if __name__ == "__main__":
    main()