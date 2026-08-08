# scripts/fetch_contributions.py
import json
import sys
import requests
from bs4 import BeautifulSoup

USERNAME = "AVIVASHISHTA29"  # replace with your username

def fetch_contributions(username):
    url = f"https://github.com/users/{username}/contributions"
    resp = requests.get(url, headers={"User-Agent": "Mozilla/5.0"})
    resp.raise_for_status()
    soup = BeautifulSoup(resp.text, "html.parser")

    days = []
    for cell in soup.select("td.ContributionCalendar-day, td[data-date]"):
        date = cell.get("data-date")
        level = cell.get("data-level", "0")
        if date:
            days.append({"date": date, "level": int(level)})

    total = sum(1 for d in days if d["level"] > 0)
    streak = 0
    for d in reversed(days):
        if d["level"] > 0:
            streak += 1
        else:
            break

    data = {
        "days": days,
        "total_contributions": total,
        "current_streak": streak,
    }
    with open("data/contributions.json", "w") as f:
        json.dump(data, f, indent=2)
    print(f"Saved data/contributions.json with {len(days)} days")

if __name__ == "__main__":
    fetch_contributions(sys.argv[1] if len(sys.argv) > 1 else USERNAME)