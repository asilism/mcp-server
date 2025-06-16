# calendar_server.py
from typing import List, Optional
from mcp.server.fastmcp import FastMCP
from datetime import datetime

mcp = FastMCP("KnoxCalendar", port=8003)

CALENDAR = {
    "events": [
        {"id": "event001", "title": "팀 정기 회의", "time": "2025-06-06T10:00:00"},
        {"id": "event002", "title": "병원 예약", "time": "2025-06-07T15:30:00"},
        {"id": "event003", "title": "프로젝트 킥오프", "time": "2025-06-08T09:00:00"},
        {"id": "event004", "title": "코드 리뷰", "time": "2025-06-09T14:00:00"},
        {"id": "event005", "title": "인사팀 미팅", "time": "2025-06-10T11:00:00"},
        {"id": "event006", "title": "예산 기획 회의", "time": "2025-06-11T16:00:00"}
    ],
    "details": {
        "event001": {"title": "팀 정기 회의", "time": "2025-06-06T10:00:00", "location": "Zoom", "description": "주간 팀 회의"},
        "event002": {"title": "병원 예약", "time": "2025-06-07T15:30:00", "location": "시티 병원", "description": "정기 건강검진"},
        "event003": {"title": "프로젝트 킥오프", "time": "2025-06-08T09:00:00", "location": "본사 회의실", "description": "프로젝트 시작을 위한 전체 회의"},
        "event004": {"title": "코드 리뷰", "time": "2025-06-09T14:00:00", "location": "회의실 A", "description": "최근 커밋 코드 리뷰"},
        "event005": {"title": "인사팀 미팅", "time": "2025-06-10T11:00:00", "location": "인사팀 사무실", "description": "월간 인사팀 미팅"},
        "event006": {"title": "예산 기획 회의", "time": "2025-06-11T16:00:00", "location": "재무팀 회의실", "description": "3분기 예산 관련 논의"}
    }
}

@mcp.tool()
async def get_today_date() -> str:
    """오늘 날짜를 'yyyy-MM-dd' 형식으로 반환합니다.
    - No input is required.
    - Call this tool without any arguments.
    """
    return "2025-06-08"
    #return datetime.now().strftime("%Y-%m-%d")

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

@mcp.tool()
async def update_event(event_id: str, title: Optional[str] = None, time: Optional[str] = None,
                       location: Optional[str] = None, description: Optional[str] = None) -> dict:
    """
    기존 일정을 업데이트합니다.
    - 제공된 필드만 수정되며 나머지는 그대로 유지됩니다.
    - event_id: str - 수정할 일정의 ID (required)
    """
    print(f"[LOG] update_event called with event_id={event_id}")
    if event_id not in CALENDAR["details"]:
        return {"error": "Invalid event ID."}

    event = CALENDAR["details"][event_id]
    if title: event["title"] = title
    if time: event["time"] = time
    if location: event["location"] = location
    if description: event["description"] = description

    # 이벤트 목록에도 반영
    for e in CALENDAR["events"]:
        if e["id"] == event_id:
            if title: e["title"] = title
            if time: e["time"] = time
            break

    return {"status": "updated", "event_id": event_id, "updated_fields": {k: v for k, v in {
        "title": title, "time": time, "location": location, "description": description}.items() if v is not None}}

@mcp.tool()
async def delete_event(event_id: str) -> dict:
    """
    기존 일정을 삭제합니다.
    - 이벤트 ID가 존재하지 않으면 오류를 반환합니다.
    """
    print(f"[LOG] delete_event called with event_id={event_id}")
    if event_id not in CALENDAR["details"]:
        return {"error": "Invalid event ID."}

    # 세부 정보 삭제
    del CALENDAR["details"][event_id]

    # 목록에서도 제거
    CALENDAR["events"] = [e for e in CALENDAR["events"] if e["id"] != event_id]

    return {"status": "deleted", "event_id": event_id}

if __name__ == "__main__":
    mcp.run(transport="streamable-http")
