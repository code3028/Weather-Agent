import requests
from datetime import datetime
from agents import Agent, Runner

# ----------------------------
# WEATHER FUNCTION (normal Python)
# ----------------------------
def get_weather_impl(city: str) -> str:
    geo = requests.get(
        f"https://geocoding-api.open-meteo.com/v1/search?name={city}&count=1"
    ).json()

    if "results" not in geo:
        return f"City not found: {city}"

    lat = geo["results"][0]["latitude"]
    lon = geo["results"][0]["longitude"]

    weather = requests.get(
        f"https://api.open-meteo.com/v1/forecast"
        f"?latitude={lat}&longitude={lon}&current_weather=true"
    ).json()

    w = weather["current_weather"]

    return f"{city}: {w['temperature']}°C, wind {w['windspeed']} km/h"


# ----------------------------
# TIME FUNCTION
# ----------------------------
def get_time_impl() -> str:
    return datetime.now().strftime("%H:%M:%S")


# ----------------------------
# TOOL WRAPPERS (IMPORTANT FIX)
# ----------------------------
weather_tool = {
    "type": "function",
    "function": {
        "name": "get_weather",
        "description": "Get weather of a city",
        "parameters": {
            "type": "object",
            "properties": {
                "city": {"type": "string"}
            },
            "required": ["city"]
        }
    },
    "handler": get_weather_impl
}

time_tool = {
    "type": "function",
    "function": {
        "name": "get_time",
        "description": "Get current time",
        "parameters": {
            "type": "object",
            "properties": {}
        }
    },
    "handler": get_time_impl
}


# ----------------------------
# AGENT
# ----------------------------
agent = Agent(
    name="Weather Agent",
    instructions="Use tools when needed.",
    tools=[weather_tool, time_tool],
)


# ----------------------------
# RUN
# ----------------------------
result = Runner.run_sync(
    agent,
    "What is the weather in Hyderabad and time?"
)

print(result.final_output)