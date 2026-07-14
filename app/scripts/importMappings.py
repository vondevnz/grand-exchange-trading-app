from app.fetch import import_latest
import json

url = "https://prices.runescape.wiki/api/v1/osrs/mapping"

result = import_latest(url)

# Save to new file
with open("app/mappings/mappingsData.json", "w", encoding="utf-8") as file:
	json.dump(result, file, indent=4)