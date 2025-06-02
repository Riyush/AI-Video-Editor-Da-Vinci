# This file creates functionality to connect to a database, and write the contents
# of a specific table to a file. I will hash out any Blob fields. This way, I can
# take a snapshot of the database before and after I make a specific change 
# and identify which database fields correspond with certain edits on Resolve

import sqlite3
import hashlib
import json
from pathlib import Path

db_path = "/Users/riyush/Documents/Resolve Project Library/Resolve Projects/Users/guest/Projects/examples/Project.db"

tables_of_interest = ["Sm2TiItem", "Sm2Sequence",]


def hash_blob(blob):
    if blob is None:
        return None
    if isinstance(blob, str):
        blob = blob.encode('utf-8')  # Convert string to bytes
    return hashlib.sha256(blob).hexdigest()

def dump_table_to_file(db_path, table_name, state):
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()

    try:
        # Fetch column info
        cur.execute(f"PRAGMA table_info({table_name})")
        col_info = cur.fetchall()
        blob_cols = {col['name'] for col in col_info if col['type'].upper() == 'BLOB'}

        # Fetch table rows
        cur.execute(f"SELECT * FROM {table_name}")
        rows = cur.fetchall()
    except Exception as E:
        print(f"Error: {E}")

    # Process each row
    output_data = []
    for row in rows:
        row_dict = {}
        for key in row.keys():
            value = row[key]
            if key in blob_cols:
                row_dict[key] = hash_blob(value)
            else:
                row_dict[key] = value
        output_data.append(row_dict)

    # Determine state name
    state_str = "before" if state else "after"

     # Construct path
    output_dir = Path(f"/Users/riyush/Documents/AI-Video-Editor-Da-Vinci/reverse_engineering_database/logs/{table_name}")
    output_dir.mkdir(parents=True, exist_ok=True)  # Make sure dirs exist
    output_file = output_dir / f"{state_str}5.json"

    # Write to file
    Path(output_file).write_text(json.dumps(output_data, indent=2), encoding='utf-8')
    print(f"✅ Table '{table_name}' dumped to {output_file}")

    conn.close()

if __name__ == "__main__":
    for table in tables_of_interest:
        dump_table_to_file(db_path, table, False)