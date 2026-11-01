import json
from datetime import date, timedelta
from persiantools.jdatetime import JalaliDate

DAYS = ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"]
HOLIDAYS = json.load(open("holidays.json", encoding="utf-8"))

PERSIAN_MONTHS = ["Farvardin", "Ordibehesht", "Khordad", "Tir", "Mordad", "Shahrivar",
                  "Mehr", "Aban", "Azar", "Dey", "Bahman", "Esfand"]

# gets the date and converts it to persian date
def get_today():
    d = date.today()
    return f"{d:%A, %Y-%m-%d} (Persian date {JalaliDate(d)})"

# how many days until the next given day (by name)
def next_weekday(name):
    d = date.today()
    delta = (DAYS.index(name.lower()) - d.weekday()) % 7 or 7
    n = d + timedelta(days=delta)
    return f"{n:%A, %Y-%m-%d} (Persian date {JalaliDate(n)})"

# how many days until the next given date (by date)
def days_until(date_str):
    return (date.fromisoformat(date_str) - date.today()).days

# x days from now 
def days_from_today(n):
    d = date.today() + timedelta(days=n)
    return f"{d:%A, %Y-%m-%d} (Persian date {JalaliDate(d)})"

# next holiday 
def next_holidays(count=3, days_off_only=True):
    today = date.today().isoformat()
    found = [e for e in HOLIDAYS if e["date"] >= today and (e["is_day_off"] or not days_off_only)]
    return [f'{e["date"]} ({e["weekday"]}): {e["name"]}' for e in found[:count]]


def next_month():
    today = date.today()
    g_first = (today.replace(day=1) + timedelta(days=32)).replace(day=1)
    g_last = (g_first + timedelta(days=32)).replace(day=1) - timedelta(days=1)
    j = JalaliDate(today)
    y, m = (j.year, j.month + 1) if j.month < 12 else (j.year + 1, 1)
    y2, m2 = (y, m + 1) if m < 12 else (y + 1, 1)
    p_first = JalaliDate(y, m, 1).to_gregorian()
    p_last = JalaliDate(y2, m2, 1).to_gregorian() - timedelta(days=1)
    return (f"Gregorian next month: {g_first:%B %Y}, {g_first} to {g_last}. "
            f"Persian next month: {PERSIAN_MONTHS[m-1]} {y}, {p_first} to {p_last}.")

def holidays_between(start, end, days_off_only=False):
    found = [e for e in HOLIDAYS if start <= e["date"] <= end and (e["is_day_off"] or not days_off_only)]
    return [f'{e["date"]} ({e["weekday"]}): {e["name"]}' + ("" if e["is_day_off"] else " [not a day off]")
            for e in found]


