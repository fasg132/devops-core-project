import os
import time
from flask import Flask
import psycopg2

app = Flask(__name__)

# Получаем данные для подключения к базе из переменных окружения 
(безопасность!)
DB_HOST = os.environ.get('DB_HOST', 'db')
DB_NAME = os.environ.get('DB_NAME', 'devops_db')
DB_USER = os.environ.get('DB_USER', 'postgres')
DB_PASSWORD = os.environ.get('DB_PASSWORD', 'secret_password')

def get_db_connection():
    # Нам нужно подождать, пока база данных запустится в Docker
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

# Инициализация таблицы в базе данных при старте
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
    
    # Добавляем запись о новом визите
    cursor.execute('INSERT INTO visits DEFAULT VALUES;')
    conn.commit()
    
    # Считаем общее количество визитов
    cursor.execute('SELECT COUNT(*) FROM visits;')
    count = cursor.fetchone()[0]
    
    cursor.close()
    conn.close()
    
    return f"<h1>Привет, это DevOps & Sec Пет-проект!</h1><p>Количество 
визитов этого сайта: {count}</p>"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
