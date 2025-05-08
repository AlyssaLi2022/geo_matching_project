# Geo Location Matcher

A Python module by Wenwen Li to match each point in a primary array of geographic locations to the closest one in a secondary array. It also includes an interactive command-line application to demonstrate its usage with various coordinate input formats.

## Features

- Calculates the geodesic distance between two GPS coordinates.
- Matches points from one list to the closest points in another list.
- Interactive CLI (`main_app.py`) for user input of coordinates.
- The interactive CLI supports several input formats for individual latitude/longitude values:
    - Degrees, Minutes, Seconds (DMS) with direction (e.g., `31°13'27"N`, `121d 28m 15s E`)
    - Decimal Degrees (DD) with degree symbol (e.g., `31.2242°`)
    - Plain Decimal Degrees (e.g., `+31.2242`, `-74.0060`)
- The core `geo_matcher` module also accepts pre-parsed `(latitude, longitude)` tuples or `"latitude,longitude"` strings.
- Basic error handling for invalid input formats and out-of-range coordinates.

## Prerequisites

- Python 3.7+
- Git

## Setup and Installation

1.  **Clone the repository:**
    *(Replace `YOUR_GITHUB_USERNAME` and `YOUR_REPOSITORY_NAME` with your actual GitHub username and the repository name you chose on GitHub, e.g., `wenwenli-bu/geo-location-matcher` if your GitHub username is `wenwenli-bu` and repo name is `geo-location-matcher`)*
    ```bash
    git clone https://github.com/YOUR_GITHUB_USERNAME/YOUR_REPOSITORY_NAME.git
    cd YOUR_REPOSITORY_NAME
    ```

2.  **Create and activate a Python virtual environment:**
    ```bash
    # For Windows (cmd.exe or compatible terminals like VS Code default)
    python -m venv .venv
    .venv\Scripts\activate.bat
    ```
    *(Note: You confirmed `.venv\Scripts\activate.bat` works best for your setup. For other shells, activation commands differ.)*

3.  **Install dependencies:**
    The only external dependency is `geopy`.
    ```bash
    pip install geopy
    ```

## Usage

To run the interactive command-line application:

1.  Ensure your virtual environment is activated.
2.  Navigate to the project directory.
3.  Run the `main_app.py` script:
    ```bash
    python main_app.py
    ```
4.  Follow the on-screen prompts to enter coordinates for the primary and secondary arrays.

To use the `geo_matcher` module in your own Python scripts:

```python
import geo_matcher

# Example points (can be tuples or "lat,lon" strings)
array1 = [(40.7128, -74.0060), "34.0522, -118.2437"]
array2 = ["40.7127, -74.0059", (34.0521, -118.2436), "0.0,0.0"]

matches = geo_matcher.match_closest_points(array1, array2)

if matches:
    for idx1, idx2, distance in matches:
        print(f"Point {idx1} from array1 matches point {idx2} from array2. Distance: {distance:.2f} km")
else:
    print("No matches found or an error occurred.")
    Tech Stack
Python
geopy library (for geodesic distance calculation)