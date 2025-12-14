import requests
import json
import os
from tavily import TavilyClient

def get_weather(city: str) -> str:
    """
    查询指定城市的实时天气。
    """
    url = f"https://wttr.in/{city}?format=j1"

    try:
        response = requests.get(url)
        response.raise_for_status()
        weather_info = response.json()
        current_condition = weather_info['current_condition'][0]
        weather_desc = current_condition['weatherDesc'][0]['value']
        temperature = current_condition['temp_C']
        return f"城市：{city}, 当前天气：{weather_desc}, 气温：{temperature}°C"
    except (requests.RequestException, KeyError, json.JSONDecodeError) as e:
        return f"错误:查询天气时遇到问题 - {e}"

def get_attraction(city: str, weather: str) -> str:
    """
    根据城市和天气搜索推荐的旅游景点。
    """
    tavilly_api_key = os.getenv("TAVILY_API_KEY")
    if not tavilly_api_key:
        return "错误: TAVILY_API_KEY 环境变量未设置。"

    client = TavilyClient(api_key=tavilly_api_key)
    prompt = f"推荐一些适合在{city}当前天气为{weather}时游玩的旅游景点。"
    response = client.search(query=prompt, search_depth="basic", include_answer=True)

    if response and 'answer' in response:
        return response['answer']
    else:
        return "未找到推荐的旅游景点。"
    
available_tools = {
    "get_weather": get_weather,
    "get_attraction": get_attraction,
}

if __name__ == "__main__":
    city = "Beijing"
    weather_info = available_tools.get("get_weather")(city)
    print(weather_info)
    weather_desc = weather_info.split("当前天气：")[1].split(",")[0]
    attractions = available_tools.get("get_attraction")(city, weather_desc)
    print(attractions)