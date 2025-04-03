import sqlite3

def create_database():
    conn = sqlite3.connect('database.db')
    c = conn.cursor()

    # Авиакомпании
    c.execute('''CREATE TABLE IF NOT EXISTS airlines(
                 id INTEGER PRIMARY KEY,
                 name TEXT UNIQUE)''')
    
    # Основные тарифы
    c.execute('''CREATE TABLE IF NOT EXISTS tariffs(
                 id INTEGER PRIMARY KEY,
                 airline_id INTEGER,
                 tariff_name TEXT,
                 free_baggage_weight INTEGER,
                 FOREIGN KEY(airline_id) REFERENCES airlines(id))''')
    
    # Доп. сборы за перевес
    c.execute('''CREATE TABLE IF NOT EXISTS overweight_fees(
                 id INTEGER PRIMARY KEY,
                 airline_id INTEGER,
                 min_weight INTEGER,
                 max_weight INTEGER,
                 fee INTEGER,
                 FOREIGN KEY(airline_id) REFERENCES airlines(id))''')
    
    # Дополнительные услуги
    c.execute('''CREATE TABLE IF NOT EXISTS extra_services(
                 id INTEGER PRIMARY KEY,
                 airline_id INTEGER,
                 service_name TEXT,
                 fee INTEGER,
                 FOREIGN KEY(airline_id) REFERENCES airlines(id))''')

    conn.commit()
    conn.close()

if __name__ == "__main__":
    create_database()