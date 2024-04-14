"""
File: config.py
Author: Elena Ryumina and Dmitry Ryumin
Description: Configuration file.
License: MIT License
"""

import toml
from typing import Dict
from types import SimpleNamespace


def flatten_dict(prefix: str, d: Dict) -> Dict:
    result = {}

    for k, v in d.items():
        if isinstance(v, dict):
            result.update(flatten_dict(f"{prefix}{k}_", v))
        else:
            result[f"{prefix}{k}"] = v

    return result


config = toml.load("config.toml")

config_data = flatten_dict("", config)

config_data = SimpleNamespace(**config_data)

DICT_EMO = {
    0: "Neutral",
    1: "Happiness",
    2: "Sadness",
    3: "Surprise",
    4: "Fear",
    5: "Disgust",
    6: "Anger",
}

COLORS = {
    0: 'blue', 
    1: 'orange', 
    2: 'green', 
    3: 'red', 
    4: 'purple', 
    5: 'brown', 
    6: 'pink'
}
