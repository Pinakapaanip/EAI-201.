import requests
from bs4 import BeautifulSoup
import pandas as pd

url = "https://www.worldfootball.net/all_matches/fifa-wm-2018/"
response = requests.get(url)
soup = BeautifulSoup(response.text, "html.parser")

matches = soup.find_all("table", class_="standard_tabelle")
data = []

for table in matches:
    rows = table.find_all("tr")
    for row in rows[1:]:
        cols = row.find_all("td")
        if len(cols) >= 5:
            match_data = {
                "Date": cols[0].text.strip(),
                "Team1": cols[1].text.strip(),
                "Score": cols[2].text.strip(),
                "Team2": cols[3].text.strip(),
                "Stage": cols[4].text.strip()
            }
            data.append(match_data)

df_matches = pd.DataFrame(data)
df_matches.to_csv("fifa_matches_scraped.csv", index=False)
5
