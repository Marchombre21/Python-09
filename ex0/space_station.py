try:
    import sys
    from pydantic import BaseModel, Field, ValidationError
    from datetime import date
except (ImportError, ModuleNotFoundError):
    print("Pydantic librairy is missing.\nMake sure you are in a virtual"
          " environment, then download it by typing the command:")
    print("pip install pydantic")
    sys.exit(1)


class StationModel(BaseModel):
    station_id: str = Field(max_length=10, min_length=3)
    name: str = Field(max_length=50, min_length=1)
    crew_size: int = Field(le=20, ge=1)
    power_level: float = Field(le=100, ge=0)
    oxygen_level: float = Field(le=100, ge=0)
    last_maintenance: date
    is_operational: bool = True
    notes: str | None = Field("", max_length=200)


def main() -> None:
    print("\nSpace Station Data Validation")
    print("========================================")
    stations: list = [
        {
            "station_id": 15,
            "name": "coucou",
            "crew_size": 22,
            "power_level": 0.5,
            "oxygen_level": 101,
            "last_maintenance": "10/10/1992",
            "is_operational": "oui",
            "notes": "Un truc"
        },
        {
            "station_id": "station_01",
            "name": "Real Station",
            "crew_size": 18,
            "power_level": 98,
            "oxygen_level": 85,
            "last_maintenance": "1992-10-10",
            "is_operational": True,
            "notes": ""
        }
    ]
    space_stations: list = [
        {
            'station_id': 'LGW125',
            'name': 'Titan Mining Outpost',
            'crew_size': 6,
            'power_level': 76.4,
            'oxygen_level': 95.5,
            'last_maintenance': '2023-07-11T00:00:00',
            'is_operational': True,
            'notes': None
        },
        {
            'station_id': 'QCH189',
            'name': 'Deep Space Observatory',
            'crew_size': 3,
            'power_level': 70.8,
            'oxygen_level': 88.1,
            'last_maintenance': '2023-08-24T00:00:00',
            'is_operational': False,
            'notes': 'System diagnostics required'
        },
        {
            'station_id': 'ISS674',
            'name': 'Europa Research Station',
            'crew_size': 11,
            'power_level': 82.0,
            'oxygen_level': 91.4,
            'last_maintenance': '2023-10-21T00:00:00',
            'is_operational': True,
            'notes': None
        },
        {
            'station_id': 'ISS877',
            'name': 'Mars Orbital Platform',
            'crew_size': 9,
            'power_level': 79.7,
            'oxygen_level': 87.2,
            'last_maintenance': '2023-10-06T00:00:00',
            'is_operational': False,
            'notes': 'System diagnostics required'
        },
        {
            'station_id': 'LGW194',
            'name': 'Deep Space Observatory',
            'crew_size': 4,
            'power_level': 80.2,
            'oxygen_level': 89.9,
            'last_maintenance': '2023-10-25T00:00:00',
            'is_operational': False,
            'notes': 'System diagnostics required'
        },
        {
            'station_id': 'ISS847',
            'name': 'Solar Wind Monitor',
            'crew_size': 11,
            'power_level': 73.6,
            'oxygen_level': 98.1,
            'last_maintenance': '2023-12-11T00:00:00',
            'is_operational': False,
            'notes': 'System diagnostics required'
        },
        {
            'station_id': 'QCH400',
            'name': 'Asteroid Belt Relay',
            'crew_size': 12,
            'power_level': 75.5,
            'oxygen_level': 86.0,
            'last_maintenance': '2023-07-15T00:00:00',
            'is_operational': False,
            'notes': 'System diagnostics required'
        },
        {
            'station_id': 'ERS891',
            'name': 'Titan Mining Outpost',
            'crew_size': 4,
            'power_level': 94.4,
            'oxygen_level': 97.3,
            'last_maintenance': '2023-09-25T00:00:00',
            'is_operational': True,
            'notes': 'All systems nominal'
        },
        {
            'station_id': 'ABR266',
            'name': 'Asteroid Belt Relay',
            'crew_size': 8,
            'power_level': 76.0,
            'oxygen_level': 88.8,
            'last_maintenance': '2023-07-10T00:00:00',
            'is_operational': False,
            'notes': 'System diagnostics required'
        },
        {
            'station_id': 'LGW723',
            'name': 'Mars Orbital Platform',
            'crew_size': 11,
            'power_level': 90.8,
            'oxygen_level': 87.3,
            'last_maintenance': '2023-09-25T00:00:00',
            'is_operational': False,
            'notes': 'System diagnostics required'
        }
    ]

    for station in stations:
        try:
            model: StationModel = StationModel(**station)
            status: str = "Operational" if model.is_operational else\
                          "Non-operational"
            print()
            print("Valid station created:")
            print("ID:", model.station_id)
            print("Name:", model.name)
            print(f"Crew: {model.crew_size} people")
            print(f"Power: {model.power_level}%")
            print(f"Oxygen: {model.oxygen_level}%")
            print("Status:", status)
            print()
        except ValidationError as e:
            print("\nExpected validation error:")
            for error in e.errors():
                error_name = error["loc"][0]
                print(f"{error_name}: {error['msg']}")
            print()
            print("="*60)

    for station in space_stations:
        try:
            model = StationModel(**station)
            status = "Operational" if model.is_operational else\
                     "Non-operational"
            print()
            print("Valid station created:")
            print("ID:", model.station_id)
            print("Name:", model.name)
            print(f"Crew: {model.crew_size} people")
            print(f"Power: {model.power_level}%")
            print(f"Oxygen: {model.oxygen_level}%")
            print("Status:", status)
            print()
        except ValidationError as e:
            print("\nExpected validation error:")
            for error in e.errors():
                error_name = error["loc"][0]
                print(f"{error_name}: {error['msg']}")
            print()
            print("="*60)


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(e)
