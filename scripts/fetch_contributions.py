# scripts/fetch_contributions.py
import os
import sys
import json
import requests

USERNAME = "Kopichino"

QUERY = """
query($login: String!) {
  user(login: $login) {
    contributionsCollection {
      contributionCalendar {
        totalContributions
        weeks {
          contributionDays {
            date
            contributionCount
            weekday
          }
        }
      }
    }
  }
}
"""

def fetch_contributions(username):
    token = os.environ.get("CONTRIB_TOKEN") or os.environ.get("GITHUB_TOKEN")
    if not token:
        print("ERROR: set CONTRIB_TOKEN env var (a GitHub PAT with read:user scope)")
        sys.exit(1)

    resp = requests.post(
        "https://api.github.com/graphql",
        json={"query": QUERY, "variables": {"login": username}},
        headers={"Authorization": f"bearer {token}"},
    )
    resp.raise_for_status()
    data = resp.json()

    weeks = data["data"]["user"]["contributionsCollection"]["contributionCalendar"]["weeks"]
    total = data["data"]["user"]["contributionsCollection"]["contributionCalendar"]["totalContributions"]

    days = []
    for week in weeks:
        for day in week["contributionDays"]:
            count = day["contributionCount"]
            level = 0 if count == 0 else min(5, 1 + count // 3)
            days.append({"date": day["date"], "level": level, "count": count})

    streak = 0
    for d in reversed(days):
        if d["count"] > 0:
            streak += 1
        else:
            break

    out = {"days": days, "total_contributions": total, "current_streak": streak}
    with open("data/contributions.json", "w") as f:
        json.dump(out, f, indent=2)
    print(f"Saved data/contributions.json with {len(days)} days, {total} total")

if __name__ == "__main__":
    fetch_contributions(sys.argv[1] if len(sys.argv) > 1 else USERNAME)