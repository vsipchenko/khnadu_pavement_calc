from dataclasses import dataclass
from typing import Dict


@dataclass
class City:
    """
    Зберігає кліматичні параметри для конкретного міста.

    Args:
        name (str): Назва міста
        soil_freezing_depth__Z_H_max (float): Глибина промерзання ґрунту
        climate_index__a_0 (float): Кліматичний показник α0
    """
    name: str
    soil_freezing_depth__Z_H_max: float
    climate_index__a_0: float


class CityTable:
    """
    Таблиця міст з їх характеристиками.

    Source:
        ГБН В.2.3-37641918-559:2019, рисунок 7.2
    """

    def __init__(self):
        self._cities: Dict[str, City] = {
            'київ':             City('Київ', soil_freezing_depth__Z_H_max=0.95, climate_index__a_0=0.65),
            'харків':           City('Харків', soil_freezing_depth__Z_H_max=1.00, climate_index__a_0=0.95),
            'львів':            City('Львів', soil_freezing_depth__Z_H_max=0.85, climate_index__a_0=0.70),
            'одеса':            City('Одеса', soil_freezing_depth__Z_H_max=0.65, climate_index__a_0=0.70),
            'дніпро':           City('Дніпро', soil_freezing_depth__Z_H_max=0.85, climate_index__a_0=0.85),
            'донецьк':          City('Донецьк', soil_freezing_depth__Z_H_max=0.90, climate_index__a_0=0.90),
            'луцьк':            City('Луцьк', soil_freezing_depth__Z_H_max=0.80, climate_index__a_0=0.60),
            'ужгород':          City('Ужгород', soil_freezing_depth__Z_H_max=0.65, climate_index__a_0=0.55),
            'чернігів':         City('Чернігів', soil_freezing_depth__Z_H_max=1.10, climate_index__a_0=0.90),
            'суми':             City('Суми', soil_freezing_depth__Z_H_max=1.05, climate_index__a_0=1.00),
            'полтава':          City('Полтава', soil_freezing_depth__Z_H_max=0.95, climate_index__a_0=0.90),
            'черкаси':          City('Черкаси', soil_freezing_depth__Z_H_max=0.90, climate_index__a_0=0.80),
            'вінниця':          City('Вінниця', soil_freezing_depth__Z_H_max=0.85, climate_index__a_0=0.50),
            'житомир':          City('Житомир', soil_freezing_depth__Z_H_max=0.90, climate_index__a_0=0.55),
            'хмельницький':     City('Хмельницький', soil_freezing_depth__Z_H_max=0.85, climate_index__a_0=0.50),
            'тернопіль':        City('Тернопіль', soil_freezing_depth__Z_H_max=0.85, climate_index__a_0=0.55),
            'рівне':            City('Рівне', soil_freezing_depth__Z_H_max=0.85, climate_index__a_0=0.60),
            'івано-франківськ': City('Івано-Франківськ', soil_freezing_depth__Z_H_max=0.90, climate_index__a_0=0.70),
            'чернівці':         City('Чернівці', soil_freezing_depth__Z_H_max=0.75, climate_index__a_0=0.60),
            'миколаїв':         City('Миколаїв', soil_freezing_depth__Z_H_max=0.70, climate_index__a_0=0.75),
            'херсон':           City('Херсон', soil_freezing_depth__Z_H_max=0.70, climate_index__a_0=0.70),
            'запоріжжя':        City('Запоріжжя', soil_freezing_depth__Z_H_max=0.80, climate_index__a_0=0.85),
            'кропивницький':    City('Кропивницький', soil_freezing_depth__Z_H_max=0.85, climate_index__a_0=0.85),
            'луганськ':         City('Луганськ', soil_freezing_depth__Z_H_max=1.00, climate_index__a_0=0.95),
            'сімферополь':      City('Сімферополь', soil_freezing_depth__Z_H_max=0.40, climate_index__a_0=0.50)
        }

    def get_city(self, city_name: str) -> City:
        """Повертає об'єкт міста за його назвою."""
        city_key = city_name.lower()
        if city_key not in self._cities:
            raise KeyError(f"Місто {city_name} не знайдено в базі даних")
        return self._cities[city_key]

    def list_cities(self) -> list[str]:
        """Повертає список всіх доступних міст."""
        return [city.name for city in self._cities.values()]
