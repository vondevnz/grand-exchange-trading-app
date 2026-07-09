import json

# Load the original JSON file
with open("mappings/items.json", "r", encoding="utf-8") as file:
	data = json.load(file)

# Reverse the mapping 'name' -> 'id'
reversed_data = {str(v): k for k, v in data.items()}

# Save to new file
with open("mappings/reversedItems.json", "w", encoding="utf-8") as file:
	json.dump(reversed_data, file, indent=4)