import os
import sys
import psycopg2

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.auth import hash_password

conn = psycopg2.connect(os.getenv("DATABASE_URL"))
cur = conn.cursor()

# Example: update one user
plain_password = "admin456"
hashed = hash_password(plain_password)

cur.execute("UPDATE users SET password = %s WHERE email = %s", (hashed, "admin@pcst.com"))
conn.commit()
cur.close()
conn.close()
