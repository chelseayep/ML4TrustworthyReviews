import json
import csv

# Load your JSON file
with open('data/processed/lalaal.json', 'r') as f:
    data = json.load(f)

# If your JSON is a list of dicts:
with open('data/processed/kakaka.csv', 'w', newline='', encoding='utf-8') as f:
    writer = csv.DictWriter(f, fieldnames=list(data[0].keys()) + ['annotation'])
    writer.writeheader()
    for row in data:
        row['annotation'] = ''  # Add empty annotation column
        writer.writerow(row)