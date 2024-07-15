import sqlite3 

def main():
    try:
        # Connect to the database
        conn = sqlite3.connect('database.db')
        cur = conn.cursor()
        cur.execute('BEGIN TRANSACTION;')
        cur.execute('''
    DELETE FROM records
WHERE BATT_ID IN (
    SELECT BATT_ID
    FROM records
    ORDER BY BATT_ID
    LIMIT 47
);
''')
        cur.execute('COMMIT;')

# Print the number of rows deleted
        print("Number of rows deleted:", cur.rowcount)

    except sqlite3.Error as e:
        print("An error occurred:", e)

    finally:
        if conn:
            # Close the database connection
            conn.close()

main()