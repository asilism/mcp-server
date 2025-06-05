# weather_server.py
from typing import List
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("KnoxMail", port=8002)

MAILBOX = {
    "unread": [
        {"id": "mail001", "from": "alice@example.com", "subject": "Meeting update"},
        {"id": "mail002", "from": "bob@example.com", "subject": "Invoice reminder"},
    ],
    "read": {
        "mail001": {"subject": "Meeting update", "body": "Meeting is moved to 3 PM."},
        "mail002": {"subject": "Invoice reminder", "body": "Please pay invoice #1234."},
    }
}

@mcp.tool()
async def list_unread_mails() -> dict:
    """ 읽지 않은 모든 메일의 헤더 정보를 JSON 형식으로 반환합니다"""
    print("[LOG] list_unread_mails called")
    return {"unread": MAILBOX["unread"]}

@mcp.tool()
async def read_mail_detail(mail_id: str) -> dict:
    """ 지정한 메일 ID에 해당하는 메일의 제목과 본문을 JSON 형식으로 반환합니다"""
    print(f"[LOG] read_mail_detail called with mail_id={mail_id}")
    if mail_id not in MAILBOX["read"]:
        return {"error": "Invalid or missing mail ID."}
    mail = MAILBOX["read"][mail_id]
    return {"subject": mail["subject"], "body": mail["body"]}

@mcp.tool()
async def send_mail(recipient_id: str, subject: str, body: str) -> dict:
    """ 지정한 수신자에게 제목과 본문을 포함한 메일을 발송하고, 결과 상태를 JSON 형식으로 반환합니다"""
    print(f"[LOG] send_mail called with recipient_id={recipient_id}, subject={subject}, body={body}")
    return {"status": "sent", "recipient": recipient_id, "subject": subject}

if __name__ == "__main__":
    mcp.run(transport="streamable-http")
