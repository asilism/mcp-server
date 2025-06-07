from mcp.server.fastmcp import FastMCP

mcp = FastMCP("KnoxJira", port=8004)

JIRA_ISSUES = {
    "PROJ-101": {
        "summary": "Fix login bug",
        "description": "Users cannot log in after password reset.",
        "status": "To Do"
    },
    "PROJ-102": {
        "summary": "Implement dark mode",
        "description": "Add dark mode support in UI settings.",
        "status": "In Progress"
    }
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
                "status": issue["status"]
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
async def create_jira_issue(project_key: str, summary: str, description: str) -> dict:
    """Creates a new Jira issue and returns the new issue key"""
    print(f"[LOG] create_jira_issue called with project_key={project_key}, summary={summary}, description={description}")
    new_id = f"{project_key.upper()}-{len(JIRA_ISSUES) + 101}"
    JIRA_ISSUES[new_id] = {
        "summary": summary,
        "description": description,
        "status": "To Do"
    }
    return {
        "status": "created",
        "issue_key": new_id,
        "summary": summary
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