# calendar_server.py
from typing import List
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("KnoxCalendar", port=8003)

CALENDAR = {
    "events": [
        {"id": "event001", "title": "Team Sync", "time": "2025-06-06T10:00:00"},
        {"id": "event002", "title": "Doctor Appointment", "time": "2025-06-07T15:30:00"},
    ],
    "details": {
        "event001": {
            "title": "Team Sync",
            "time": "2025-06-06T10:00:00",
            "location": "Zoom",
            "description": "Weekly team sync-up meeting"
        },
        "event002": {
            "title": "Doctor Appointment",
            "time": "2025-06-07T15:30:00",
            "location": "City Hospital",
            "description": "Regular health check-up"
        },
    }
}

@mcp.tool()
async def list_events() -> dict:
    """ 등록된 모든 일정의 요약 정보를 JSON 형식으로 반환합니다 """
    print("[LOG] list_events called")
    return {"events": CALENDAR["events"]}

@mcp.tool()
async def get_event_detail(event_id: str) -> dict:
    """ 특정 일정의 세부 정보를 JSON 형식으로 반환합니다 """
    print(f"[LOG] get_event_detail called with event_id={event_id}")
    if event_id not in CALENDAR["details"]:
        return {"error": "Invalid or missing event ID."}
    return CALENDAR["details"][event_id]

@mcp.tool()
async def create_event(title: str, time: str, location: str, description: str) -> dict:
    """ 새로운 일정을 생성하고 생성된 일정의 정보를 반환합니다 """
    print(f"[LOG] create_event called with title={title}, time={time}, location={location}, description={description}")
    new_id = f"event{len(CALENDAR['events']) + 1:03d}"
    new_event = {"id": new_id, "title": title, "time": time}
    CALENDAR["events"].append(new_event)
    CALENDAR["details"][new_id] = {
        "title": title,
        "time": time,
        "location": location,
        "description": description
    }
    return {"status": "created", "event_id": new_id, "title": title}

if __name__ == "__main__":
    mcp.run(transport="streamable-http")
