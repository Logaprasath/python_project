import os
import mysql.connector
from dotenv import load_dotenv
from tabulate import tabulate

load_dotenv()

def get_db_connection():
    return mysql.connector.connect(
        host=os.getenv('DB_HOST'),
        port=os.getenv('DB_PORT'),
        user=os.getenv('DB_USER'),
        password=os.getenv('DB_PASSWORD'),
        database=os.getenv('DB_NAME')
    )

def fetch_data(query):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute(query)
    result = cursor.fetchall()
    cursor.close()
    conn.close()
    return result

# Example usage:
if __name__ == "__main__":
    data = fetch_data("SELECT * FROM por_extracted_data LIMIT 10")
    table = tabulate(data, headers="keys", tablefmt="psql")
    print(table)