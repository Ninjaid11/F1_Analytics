import requests
from bs4 import BeautifulSoup
import re
from src.config import get_settings

settings = get_settings()

class F1Scraper:

    @staticmethod
    def get_pilots(url="https://www.formula1.com/en/results/2026/drivers"):
        response = requests.get(url)

        if response.status_code != 200:
            return []

        soup = BeautifulSoup(response.text, "html.parser")
        rows = soup.find_all("tr")

        data = []
        seen = set()

        for row in rows:
            cols = row.find_all("td")

            if len(cols) >= 4:
                driver_raw = cols[1].get_text(strip=True)
                team = cols[3].get_text(strip=True)
                pts = cols[4].get_text(strip=True)

                # убираем код страны (ANT, RUS, NOR...)
                driver_clean = re.sub(r"[A-Z]{3}$", "", driver_raw).strip()

                parts = driver_clean.split(" ", 1)
                name = parts[0]
                surname = parts[1] if len(parts) > 1 else ""

                full_name = f"{name} {surname}"

                if full_name not in seen:
                    data.append({
                        "№": len(data) + 1,
                        "name": name,
                        "surname": surname,
                        "team": team,
                        "PTS": pts
                    })
                    seen.add(full_name)

        return data

    @staticmethod
    def get_results(race_url="https://www.formula1.com/en/results/2025/races"):
        response = requests.get(race_url)
        if response.status_code != 200:
            return []

        soup = BeautifulSoup(response.text, "html.parser")

        rows = soup.find_all("tr")[1:]

        results = []
        for row in rows:
            cols = row.find_all("td")
            if len(cols) >= 6:
                gp_tag = cols[0]

                img = gp_tag.find("svg")
                if img:
                    img.decompose()

                results.append({
                    "grand_prix": gp_tag.get_text(strip=True),
                    "date": cols[1].get_text(strip=True),
                    "winner": cols[2].get_text(strip=True)[:-3],
                    "team": cols[3].get_text(strip=True),
                    "laps": cols[4].get_text(strip=True),
                    "time": cols[5].get_text(strip=True),
                })

        return results


