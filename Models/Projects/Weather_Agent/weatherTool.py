from typing import List, Union
from datetime import datetime
from zoneinfo import ZoneInfo

from langchain_core.tools import tool
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_classic.agents import AgentExecutor, create_tool_calling_agent

from langchain_community.utilities import OpenWeatherMapAPIWrapper
from langchain_community.tools.openweathermap.tool import OpenWeatherMapQueryRun
from langchain_community.document_loaders.weather import WeatherDataLoader


def now_ist_str()->str:
    ist = ZoneInfo("Asia/Kolkata")
    return datetime.now(ist).strftime("%Y-%m-%d %H:%M IST")

@tool
def get_weather(city:str)->str:
    """Returns a short,human-friendly weather report for the given city(mock date)."""
    if not city or not city.strip():
        return "Please provide a city name."
    key = city.strip().lower()
    # data = 
    weather_wrapper = OpenWeatherMapAPIWrapper()
    data = WeatherDataLoader(client=weather_wrapper,places=key)
    result = data.load()

    return (
        f"City : {city.strip().title()}\n"
        f"Time : {now_ist_str()}\n"
        f"Condition : {data["condition"]}"
        f"Temprature : {data["tempF"]}"
        f"Humidity : {data["humidity"]}"
        f"windMPH : {data["windMPH"]}"
    )


