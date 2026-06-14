import os
import time
from flask import Flask
import psycopg2

app = Flask(__name__)

# Fetch database connection details from environment variables
DB_HOST = os.environ.get('DB_HOST', 'db')
DB_NAME = os.environ.get('DB_NAME', 'devops_db')
DB_USER = os.environ.get('DB_USER', 'postgres')
DB_PASSWORD = os.environ.get('DB_PASSWORD', 'secret_password')

def get_db_connection():
    # Retry mechanism to wait until PostgreSQL container is ready
    retries = 5
    while True:
        try:
            conn = psycopg2.connect(
                host=DB_HOST,
                database=DB_NAME,
                user=DB_USER,
                password=DB_PASSWORD
            )
            return conn
        except psycopg2.OperationalError as e:
            if retries == 0:
                raise e
            retries -= 1
            time.sleep(2)

# Initialize database schema on startup
conn = get_db_connection()
cursor = conn.cursor()
cursor.execute('''
    CREATE TABLE IF NOT EXISTS visits (
        id SERIAL PRIMARY KEY,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
''')
conn.commit()
cursor.close()
conn.close()

@app.route('/')
def hello():
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Log a new visit
    cursor.execute('INSERT INTO visits DEFAULT VALUES;')
    conn.commit()
    
    # Count total visits
    cursor.execute('SELECT COUNT(*) FROM visits;')
    count = cursor.fetchone()[0]
    
    cursor.close()
    conn.close()
    
    return f"<h1>Hello, this is DevOps & Sec Pet Project!</h1><p>Total page visits: {count}</p>"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)