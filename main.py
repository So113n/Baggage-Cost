import sys
from PyQt6.QtWidgets import (
    QApplication, QWidget, QLabel, QPushButton, QVBoxLayout,
    QComboBox, QLineEdit, QCheckBox, QHBoxLayout
)
from PyQt6.QtGui import QPixmap, QIcon
from PyQt6.QtCore import Qt


class BaggageCalculator(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Калькулятор стоимости багажа")
        self.setGeometry(200, 100, 500, 400)
        self.setWindowIcon(QIcon("assets/icon.png"))
        self.initUI()
    
    def initUI(self):
        layout = QVBoxLayout()
        
        # Логотип
        self.logo = QLabel(self)
        pixmap = QPixmap("assets/logo.png").scaled(200, 100, Qt.AspectRatioMode.KeepAspectRatio)
        self.logo.setPixmap(pixmap)
        self.logo.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.logo)
        
        # Выпадающий список авиакомпаний
        self.airline_label = QLabel("Выберите авиакомпанию:")
        self.airline_combo = QComboBox()
        self.airline_combo.addItems(["Аэрофлот", "S7 Airlines", "Utair", "Победа", "Ural Airlines"])
        
        # Выпадающий список тарифов
        self.tariff_label = QLabel("Выберите тариф:")
        self.tariff_combo = QComboBox()
        self.tariff_combo.addItems(["Эконом", "Комфорт", "Бизнес"])
        
        # Поле ввода веса багажа
        self.weight_label = QLabel("Вес багажа (кг):")
        self.weight_input = QLineEdit()
        self.weight_input.setPlaceholderText("Введите вес")
        
        # Чекбоксы для доп. опций
        self.hand_luggage = QCheckBox("Ручная кладь")
        self.oversized = QCheckBox("Сверхнормативный багаж")
        self.sports = QCheckBox("Спортивный инвентарь")
        
        # Кнопка расчета стоимости
        self.calculate_button = QPushButton("Рассчитать стоимость")
        self.calculate_button.clicked.connect(self.calculate_price)
        
        # Поле вывода стоимости
        self.result_label = QLabel("Стоимость: 0 руб.")
        self.result_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        # Кнопка сброса
        self.reset_button = QPushButton("Сбросить")
        self.reset_button.clicked.connect(self.reset_fields)
        
        # Размещаем элементы в макете
        layout.addWidget(self.airline_label)
        layout.addWidget(self.airline_combo)
        layout.addWidget(self.tariff_label)
        layout.addWidget(self.tariff_combo)
        layout.addWidget(self.weight_label)
        layout.addWidget(self.weight_input)
        layout.addWidget(self.hand_luggage)
        layout.addWidget(self.oversized)
        layout.addWidget(self.sports)
        layout.addWidget(self.calculate_button)
        layout.addWidget(self.result_label)
        layout.addWidget(self.reset_button)
        
        self.setLayout(layout)

    def calculate_price(self):
        self.result_label.setText("Расчет пока не реализован")
    
    def reset_fields(self):
        self.weight_input.clear()
        self.hand_luggage.setChecked(False)
        self.oversized.setChecked(False)
        self.sports.setChecked(False)
        self.result_label.setText("Стоимость: 0 руб.")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = BaggageCalculator()
    window.show()
    sys.exit(app.exec())
