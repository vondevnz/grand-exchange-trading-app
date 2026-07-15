import asyncio
from app.fetch import import_latest

def audit():
    url = "https://prices.runescape.wiki/api/v1/osrs/latest"
    response = import_latest(url)
    data = response["data"]

    missing = {
        "high": 0,
        "low": 0,
        "highTime": 0,
        "lowTime": 0,
    }
    total = len(data)

    for item_id, price_data in data.items():
        for field in missing:
            if price_data.get(field) is None:
                missing[field] += 1

    print(f"Total items: {total}")
    for field, count in missing.items():
        pct = (count / total) * 100
        print(f"{field}: {count} missing ({pct:.1f}%)")

if __name__ == "__main__":
    audit()