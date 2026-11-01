# imports the libraries
import json
import openai
from calendar_rag import search
from date_tools import (get_today, next_weekday, days_until, days_from_today,
                        next_month, next_holidays, holidays_between)


# defines the tools 
def tool(name, desc, props=None, required=None):
    return {"type": "function", "function": {
        "name": name, "description": desc,
        "parameters": {"type": "object", "properties": props or {}, "required": required or []}}}

# tool registries (describe the tools)
TOOLS = [
    tool("get_today", "Get today's date and weekday, with the Persian date"),
    tool("next_weekday", "Date of the next given weekday, e.g. wednesday",
         {"name": {"type": "string"}}, ["name"]),
    tool("days_until", "Number of days from today until a date in YYYY-MM-DD format",
         {"date_str": {"type": "string"}}, ["date_str"]),
    tool("days_from_today", "The date that is n days from today. Negative n goes into the past",
         {"n": {"type": "integer"}}, ["n"]),
    tool("next_month", "Start and end dates of next month in the Gregorian and Persian calendars"),
    tool("next_holidays", "The next upcoming official holidays (days off)",
         {"count": {"type": "integer"}}),
    tool("holidays_between", "List holidays and occasions between two dates in YYYY-MM-DD format",
         {"start": {"type": "string"}, "end": {"type": "string"}}, ["start", "end"]),
]

#calls functions for the demanded action 
FUNCS = {
    "get_today": get_today,
    "next_weekday": next_weekday,
    "days_until": days_until,
    "days_from_today": days_from_today,
    "next_month": next_month,
    "next_holidays": next_holidays,
    "holidays_between": holidays_between,
}

