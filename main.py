import sys
import sqlite3
from PyQt6.QtWidgets import (
    QApplication, QWidget, QLabel, QPushButton, QVBoxLayout,
    QComboBox, QLineEdit, QCheckBox
)
from PyQt6.QtGui import QPixmap, QIcon
from PyQt6.QtCore import Qt

class BaggageCalculator(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Калькулятор стоимости багажа")
        self.setGeometry(200, 100, 500, 400)
        self.setWindowIcon(QIcon("assets/ARlogo.ico"))
        self.conn = sqlite3.connect('database.db')
        self.dynamic_checkboxes = []
        self.init_ui()
        self.load_airlines()

    def init_ui(self):
        layout = QVBoxLayout()
        
        # Логотип
        self.logo = QLabel(self)
        pixmap = QPixmap("assets/BaggageCost.png").scaled(1000, 500, Qt.AspectRatioMode.KeepAspectRatio)
        self.logo.setPixmap(pixmap)
        self.logo.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.logo)

        # Выбор авиакомпании
        layout.addWidget(QLabel("Выберите авиакомпанию:"))
        self.airline_combo = QComboBox()
        layout.addWidget(self.airline_combo)

        # Выбор тарифа
        layout.addWidget(QLabel("Выберите тариф:"))
        self.tariff_combo = QComboBox()
        layout.addWidget(self.tariff_combo)

        # Ввод веса
        layout.addWidget(QLabel("Вес багажа (кг):"))
        self.weight_input = QLineEdit()
        self.weight_input.setPlaceholderText("Введите вес")
        layout.addWidget(self.weight_input)

        # Статические чекбоксы
        self.hand_luggage = QCheckBox("Ручная кладь")
        self.oversized = QCheckBox("Сверхнормативный багаж")
        self.sports = QCheckBox("Спортивный инвентарь")
        layout.addWidget(self.hand_luggage)
        layout.addWidget(self.oversized)
        layout.addWidget(self.sports)

        # Динамические чекбоксы
        self.dynamic_services_label = QLabel("Дополнительные услуги:")
        layout.addWidget(self.dynamic_services_label)
        self.dynamic_container = QWidget()
        self.dynamic_layout = QVBoxLayout(self.dynamic_container)
        layout.addWidget(self.dynamic_container)

        # Кнопки
        self.calculate_btn = QPushButton("Рассчитать стоимость")
        self.calculate_btn.clicked.connect(self.calculate_price)
        layout.addWidget(self.calculate_btn)

        # Результат
        self.result_label = QLabel("Стоимость: 0 руб.")
        self.result_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.result_label)

        # Сброс
        self.reset_btn = QPushButton("Сбросить")
        self.reset_btn.clicked.connect(self.reset_fields)
        layout.addWidget(self.reset_btn)

        self.setLayout(layout)

    def load_airlines(self):
        self.airline_combo.clear()
        c = self.conn.cursor()
        c.execute("SELECT id, name FROM airlines")
        for airline_id, name in c.fetchall():
            self.airline_combo.addItem(name, userData=airline_id)
        self.airline_combo.currentIndexChanged.connect(self.update_data)
        self.update_data()

    def update_data(self):
        self.load_tariffs()
        self.load_services()

    def load_tariffs(self):
        airline_id = self.airline_combo.currentData()
        c = self.conn.cursor()
        c.execute("SELECT tariff_name FROM tariffs WHERE airline_id=?", (airline_id,))
        self.tariff_combo.clear()
        self.tariff_combo.addItems([row[0] for row in c.fetchall()])

    def load_services(self):
        # Очистка предыдущих чекбоксов
        for cb in self.dynamic_checkboxes:
            cb.deleteLater()
        self.dynamic_checkboxes.clear()

        # Загрузка новых услуг
        airline_id = self.airline_combo.currentData()
        c = self.conn.cursor()
        c.execute("SELECT service_name FROM extra_services WHERE airline_id=?", (airline_id,))
        
        for service in c.fetchall():
            cb = QCheckBox(service[0])
            self.dynamic_layout.addWidget(cb)
            self.dynamic_checkboxes.append(cb)

    def calculate_price(self):
        try:
            weight = float(self.weight_input.text())
            airline_id = self.airline_combo.currentData()
            tariff = self.tariff_combo.currentText()
            
            base_price = self.get_base_price(airline_id, tariff, weight)
            extra_price = self.get_extra_charges(airline_id)
            
            total = base_price + extra_price
            self.result_label.setText(f"Итоговая стоимость: {total} руб.")
            
        except ValueError:
            self.result_label.setText("Ошибка: Некорректный вес")
        except Exception as e:
            self.result_label.setText(f"Ошибка расчета: {str(e)}")

    def get_base_price(self, airline_id, tariff_name, weight):
        c = self.conn.cursor()
        c.execute('''SELECT free_baggage_weight 
                   FROM tariffs 
                   WHERE airline_id=? AND tariff_name=?''',
                (airline_id, tariff_name))
        
        result = c.fetchone()
        if not result:
            return 0
        
        free_limit = result[0]
        if weight <= free_limit:
            return 0
        
        c.execute('''SELECT fee FROM overweight_fees 
                   WHERE airline_id=? AND ? > min_weight AND ? <= max_weight''',
                (airline_id, weight, weight))
        
        result = c.fetchone()
        return result[0] if result else 0

    def get_extra_charges(self, airline_id):
        total = 0
        c = self.conn.cursor()
        for cb in self.dynamic_checkboxes + [self.hand_luggage, self.oversized, self.sports]:
            if cb.isChecked():
                c.execute('''SELECT fee FROM extra_services 
                          WHERE airline_id=? AND service_name=?''',
                       (airline_id, cb.text()))
                result = c.fetchone()
                if result:
                    total += result[0]
        return total

    def reset_fields(self):
        self.weight_input.clear()
        for cb in self.dynamic_checkboxes + [self.hand_luggage, self.oversized, self.sports]:
            cb.setChecked(False)
        self.result_label.setText("Стоимость: 0 руб.")

    def closeEvent(self, event):
        self.conn.close()
        super().closeEvent(event)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = BaggageCalculator()
    window.show()
    sys.exit(app.exec())