# parser.py
import re
from datetime import datetime
import dateparser
from dateparser.search import search_dates

def parse_expenses(text):
    """
    Parse multiple expenses from one sentence.
    Example: 'today pizza 200, tea 50, sandwich 100'
    Returns list of dicts: [{date, item, price}, ...]
    """
    if not text:
        return []

    # Find date
    date = None
    try:
        found = search_dates(text, settings={'RELATIVE_BASE': datetime.now()})
        if found:
            date = found[0][1]
    except Exception:
        pass
    if not date:
        date = datetime.now()
    date_str = date.strftime("%Y-%m-%d")

    # Split by commas
    parts = text.split(",")
    expenses = []

    for part in parts:
        # Extract price
        price_match = re.search(r'(\d+(?:\.\d+)?)', part)
        price = float(price_match.group(1)) if price_match else 0.0

        # Remove numbers & currency words to keep item name
        item = re.sub(r'\d+(?:\.\d+)?', '', part)
        item = re.sub(r'\b(rs|rupees|rupee|₹)\b', '', item, flags=re.I)
        item = item.strip(" .-").strip()

        if item == "":
            item = "unknown"

        expenses.append({
            "date": date_str,
            "item": item,
            "price": round(price, 2)
        })

    return expenses
