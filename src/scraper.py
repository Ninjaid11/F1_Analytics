import requests
from bs4 import BeautifulSoup
from src.config import get_settings

settings = get_settings()

class F1Scraper:

    @staticmethod
    def get_pilots(url="https://www.formula1.com/en/results/2025/drivers"):
        response = requests.get(url)
        if response.status_code != 200:
            return []

        soup = BeautifulSoup(response.text, "html.parser")

        first_names = soup.find_all("span", class_="max-lg:hidden")
        last_names = soup.find_all("span", class_="max-md:hidden")
        team_tags = soup.find_all("a", class_="flex gap-px-10")
        points_tags = soup.find_all("td", class_="typography-module_body-s-semibold__O2lOH Table-module_cell__3rpTC Table-module_no-wrap-text__CP2oI Table-module_flush-right__0xoPP")

        data = []
        seen = set()

        for i, (name, surname, team, pts) in enumerate(zip(first_names, last_names, team_tags, points_tags), 1):
            full_name = f"{name.text.strip()} {surname.text.strip()}"
            if full_name not in seen:
                data.append({
                    "№": i,
                    "name": name.text.strip(),
                    "surname": surname.text.strip(),
                    "team": team.text.strip(),
                    "PTS": pts.text.strip()
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


