# weather_server.py
from typing import List
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("KnoxMail", port=8002)

MAILBOX = {
    "unread": [
        {"id": "mail001", "from": "alice@example.com", "subject": "회의 일정 변경"},
        {"id": "mail002", "from": "bob@example.com", "subject": "청구서 알림"},
        {"id": "mail003", "from": "carol@example.com", "subject": "팀 점심 약속"},
        {"id": "mail004", "from": "dave@example.com", "subject": "보안 경고"},
        {"id": "mail005", "from": "eve@example.com", "subject": "성과 평가 일정"},
        {"id": "mail006", "from": "frank@example.com", "subject": "배포 상태 보고"}
    ],
    "detail": {
        "mail001": {"subject": "회의 일정 변경", "body": "회의 시간이 오후 3시로 변경되었습니다."},
        "mail002": {"subject": "청구서 알림", "body": "청구서 #1234를 결제해주세요."},
        "mail003": {"subject": "팀 점심 약속", "body": "점심은 12시 30분에 예정되어 있습니다."},
        "mail004": {"subject": "보안 경고", "body": "의심스러운 로그인이 감지되었습니다."},
        "mail005": {"subject": "성과 평가 일정", "body": "성과 평가는 이번 주 금요일로 예정되어 있습니다."},
        "mail006": {"subject": "배포 상태 보고", "body": "배포가 성공적으로 완료되었습니다."}
    }
}

@mcp.tool()
async def send_mail(recipient_email: str, subject: str, body: str) -> dict:
    """
    Sends an email with the specified recipient, subject, and body, and returns the result in JSON format
    recipient_email: str - The email address of the recipient (must be a valid email format))
    subject: str - The subject of the email
    body: str - The body content of the email
    """
    print(f"[LOG] send_mail called with recipient_id={recipient_email}, subject={subject}, body={body}")
    return {"status": "sent", "recipient": recipient_email, "subject": subject}

@mcp.tool()
async def get_unread_mails() -> dict:
    """Returns header information of all unread emails in JSON format"""
    print("[LOG] list_unread_mails called")
    return {"unread": MAILBOX["unread"]}

@mcp.tool()
async def read_mail_detail(mail_id: str) -> dict:
    """Returns the subject and body of the specified email ID in JSON format"""
    print(f"[LOG] read_mail_detail called with mail_id={mail_id}")
    if mail_id not in MAILBOX["detail"]:
        return {"error": "Invalid or missing mail ID."}
    mail = MAILBOX["detail"][mail_id]
    return {"subject": mail["subject"], "body": mail["body"]}


if __name__ == "__main__":
    mcp.run(transport="streamable-http")
