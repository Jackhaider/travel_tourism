# view_bookings.py
import sqlite3
from pathlib import Path
from prettytable import PrettyTable

db = Path(__file__).resolve().parent / "app.db"
conn = sqlite3.connect(db)
cur = conn.cursor()

cur.execute("""
SELECT b.id, d.name AS destination, b.name, b.email, b.phone, 
       b.num_people, b.date, b.status, b.created_at
FROM booking b
JOIN destination d ON b.destination_id = d.id
ORDER BY b.created_at DESC
""")

rows = cur.fetchall()

# Table formatting
table = PrettyTable()
table.field_names = [
    "ID", "Destination", "Name", "Email", "Phone",
    "People", "Date", "Status", "Created At"
]

for row in rows:
    table.add_row(row)

print(table)

conn.close()
