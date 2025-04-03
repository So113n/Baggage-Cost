import sqlite3

def populate_data():
    conn = sqlite3.connect('database.db')
    c = conn.cursor()

    # Очистка таблиц (опционально)
    c.execute("DELETE FROM airlines")
    c.execute("DELETE FROM tariffs")
    c.execute("DELETE FROM overweight_fees")
    c.execute("DELETE FROM extra_services")

    # Добавление авиакомпаний
    airlines_data = [
        ('Аэрофлот',),
        ('S7 Airlines',),
        ('Utair',),
        ('Победа',),
        ('Ural Airlines',)
    ]
    c.executemany("INSERT INTO airlines (name) VALUES (?)", airlines_data)

    # Данные для всех авиакомпаний
    companies = [
        {
            'name': 'Аэрофлот',
            'tariffs': [
                ('Бизнес', 32),
                ('Комфорт', 23),
                ('Эконом', 20)
            ],
            'overweight': [
                (23, 32, 3000),
                (32, 50, 6000)
            ],
            'services': [
                ('Негабаритный багаж', 5000),
                ('Спортивный инвентарь', 2500),
                ('Животное в салоне', 4000)
            ]
        },
        {
            'name': 'S7 Airlines',
            'tariffs': [
                ('Эконом Basic', 0),
                ('Эконом Standard', 23),
                ('Бизнес', 32)
            ],
            'overweight': [
                (23, 32, 1500),
                (32, 50, 3000)
            ],
            'services': [
                ('Негабаритный багаж', 2500),
                ('Перевозка животных', 4000),
                ('Приоритетная посадка', 1000)
            ]
        },
        {
            'name': 'Utair',
            'tariffs': [
                ('Эконом', 20),
                ('Комфорт', 25),
                ('Бизнес', 30)
            ],
            'overweight': [
                (20, 30, 2000),
                (30, 50, 4000)
            ],
            'services': [
                ('Негабаритный багаж', 3000),
                ('Дополнительное место', 4500)
            ]
        },
        {
            'name': 'Победа',
            'tariffs': [
                ('Базовый', 0),
                ('Стандарт', 10)
            ],
            'overweight': [
                (10, 20, 15)  # руб/кг
            ],
            'services': [
                ('Дополнительная сумка', 500),
                ('Выбор места', 300)
            ]
        },
        {
            'name': 'Ural Airlines',
            'tariffs': [
                ('Эконом', 20),
                ('Бизнес', 30)
            ],
            'overweight': [
                (20, 30, 2500),
                (30, 50, 5000)
            ],
            'services': [
                ('Негабаритный багаж', 4000),
                ('Спортивное снаряжение', 3500)
            ]
        }
    ]

    for company in companies:
        # Получаем ID авиакомпании
        c.execute("SELECT id FROM airlines WHERE name = ?", (company['name'],))
        airline_id = c.fetchone()[0]

        # Добавляем тарифы
        tariffs_data = [(airline_id, name, weight) for name, weight in company['tariffs']]
        c.executemany("INSERT INTO tariffs (airline_id, tariff_name, free_baggage_weight) VALUES (?,?,?)", tariffs_data)

        # Добавляем перевес
        overweight_data = [(airline_id, min_w, max_w, fee) for min_w, max_w, fee in company['overweight']]
        c.executemany("INSERT INTO overweight_fees (airline_id, min_weight, max_weight, fee) VALUES (?,?,?,?)", overweight_data)

        # Добавляем услуги
        services_data = [(airline_id, name, fee) for name, fee in company['services']]
        c.executemany("INSERT INTO extra_services (airline_id, service_name, fee) VALUES (?,?,?)", services_data)

    conn.commit()
    conn.close()
    print("База данных успешно заполнена!")

if __name__ == "__main__":
    populate_data()