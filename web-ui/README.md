# Web UI - Twitch Mobile Search (Pytest + Selenium)

## Overview
Automates the Twitch mobile web flow in Chrome emulation:
1. Open Twitch
2. Tap search icon
3. Search for "StarCraft II"
4. Scroll down twice
5. Open a streamer
6. Wait for the streamer page to load and take a screenshot

Handles optional modal/pop-up before the video loads.

## Repository Structure
```
web-ui/
├── pages/                 # Page Object Model classes
│   ├── base_page.py      # Base class with common methods
│   ├── twitch_home.py    # Twitch home page interactions
│   ├── twitch_search.py  # Search page interactions
│   ├── twitch_results.py # Results page interactions
│   └── twitch_streamer.py # Streamer page interactions
├── utils/                 # Utility functions
│   ├── screenshot.py     # Screenshot capture
│   ├── scroll.py         # Scroll functionality
│   └── waits.py          # Custom wait conditions
├── tests/                 # Test files
│   └── test_twitch_mobile.py
├── screenshots/           # Output directory for screenshots
├── conftest.py           # Pytest fixtures and configuration
├── pytest.ini            # Pytest configuration
└── requirements.txt      # Python dependencies
```

## Requirements
- Python 3.10+
- Google Chrome
- ChromeDriver compatible with your Chrome version (ensure it is in PATH)

## Setup
```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Run
```bash
pytest
```

## Configuration
- `HEADLESS=true` to run headless
- `MOBILE_DEVICE_NAME=Pixel 5` to change the emulated device (default: Pixel 5)

Example:
```bash
HEADLESS=true MOBILE_DEVICE_NAME="Pixel 5" pytest
```

## Output
Screenshots are saved to `screenshots/` with timestamped filenames.

## Framework Design
- **Page Object Model**: Each page has its own class with locators and methods, making tests maintainable and scalable
- **Robust Waits**: Custom wait conditions handle dynamic content and multiple selector strategies
- **Modal Handling**: Comprehensive modal/popup detection and closure with multiple selector strategies
- **Mobile Emulation**: Proper Chrome mobile emulation with configurable device profiles
- **Utility Functions**: Reusable utilities for common operations (scrolling, screenshots, waits)

## Notes
- Test uses Chrome mobile emulation via Selenium ChromeOptions
- If Twitch shows a login or cookie modal, it attempts to close it automatically
- Supports both headed and headless execution
- Screenshots are timestamped for easy identification

## GIF
![Web UI tests demo](../assets/web-ui.gif)
