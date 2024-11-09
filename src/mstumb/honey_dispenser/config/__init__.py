import json
from dataclasses import dataclass, field
from typing import Dict, Any
import os
from enum import Enum


# Enum to represent setting keys
class Setting(Enum):
    WEIGHT_SET = 'weight_set'
    WEIGHT_BEFORE = 'weight_before'
    JARS_FILLED = 'jars_filled'
    ROUNDING = 'rounding'
    MAX_STEPS = 'max_steps'
    # Add more settings as needed


# Enum for stepper parameters
class StepperSetting(Enum):
    STEP1 = 'step1'
    STEP2 = 'step2'
    STEP3 = 'step3'
    STEP4 = 'step4'


# Enum for scale parameters
class ScaleSetting(Enum):
    DT = 'DT'
    SCK = 'SCK'
    REF_UNIT = 'refUnit'
    ZERO_VALUE = 'zeroValue'


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
    weight_set: int = 900
    weight_before: int = 50
    jars_filled: int = 0
    rounding: int = 5
    max_steps: int = 20


@dataclass
class Config:
    stepper: Stepper = field(default_factory=Stepper)
    scale: Scale = field(default_factory=Scale)
    settings: Settings = field(default_factory=Settings)

    # excluded from serialization
    _filepath: str = None
    _instance: 'Config' = None  # Singleton instance

    @classmethod
    def instance(cls):
        """Returns the singleton instance."""
        if cls._instance is None:
            raise ValueError("Config instance is not initialized. Call load_from_file() first.")
        return cls._instance

    @classmethod
    def load_from_file(cls, filepath: str) -> 'Config':
        """Loads the config from a file, initializes the singleton."""
        if not os.path.exists(filepath):
            # Create file with default values if it doesn't exist
            config = cls()
            config._filepath = filepath  # Set the file path before saving
            config.save_to_file()  # Save the default configuration to file
            cls._instance = config
            return config
        else:
            with open(filepath, 'r') as file:
                data = json.load(file)
            config = cls.from_json(data)
            config._filepath = filepath  # Set the filepath after loading
            cls._instance = config  # Set the singleton instance
            return config

    @classmethod
    def from_json(cls, json_data: Dict[str, Any]) -> 'Config':
        """Creates a Config instance from JSON data."""
        return Config(
            stepper=Stepper(**json_data.get("stepper", {})),
            scale=Scale(**json_data.get("scale", {})),
            settings=Settings(**json_data.get("settings", {}))
        )

    def to_json(self) -> str:
        """Convert the Config object to a JSON string, excluding _filepath."""
        return json.dumps(self, default=lambda o: {k: v for k, v in o.__dict__.items() if not k.startswith('_')}, indent=2)

    def save_to_file(self):
        """Saves the current config to the file."""
        if not self._filepath:
            raise ValueError("File path is not set. Cannot save the configuration.")
        with open(self._filepath, 'w') as file:
            json.dump(self, file, default=lambda o: {k: v for k, v in o.__dict__.items() if not k.startswith('_')}, indent=2)

    def update(self, setting: [Setting, ScaleSetting, StepperSetting], value: [str, int]):
        """Updates a setting using the Setting enum."""
        if isinstance(setting, Setting):
            self.settings.__dict__[setting.value] = value
            self.save_to_file()
        elif isinstance(setting, ScaleSetting):
            self.scale.__dict__[setting.value] = value
            self.save_to_file()
        elif isinstance(setting, StepperSetting):
            self.stepper.__dict__[setting.value] = value
            self.save_to_file()
        else:
            raise ValueError(f"Setting {setting.value} not found.")

    def get(self, setting: [Setting, ScaleSetting, StepperSetting]):
        """Gets the value of a setting using the Setting enum."""
        if isinstance(setting, Setting):
            return self.settings.__dict__.get(setting.value, None)
        elif isinstance(setting, ScaleSetting):
            return self.scale.__dict__.get(setting.value, None)
        elif isinstance(setting, StepperSetting):
            return self.stepper.__dict__.get(setting.value, None)


if __name__ == '__main__':
    # Main app (initializing config)
    Config.load_from_file('config.json')

    # Update the setting
    Config.instance().update(Setting.WEIGHT_BEFORE, 600)
    print("Updated weight_before to 200.")
    # Update the setting
    Config.instance().update(Setting.ROUNDING, 2)
