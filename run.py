#!/usr/bin/env python3


import sys
import time
import logging
import requests
import pytemperature
import click


def wind_direction(degree):
    if degree < 11.25 and degree >= 0:
        return "N"
    if degree <= 360 and degree >= 348.75:
        return "N"
    if degree < 33.75:
        return "NNE"
    if degree < 56.25:
        return "NE"
    if degree < 78.75:
        return "ENE"
    if degree < 101.25:
        return "E"
    if degree < 123.75:
        return "ESE"
    if degree < 146.25:
        return "SE"
    if degree < 168.75:
        return "SSE"
    if degree < 191.25:
        return "S"
    if degree < 213.75:
        return "SSW"
    if degree < 236.25:
        return "SW"
    if degree < 258.75:
        return "WSW"
    if degree < 281.25:
        return "W"
    if degree < 303.75:
        return "WNW"
    if degree < 326.25:
        return "NW"
    if degree < 348.75:
        return "NNW"
    raise Exception(f"Invalid wind direction: {degree}")


def get_data(url):
    r = requests.get(url)
    return r.json()


class Weather:
    summary = None
    description = None
    temp_cur = None
    humid_cur = None
    temp_feel = None
    temp_min = None
    temp_max = None
    wind_speed = None
    wind_dir = None
    city = None
    country = None
    sunrise = None
    sunset = None

    def __str__(self):
        return f"temp_cur={self.temp_cur:0.1f} humid_cur={self.humid_cur:0.1f}% temp_feel={self.temp_feel:0.1f} temp_min={self.temp_min:0.1f} temp_max={self.temp_max:0.1f} wind_speed={self.wind_speed:0.1f} wind_dir={self.wind_dir} city={self.city} country={self.country} sunrise={self.sunrise} sunset={self.sunset} summary={self.summary} description={self.description}"


def parse_data(result):
    w = Weather()

    # only use primary weather condition for now
    w.summary = result["weather"][0]["main"]
    w.description = result["weather"][0]["description"]
    w.temp_cur = result["main"]["temp"]
    w.humid_cur = result["main"]["humidity"]
    w.temp_feel = result["main"]["feels_like"]
    w.temp_min = result["main"]["temp_min"]
    w.temp_max = result["main"]["temp_max"]
    w.wind_speed = result["wind"]["speed"]
    if "deg" in result["wind"]:
        w.wind_dir = wind_direction(result["wind"]["deg"])
    else:
        w.wind_dir = "None"
    w.city = result["name"].replace(" ", "_")
    w.country = result["sys"]["country"]
    w.sunrise = time.strftime("%-I:%M%p", time.localtime(result["sys"]["sunrise"]))
    w.sunset = time.strftime("%-I:%M%p", time.localtime(result["sys"]["sunset"]))
    return w


def build_url(location_id, api_key, units):
    base_url = "http://api.openweathermap.org/data/2.5/weather?"
    return f"{base_url}id={location_id}&APPID={api_key}&units={units}"


@click.command()
@click.option(
    "--mode",
    type=click.Choice(["once", "forever"]),
    default="once",
    help="Run mode: once gathers data once, and then exits, forever gathers data every INTERVAL seconds forever",
)
@click.option(
    "--interval",
    default=600,
    help="Number of seconds between data queries, default is 600 seconds(5 minutes)",
)
@click.option(
    "--api_key", required=True, help="API Key from openweathermap.org", envvar="API_KEY"
)
@click.option(
    "--units",
    type=click.Choice(["imperial", "metric"]),
    default="imperial",
    help="Type of units to get from API",
)
@click.option(
    "--location-id",
    default="5391959",
    help="Location Id, default to 5391959 for San Francisco, CA",
)
@click.option(
    "--logfile", default="weather.log", help="Log filename data is written to."
)
def main(logfile, location_id, units, api_key, interval, mode):
    """Poll current weather condition and log it to file"""

    logging.basicConfig(
        filename=logfile,
        filemode="a",
        format="%(created)f %(message)s",
        level=logging.INFO,
    )

    url = build_url(location_id, api_key, units)

    while True:
        result = get_data(url)
        weather = parse_data(result)

        if mode == "once":
            print(weather)
            break

        logging.info(weather)
        time.sleep(interval)


if __name__ == "__main__":
    main()
