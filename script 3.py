import pandas as pd

# Read yesterday's and today's CSVs
yesterday = pd.read_csv("yesterday.csv")
today = pd.read_csv("today.csv")

# Merge on unique ID to align rows
merged = pd.merge(yesterday, today, on="id", suffixes=('_yest', '_today'))

# Find rows where any column (except id) has changed
changed_rows = merged[
    (merged.filter(like='_yest') != merged.filter(like='_today')).any(axis=1)
]

# Display changes
for _, row in changed_rows.iterrows():
    print(f"ID: {row['id']}")
    for col in [c for c in merged.columns if '_yest' in c]:
        base_col = col.replace('_yest', '')
        old_val = row[f"{base_col}_yest"]
        new_val = row[f"{base_col}_today"]
        if old_val != new_val:
            print(f" - {base_col}: '{old_val}' → '{new_val}'")
    print()
