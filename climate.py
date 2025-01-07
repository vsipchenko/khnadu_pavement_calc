from enum import Enum
from typing import Optional

from city import CityTable, City


class ClimateZone(Enum):
    """
    Дорожньо-кліматичні зони України.

    """
    ZONE_1 = "I"    # I зона
    ZONE_2 = "II"   # II зона
    ZONE_3 = "III"  # III зона
    ZONE_4 = "IV"   # IV зона (розділяється на західну та південну частини)


class TerrainType(Enum):
    """
    Типи місцевості за характером зволоження.

    """
    TYPE_1 = 1  # Сухі ділянки, добре дреновані
    TYPE_2 = 2  # Нормальні умови зволоження
    TYPE_3 = 3  # Підвищена вологість, погане водовідведення


class ClimateConfig:
    """
    Конфігурація кліматичних параметрів для розрахунку нежорсткого дорожнього одягу.

    Args:
        zone (ClimateZone): Дорожньо-кліматична зона
        terrain_type (TerrainType): Тип місцевості за характером зволоження
        city (str, optional): Назва міста українською, альтернатива для soil_freezing_depth__Z_H_max
        soil_freezing_depth__Z_H_max (float, optional): Глибина промерзання ґрунту в метрах (якщо відома)
        climate_index__a_0 (float, optional): Кліматичний показник α0 (якщо відомий)
        is_sandy_soil (bool, optional): True якщо ґрунт - супісок, дрібний або пилуватий пісок


    Example:
        >>> climate_config = ClimateConfig(
        ...     zone=ClimateZone.ZONE_2,
        ...     terrain_type=TerrainType.TYPE_1,
        ...     city='Київ',
        ...     is_sandy_soil=True
        ... )
        or
        >>> climate_config = ClimateConfig(
        ...     zone=ClimateZone.ZONE_2,
        ...     terrain_type=TerrainType.TYPE_1,
        ...     soil_freezing_depth__Z_H_max=0.95,
        ...     climate_index__a_0=0.65,
        ... )

    Source:
        ГБН В.2.3-37641918-559:2019 "Автомобільні дороги. Дорожній одяг нежорсткий.
        Проектування" розділ 7 "Розрахунок на морозостійкість", рисунок 7.2 -
        "Карта ізоліній глибини промерзання ґрунтів та ізоліній значень кліматичного
        коефіцієнта на території України"
    """

    def __init__(
            self,
            zone: ClimateZone,
            terrain_type: TerrainType,
            city: Optional[str] = None,
            soil_freezing_depth__Z_H_max: Optional[float] = None,
            climate_index__a_0: Optional[float] = None,
            is_sandy_soil: Optional[bool] = False,
        ):
        if not isinstance(zone, ClimateZone):
            raise ValueError('zone must be ClimateZone enum')
        if not isinstance(terrain_type, TerrainType):
            raise ValueError('terrain_type must be TerrainType enum')

        self.zone = zone
        self.terrain_type = terrain_type

        self.city_table = CityTable()
        self.city_data = self.city_table.get_city(city)
        self.soil_freezing_depth__Z_H_max = soil_freezing_depth__Z_H_max or self._get_soil_freezing_depth_by_city(self.city_data, is_sandy_soil)
        self.climate_index__a_0 = climate_index__a_0 or self._get_climate_index_by_city(self.city_data)
        self.is_sandy_soil = is_sandy_soil

    def _get_soil_freezing_depth_by_city(self, city: City, is_sandy_soil: bool) -> float:
        """
        Повертає нормативну глибину промерзання ґрунту для заданого міста.

        Returns:
            float: Глибина промерзання в метрах

        Note:
            Значення взяті з карти ізоліній глибини промерзання ґрунтів згідно з
            ГБН В.2.3-37641918-559:2019, рисунок 7.2.

            Для супісків, дрібних та пилуватих пісків значення
            збільшується на 20%.
        """
        base_depth = city.soil_freezing_depth__Z_H_max
        return base_depth * 1.2 if is_sandy_soil else base_depth

    def _get_climate_index_by_city(self, city: City) -> float:
        """
        Повертає кліматичний показник α0 для заданого міста.

        Returns:
            float: Кліматичний показник α0

        Note:
            Значення взяті з карти ізоліній згідно з ГБН В.2.3-37641918-559:2019, рис. 7.2.

            Альтернативно може бути розрахований за формулою:
            α0 = (Z - Z0)^2 / (2Тз)
            де:
            Z - середня багаторічна глибина промерзання ґрунту
            Z0 - товщина дорожнього одягу
            Тз - середня тривалість промерзання ґрунту
        """
        return city.climate_index__a_0

    @classmethod
    def calculate_climate_index(
            cls,
            frost_depth: float,
            road_thickness: float,
            freezing_duration: int
    ) -> float:
        """
        Розраховує кліматичний показник α0 за формулою.

        Args:
            frost_depth (float): Середня багаторічна глибина промерзання ґрунту (Z)
            road_thickness (float): Товщина дорожнього одягу (Z0)
            freezing_duration (int): Середня тривалість промерзання ґрунту (Тз)

        Returns:
            float: Розрахований кліматичний показник α0
        """
        return (frost_depth - road_thickness) ** 2 / (2 * freezing_duration)

    @property
    def calculation_days(self) -> int:
        """
        Повертає кількість розрахункових діб на рік для заданої кліматичної зони.

        Returns:
            int: Кількість розрахункових діб
        """
        days_map = {
            ClimateZone.ZONE_1: 145,
            ClimateZone.ZONE_2: 135,
            ClimateZone.ZONE_3: 130,
            ClimateZone.ZONE_4: {"west": 140, "south": 120}
        }
        return days_map[self.zone]

    @property
    def design_temperature(self) -> int:
        """
        Повертає розрахункову температуру для матеріалів на основі органічних в'яжучих.

        Returns:
            int: Розрахункова температура в градусах Цельсія
        """
        temp_map = {
            ClimateZone.ZONE_1: 20,
            ClimateZone.ZONE_2: 25,
            ClimateZone.ZONE_3: 30,
            ClimateZone.ZONE_4: {"west": 25, "south": 35}
        }
        return temp_map[self.zone]