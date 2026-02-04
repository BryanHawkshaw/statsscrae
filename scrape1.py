# %%
import pandas as pd
import requests
from bs4 import BeautifulSoup
import re

# %%
url = "https://www.transfermarkt.com/afc-bournemouth_liverpool-fc/statistik/spielbericht/4626019"
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36"
}

data = requests.get(url, headers=headers)
data.text

# %%
soup = BeautifulSoup(data.text, 'html.parser')
possesion_stat = soup.select_one("div.sb-st-ballbesitz")
stats = soup.select("div.sb-statistik")

# %%
stats_data = []
possession_values = []

for i in stats:
    left = i.find("li", class_="sb-statistik-heim")
    right = i.find("li", class_="sb-statistik-gast")
    
    if left and right:
        stats_data.append({
            "stat_home": left.text.strip(),
            "stat_away": right.text.strip()
        })

# %%
if possesion_stat:
    for t in possesion_stat.find_all("tspan"):
        match = re.search(r"\d+", t.text)
        if match:
            possession_values.append((match.group))
            
home_possession = possession_values[0] if len(possession_values) else None
away_possession = possession_values[1] if len(possession_values) else None

# %%
df_stats = pd.DataFrame(stats_data)
possession_row = {
    "stat_home" : home_possession,
    "stat_away" : away_possession
}

df_stats = pd.concat(
    [pd.DataFrame([possession_row]), df_stats], ignore_index=True
)
df_stats


