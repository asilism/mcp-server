# weather_server.py
from typing import Optional
from mcp.server.fastmcp import FastMCP
from datetime import datetime
from random import choice

mcp = FastMCP("Weather", port=8001)

def normalize_date(date: Optional[str]) -> str:
    # 날짜 형식은 'yyyy-MM-dd'만 허용합니다.
    if not date:
        return datetime.now().strftime("%Y-%m-%d")
    try:
        datetime.strptime(date, "%Y-%m-%d")
        return date
    except Exception:
        return "INVALID_DATE"

@mcp.tool()
async def get_weather(date: str, location: str = 'Seoul') -> str:
    """
    지정한 위치와 날짜의 날씨를 조회합니다.
    - date: 'yyyy-MM-dd' 형식의 날짜 문자열 (예: '2025-06-20') (required)
    - location: 지역 이름 (예: 'Seoul') (default : 'Seoul')
    """
    date_key = normalize_date(date)
    if date_key == "INVALID_DATE":
        return "날짜 형식이 잘못되었습니다. yyyy-MM-dd 형식으로 입력해주세요."
    weather = choice(["맑음", "흐림", "비", "안개"])
    return f"{location}의 {date_key} 날씨는 '{weather}'입니다."

@mcp.tool()
async def get_temperature(date: str, location: str = 'Seoul') -> str:
    """
    지정한 위치와 날짜의 온도를 조회합니다.
    - date: 'yyyy-MM-dd' 형식의 날짜 문자열 (예: '2025-06-20') (required)
    - location: 지역 이름 (예: 'Seoul') (default : 'Seoul')
    """
    date_key = normalize_date(date)
    if date_key == "INVALID_DATE":
        return "날짜 형식이 잘못되었습니다. yyyy-MM-dd 형식으로 입력해주세요."
    temp = f"{choice(range(18, 30))}°C"
    return f"{location}의 {date_key} 기온은 {temp}입니다."

@mcp.tool()
async def get_fine_dust_level(date: str, location: str = 'Seoul') -> str:
    """
    지정한 위치와 날짜의 미세먼지 농도를 조회합니다.
    - date: 'yyyy-MM-dd' 형식의 날짜 문자열 (예: '2025-06-21') (required)
    - location: 지역 이름 (예: 'Seoul') (default : 'Seoul')
    """
    date_key = normalize_date(date)
    if date_key == "INVALID_DATE":
        return "날짜 형식이 잘못되었습니다. yyyy-MM-dd 형식으로 입력해주세요."
    dust = f"{choice(range(20, 70))} µg/m³ ({choice(['좋음', '보통', '나쁨'])})"
    return f"{location}의 {date_key} 미세먼지 농도는 {dust}입니다."

@mcp.tool()
async def get_precipitation_chance(date: str, location: str = 'Seoul') -> str:
    """
    지정한 위치와 날짜의 강수 확률을 조회합니다.
    - date: 'yyyy-MM-dd' 형식의 날짜 문자열 (예: '2025-06-21') (required)
    - location: 지역 이름 (예: 'Seoul') (default : 'Seoul')
    """
    date_key = normalize_date(date)
    if date_key == "INVALID_DATE":
        return "날짜 형식이 잘못되었습니다. yyyy-MM-dd 형식으로 입력해주세요."
    rain = choice(["0%", "10%", "20%", "40%", "60%", "80%", "100%"])
    return f"{location}의 {date_key} 강수 확률은 {rain}입니다."

if __name__ == "__main__":
    mcp.run(transport="streamable-http")
