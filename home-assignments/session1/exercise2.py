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


def invoke_request_to_url(url):
    response = requests.get(url)
    json_response = response.json()
    return json_response


def current_location(location_by_ip_api_url):
    json_response = invoke_request_to_url(location_by_ip_api_url)
    current_city = json_response["city"]
    current_country = json_response["country"]
    return current_city, current_country


def local_weather_output_to_file(current_city, current_country):
    custom_weather_api_url = weather_api_url.replace("{city}", current_city)
    weather_request_data = invoke_request_to_url(custom_weather_api_url)
    weather_description = weather_request_data["weather"][0]["description"]
    weather_temperature = pytemperature.k2c(weather_request_data["main"]["temp"])
    with open("{}weather_in_{}.txt".format("", current_city), "w") as text_file:
        print("Want to know what's the weather in", current_city, "? Go to the text file created!")
        print("The weather in {}, {}: {} with temperature of {} Celsius degrees".format(current_country, current_country,
                                                                                        weather_description,
                                                                                        int(weather_temperature)),
                                                                                        file=text_file)


def check_weather_in_listed_cities(worldwide_cities):
    for city in worldwide_cities:
        custom_weather_api_url = weather_api_url.replace("{city}", city)
        weather_request_data = invoke_request_to_url(custom_weather_api_url)
        weather_temperature = pytemperature.k2c(weather_request_data["main"]["temp"])
        country_code = weather_request_data["sys"]["country"]
        country_name = country_alpha2_to_country_name(country_code)
        print("The weather in", city, ', ' + country_name, "is", int(weather_temperature), "Celsius degrees.")


def main():
    current_city, current_country = current_location(location_by_ip_api_url)
    local_weather_output_to_file(current_city, current_country)
    check_weather_in_listed_cities(worldwide_cities)


if __name__ == "__main__":
    main()