
import sqlite3
from datetime import datetime

DB_NAME = "../database/tokenqueue.db"


# getting current date and time
def get_current_time():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


# setting up  database
def setup_database():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS tokens (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            display_id TEXT NOT NULL,
            status TEXT NOT NULL,
            issued_at TEXT NOT NULL,
            serving_started_at TEXT,
            served_at TEXT
        )
    """)

    # # Update DB to newer version code
    # cursor.execute("PRAGMA table_info(tokens)")
    # columns = [column[1] for column in cursor.fetchall()]

    # if "serving_started_at" not in columns:
    #     cursor.execute("""
    #         ALTER TABLE tokens
    #         ADD COLUMN serving_started_at TEXT
    #     """)

    conn.commit()
    conn.close()

    print("Database setup successful!")


# adding a new token
def add_token(display_id, status="waiting"):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    issued_at = get_current_time()

    cursor.execute("""
        INSERT INTO tokens (
            display_id,
            status,
            issued_at,
            serving_started_at,
            served_at
        )
        VALUES (?, ?, ?, NULL, NULL)
    """, (display_id, status, issued_at))

    token_id = cursor.lastrowid

    conn.commit()
    conn.close()

    return token_id


# change token status and record timestamps
def change_status(token_id, new_status):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    current_time = get_current_time()

    if new_status == "serving":
        cursor.execute("""
            UPDATE tokens
            SET status = ?, serving_started_at = ?
            WHERE id = ?
        """, (new_status, current_time, token_id))

    elif new_status == "completed":
        cursor.execute("""
            UPDATE tokens
            SET status = ?, served_at = ?
            WHERE id = ?
        """, (new_status, current_time, token_id))

    else:
        cursor.execute("""
            UPDATE tokens
            SET status = ?
            WHERE id = ?
        """, (new_status, token_id))

    updated = cursor.rowcount > 0

    conn.commit()
    conn.close()

    return updated


# Getting all tokens
def get_all_tokens():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            id,
            display_id,
            status,
            issued_at,
            serving_started_at,
            served_at
        FROM tokens
        ORDER BY id ASC
    """)

    rows = cursor.fetchall()

    conn.close()

    return rows


#  getting waiting tokens
def get_waiting_tokens():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
        SELECT *
        FROM tokens
        WHERE status = 'waiting'
        ORDER BY id ASC
    """)

    rows = cursor.fetchall()

    conn.close()

    return rows


#  displaying all tokens in table format
def display_tokens():
    tokens = get_all_tokens()

    headers = [
        "ID",
        "Token",
        "Status",
        "Issued At",
        "Serving Started At",
        "Served At"
    ]

    widths = [5, 10, 13, 21, 22, 21]

    total_width = sum(widths) + 3 * (len(widths) - 1)

    print("\n" + "=" * total_width)
    print("DIGITAL QUEUE MANAGEMENT SYSTEM".center(total_width))
    print("=" * total_width)

    # printing table headings
    print(" | ".join(
        headers[i].ljust(widths[i])
        for i in range(len(headers))
    ))

    print("-" * total_width)

    # Print records
    if not tokens:
        print("No tokens found.".center(total_width))
    else:
        for token in tokens:
            row = [
                str(token[0]),
                str(token[1]),
                str(token[2]),
                str(token[3] or "N/A"),
                str(token[4] or "N/A"),
                str(token[5] or "N/A")
            ]

            print(" | ".join(
                row[i].ljust(widths[i])
                for i in range(len(row))
            ))

    print("=" * total_width)


#  main program
if __name__ == "__main__":

    setup_database()

    # generating sample tokens
    token1 = add_token("A001")
    token2 = add_token("A002")
    token3 = add_token("A003")
    token4 = add_token("A004")
    

    print("\nTokens generated successfully!")

    # updating token statuses
    change_status(token1, "serving")
    change_status(token1, "completed")
    change_status(token2, "serving")
    change_status(token2, "completed")
    change_status(token3, "serving")
   

    # displaying all tokens
    display_tokens()
