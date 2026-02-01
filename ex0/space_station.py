try:
    from pydantic import BaseModel, Field, ValidationError
    from datetime import date, timedelta, datetime
    from typing import Any
    from dataclasses import dataclass
    import random
except ImportError:
    print("Pydantic librairy is missing.\nBe sure being in a virtual"
          " environment, then download it typing the command:")
    print("pip install pydantic")



@dataclass
class DataConfig:
    """Configuration parameters for data generation"""
    seed: int = 42
    base_date: datetime = datetime(2024, 1, 1)
    date_range_days: int = 365


class station_model(BaseModel):
    station_id: str = Field(max_length=10, min_length=3)
    name: str = Field(max_length=50, min_length=1)
    crew_size: int = Field(le=20, ge=1)
    power_level: float = Field(le=100, ge=0)
    oxygen_level: float = Field(le=100, ge=0)
    last_maintenance: date
    is_operational: bool
    notes: str | None = Field("", max_length=200)


class SpaceStationGenerator:
    """Generates space station monitoring data"""
    STATION_NAMES = [
        "International Space Station", "Lunar Gateway", "Mars Orbital Platform",
        "Europa Research Station", "Titan Mining Outpost", "Asteroid Belt Relay",
        "Deep Space Observatory", "Solar Wind Monitor", "Quantum Communications Hub"
    ]
    STATION_PREFIXES = ["ISS", "LGW", "MOP", "ERS", "TMO", "ABR", "DSO", "SWM", "QCH"]

    def __init__(self, config: DataConfig):
        self.config = config
        random.seed(config.seed)

    def generate_station_data(self, count: int = 5) -> list[dict[str, Any]]:
        """Generate multiple space station records"""
        stations = []
        for i in range(count):
            station_id = f"{random.choice(self.STATION_PREFIXES)}{random.randint(100, 999)}"
            name = random.choice(self.STATION_NAMES) 
            # Realistic operational parameters
            crew_size = random.randint(3, 12)
            power_level = round(random.uniform(70.0, 98.5), 1)
            oxygen_level = round(random.uniform(85.0, 99.2), 1)
            # Recent maintenance date
            days_ago = random.randint(1, 180)
            maintenance_date = self.config.base_date - timedelta(days=days_ago)
            # Operational status based on system health
            is_operational = power_level > 75.0 and oxygen_level > 90.0
            # Optional maintenance notes
            notes = None
            if not is_operational:
                notes = "System diagnostics required"
            elif random.random() < 0.3:
                notes = "All systems nominal"
            stations.append({
                "station_id": station_id,
                "name": name,
                "crew_size": crew_size,
                "power_level": power_level,
                "oxygen_level": oxygen_level,
                "last_maintenance": maintenance_date.isoformat(),
                "is_operational": is_operational,
                "notes": notes
            })
        return stations


def main():
    print("\nSpace Station Data Validation")
    print("========================================")
    config = DataConfig()
    generator = SpaceStationGenerator(config)
    stations = generator.generate_station_data(5)
    for station in stations:
        try:
            station_test = station_model(**station)
            print("\nValid station created")
            print(f"ID: {station_test.station_id}")
            print(f"Name: {station_test.name}")
            print(f"Crew: {station_test.crew_size}")
            print(f"Power: {station_test.power_level}%")
            print(f"Oxygen: {station_test.oxygen_level}%")
            print(
                f"Status: {'Operational' if station_test.is_operational else
                           'Non-operational'}"
                )
            error_station = station_model(
                station_id=15,
                name="coucou",
                crew_size=22,
                power_level=0.5,
                oxygen_level=101,
                last_maintenance="10/10/1992",
                is_operational=True,
                notes="ok"
            )
        except ValidationError as e:
            print("\nExpected validation error:")
            for error in e.errors():
                error_name = error["loc"][0]
                print(f"{error_name}: {error["msg"]}")


if __name__ == "__main__":
    main()
