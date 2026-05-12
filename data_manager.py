"""
Data Manager Module
Handles reading and writing assignments and exams from/to JSON files.
All data is stored locally in the /data folder.
"""

import json
import os

DATA_DIR = "data"
ASSIGNMENTS_FILE = os.path.join(DATA_DIR, "assignments.json")
EXAMS_FILE = os.path.join(DATA_DIR, "exams.json")
SETTINGS_FILE = os.path.join(DATA_DIR, "settings.json")

os.makedirs(DATA_DIR, exist_ok=True)


def _read_json(filepath):
    """Read JSON file. Returns empty list if file doesn't exist."""
    if not os.path.exists(filepath):
        return []
    with open(filepath, "r") as f:
        return json.load(f)


def _write_json(filepath, data):
    """Write data to JSON file."""
    with open(filepath, "w") as f:
        json.dump(data, f, indent=4)


def load_assignments():
    return _read_json(ASSIGNMENTS_FILE)


def save_assignments(assignments):
    _write_json(ASSIGNMENTS_FILE, assignments)


def load_exams():
    return _read_json(EXAMS_FILE)


def save_exams(exams):
    _write_json(EXAMS_FILE, exams)


def load_settings():
    """Load user settings. Returns default settings if file doesn't exist."""
    settings = _read_json(SETTINGS_FILE)
    if not settings:
        settings = {
            "profile_picture": None,
            "notifications_enabled": True,
            "email_notifications": False,
            "theme": "light"
        }
        save_settings(settings)
    return settings


def save_settings(settings):
    _write_json(SETTINGS_FILE, settings)