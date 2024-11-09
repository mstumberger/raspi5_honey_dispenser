import json
from dataclasses import dataclass, field
from typing import Dict, Any
import os


@dataclass
class Stepper:
    step1: int = 5
    step2: int = 6
    step3: int = 13
    step4: int = 12


@dataclass
class Scale:
    DT: int = 20
    SCK: int = 21
    refUnit: int = 731
    zeroValue: int = 82302


@dataclass
class Settings:
    weight_before: int = 50
    jars_filled: int = 0


@dataclass
class Config:
    stepper: Stepper = field(default_factory=Stepper)
    scale: Scale = field(default_factory=Scale)
    settings: Settings = field(default_factory=Settings)

    @staticmethod
    def from_json(json_data: Dict[str, Any]) -> 'Config':
        return Config(
            stepper=Stepper(**json_data.get("stepper", {})),
            scale=Scale(**json_data.get("scale", {})),
            settings=Settings(**json_data.get("settings", {}))
        )

    def to_json(self) -> str:
        return json.dumps(self, default=lambda o: o.__dict__, indent=2)

    @classmethod
    def load_from_file(cls, filepath: str) -> 'Config':
        if not os.path.exists(filepath):
            # Create file with default values if it doesn't exist
            config = cls()
            config.save_to_file(filepath)
            return config
        else:
            with open(filepath, 'r') as file:
                data = json.load(file)
            return cls.from_json(data)

    def save_to_file(self, filepath: str):
        with open(filepath, 'w') as file:
            json.dump(self, file, default=lambda o: o.__dict__, indent=2)


if __name__ == '__main__':
    # Example usage
    config = Config.load_from_file('config.json')
    print(config)

    # Modify a value
    config.settings.weight_before = 60

    # Save the changes back to file
    config.save_to_file('config.json')
