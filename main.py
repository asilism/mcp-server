# main.py
from multiprocessing import Process
from server.knox_mail import mcp as mail_mcp
from server.knox_calendar import mcp as calendar_mcp
from server.weather_server import mcp as weather_mcp
from server.jira_integration import mcp as jira_mcp
from server.knox_contact import mcp as contact_mcp

def run_mail():
    mail_mcp.run(transport="streamable-http")

def run_calendar():
    calendar_mcp.run(transport="streamable-http")

def run_weather():
    weather_mcp.run(transport="streamable-http")

def run_jira():
    jira_mcp.run(transport="streamable-http")

def run_contact():
    contact_mcp.run(transport="streamable-http")

if __name__ == "__main__":
    processes = [
        Process(target=run_mail),
        Process(target=run_calendar),
        Process(target=run_weather),
        Process(target=run_jira),
        Process(target=run_contact)
    ]

    for p in processes:
        p.start()

    for p in processes:
        p.join()