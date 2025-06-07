from mcp.server.fastmcp import FastMCP

mcp = FastMCP("KnoxContact", port=8006)

# Full contact list with name, ID, phone, and email explicitly included
CONTACTS = [
    {
        "name": "김철수",
        "id": "chulsoo98",
        "phone": "010-1234-5678",
        "email": "chulsoo98@samsung.com"
    },
    {
        "name": "이영희",
        "id": "younghee21",
        "phone": "010-2345-6789",
        "email": "younghee21@samsung.com"
    },
    {
        "name": "김철수",  # Duplicate name
        "id": "coolsoo",
        "phone": "010-3456-7890",
        "email": "coolsoo@samsung.com"
    },
    {
        "name": "박민수",
        "id": "minsu91",
        "phone": "010-4567-8901",
        "email": "minsu91@samsung.com"
    },
    {
        "name": "이성준",
        "id": "sungjun87",
        "phone": "010-5678-9012",
        "email": "sungjun87@samsung.com"
    }
]

@mcp.tool()
async def search_by_name(name: str) -> dict:
    """Search contacts by exact name (supports duplicates)"""
    print(f"[LOG] search_by_name called with name={name}")
    matches = [c for c in CONTACTS if c["name"] == name]
    return {"results": matches}

@mcp.tool()
async def search_by_last_digits(phone_ending: str) -> dict:
    """Search contacts whose phone number ends with the given digits"""
    print(f"[LOG] search_by_last_digits called with phone_ending={phone_ending}")
    matches = [c for c in CONTACTS if c["phone"].replace("-", "").endswith(phone_ending)]
    return {"results": matches}

@mcp.tool()
async def search_by_id(user_id: str) -> dict:
    """Search contact by user ID"""
    print(f"[LOG] search_by_id called with user_id={user_id}")
    for c in CONTACTS:
        if c["id"] == user_id:
            return {"result": c}
    return {"error": "User ID not found."}

@mcp.tool()
async def search_by_email(email: str) -> dict:
    """Search contact by email address"""
    print(f"[LOG] search_by_email called with email={email}")
    for c in CONTACTS:
        if c["email"].lower() == email.lower():
            return {"result": c}
    return {"error": "Email not found."}
