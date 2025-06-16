from mcp.server.fastmcp import FastMCP

mcp = FastMCP("KnoxJira", port=8004)

JIRA_ISSUES = {
    "PROJ-101": {"summary": "로그인 오류 수정", "description": "비밀번호 재설정 후 로그인이 되지 않습니다.", "status": "To Do", "due_date": "2025-06-09"},
    "PROJ-102": {"summary": "다크 모드 구현", "description": "UI 설정에 다크 모드 지원 추가", "status": "In Progress", "due_date": "2025-06-11"},
    "PROJ-103": {"summary": "DB 레이어 리팩토링", "description": "성능 및 유지보수성을 개선합니다", "status": "In Progress", "due_date": "2025-06-15"},
    "PROJ-104": {"summary": "사용자 가이드 업데이트", "description": "최근 기능을 문서에 반영합니다", "status": "To Do", "due_date": "2025-06-20"},
    "PROJ-105": {"summary": "클라우드로 마이그레이션", "description": "GCP 인프라로 이전합니다", "status": "Done", "due_date": "2025-06-01"},
    "PROJ-106": {"summary": "이메일 알림 오류 수정", "description": "비밀번호 재설정 시 이메일이 전송되지 않음", "status": "Done", "due_date": "2025-06-05"}
}

@mcp.tool()
async def list_jira_issues() -> dict:
    """Returns a list of all Jira issue keys and summaries"""
    print("[LOG] list_jira_issues called")
    issues = [{"key": k, "summary": v["summary"]} for k, v in JIRA_ISSUES.items()]
    return {"issues": issues}

@mcp.tool()
async def get_jira_issue_by_issue_key(issue_key: str) -> dict:
    """Returns the details of a specific Jira issue by issue key (case-insensitive)"""
    print(f"[LOG] get_jira_issue_by_issue_key called with issue_key={issue_key}")
    normalized_key = issue_key.upper()
    for key in JIRA_ISSUES:
        if key.upper() == normalized_key:
            issue = JIRA_ISSUES[key]
            return {
                "key": key,
                "summary": issue["summary"],
                "description": issue["description"],
                "status": issue["status"],
                "due_date": issue.get("due_date", "N/A")
            }
    return {"error": "Issue key not found."}

@mcp.tool()
async def get_jira_issue_by_status(status: str) -> dict:
    """Returns a list of Jira issues matching the given status (case-insensitive)"""
    print(f"[LOG] get_jira_issue_by_status called with status={status}")
    normalized_status = status.lower()
    matched = [
        {"key": key, "summary": issue["summary"], "status": issue["status"]}
        for key, issue in JIRA_ISSUES.items()
        if issue["status"].lower() == normalized_status
    ]
    return {"issues": matched}

@mcp.tool()
async def create_jira_issue(project_key: str, summary: str, description: str, due_date: str = "N/A") -> dict:
    """Creates a new Jira issue and returns the new issue key"""
    print(f"[LOG] create_jira_issue called with project_key={project_key}, summary={summary}, description={description}")
    new_id = f"{project_key.upper()}-{len(JIRA_ISSUES) + 101}"
    JIRA_ISSUES[new_id] = {
        "summary": summary,
        "description": description,
        "status": "To Do",
        "due_date": due_date
    }
    return {
        "status": "created",
        "issue_key": new_id,
        "summary": summary,
        "due_date": due_date
    }

@mcp.tool()
async def update_jira_issue_status(issue_key: str, new_status: str) -> dict:
    """Updates the status of the specified Jira issue to the given new status (case-insensitive issue key)"""
    print(f"[LOG] update_jira_issue_status called with issue_key={issue_key}, new_status={new_status}")
    normalized_key = issue_key.upper()
    for key in JIRA_ISSUES:
        if key.upper() == normalized_key:
            JIRA_ISSUES[key]["status"] = new_status
            return {
                "status": "updated",
                "issue_key": key,
                "new_status": new_status
            }
    return {"error": "Issue key not found."}

@mcp.tool()
async def update_jira_issue_due_date(issue_key: str, new_due_date: str) -> dict:
    """Updates the due date of the specified Jira issue"""
    normalized_key = issue_key.upper()
    for key in JIRA_ISSUES:
        if key.upper() == normalized_key:
            JIRA_ISSUES[key]["due_date"] = new_due_date
            return {
                "status": "updated",
                "issue_key": key,
                "new_due_date": new_due_date
            }
    return {"error": "Issue key not found."}