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
async def send_mail(recipient_id: str, subject: str, body: str) -> dict:
    """Sends an email with the specified recipient, subject, and body, and returns the result in JSON format"""
    print(f"[LOG] send_mail called with recipient_id={recipient_id}, subject={subject}, body={body}")
    return {"status": "sent", "recipient": recipient_id, "subject": subject}

@mcp.tool()
async def get_unread_mails() -> dict:
    """Returns header information of all unread emails in JSON format"""
    print("[LOG] list_unread_mails called")
    return {"unread": MAILBOX["unread"]}

@mcp.tool()
async def read_mail_detail(mail_id: str) -> dict:
    """Returns the subject and body of the specified email ID in JSON format"""
    print(f"[LOG] read_mail_detail called with mail_id={mail_id}")
    if mail_id not in MAILBOX["read"]:
        return {"error": "Invalid or missing mail ID."}
    mail = MAILBOX["read"][mail_id]
    return {"subject": mail["subject"], "body": mail["body"]}


if __name__ == "__main__":
    mcp.run(transport="streamable-http")
