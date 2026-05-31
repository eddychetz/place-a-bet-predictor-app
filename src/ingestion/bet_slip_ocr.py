import pytesseract
import cv2
import pandas as pd
import re

# ---------------------------
# Load image
# ---------------------------
image_path = "bet_slip.jpg"
img = cv2.imread(image_path)

# Convert to grayscale (improves OCR)
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# OCR extraction
text = pytesseract.image_to_string(gray)

print("RAW OCR OUTPUT:\n", text)


# ---------------------------
# Parsing function
# ---------------------------
def parse_bet_slips(text):
    entries = text.split("MULTIPLE")

    records = []

    for i, entry in enumerate(entries[1:], start=1):

        try:
            # selection count
            selection_count = int(re.search(r"\((\d+)\)", entry).group(1))

            # payout
            payout_match = re.search(r"R\s*([\d\s,]+)", entry)
            payout = payout_match.group(1).replace(" ", "").replace(",", ".") if payout_match else None

            # stake
            stake_match = re.search(r"/R\s*([\d,]+)", entry)
            stake = stake_match.group(1).replace(",", ".") if stake_match else None

            # match name
            match_match = re.search(r"Full Time\s*-\s*(.+)", entry)
            match_name = match_match.group(1).strip() if match_match else None

            # date + time
            date_match = re.search(r"(\d{2} \w+ \d{4}) \| (\d{2}:\d{2})", entry)
            date = date_match.group(1) if date_match else None
            time = date_match.group(2) if date_match else None

            # status
            status = "LOSING" if "LOSING" in entry else "UNKNOWN"

            records.append({
                "bet_id": i,
                "bet_type": "MULTIPLE",
                "selection_count": selection_count,
                "payout": float(payout) if payout else None,
                "stake": float(stake) if stake else None,
                "market": "Full Time",
                "match_name": match_name,
                "bet_date": date,
                "bet_time": time,
                "status": status,
                "currency": "ZAR"
            })

        except Exception as e:
            print(f"Skipping entry due to error: {e}")

    return pd.DataFrame(records)


# ---------------------------
# Convert to dataframe
# ---------------------------
df = parse_bet_slips(text)

print(df.head())

# Save
df.to_csv("parsed_bet_slip.csv", index=False)