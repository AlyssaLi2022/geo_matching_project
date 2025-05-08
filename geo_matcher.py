# geo_matcher.py

# Lib import
from geopy.distance import geodesic
# import re # Not strictly needed in this version of geo_matcher.py

# Internal helper to parse various coordinate inputs
def _parse_coordinate_input(coord_input):
    """
    Try to parse coord_input to (lat, lon) tuple.
    Supports:
        - (float, float) tuple
        - "lat,lon" string
    Returns (lat, lon) or None if parsing fails.
    """
    if isinstance(coord_input, tuple) and len(coord_input) == 2:
        if isinstance(coord_input[0], (int, float)) and isinstance(coord_input[1], (int, float)):
            return float(coord_input[0]), float(coord_input[1]) # Ensure float
        return None # Tuple elements not numbers

    if isinstance(coord_input, str):
        try:
            parts = [part.strip() for part in coord_input.split(',')]
            if len(parts) == 2:
                lat = float(parts[0])
                lon = float(parts[1])
                return lat, lon
        except ValueError:
            return None # String parts not convertible to float
        return None # String not in "lat,lon" format
    return None # Unrecognized format

# Calculate distance (expects validated DD tuples)
def calculate_distance(coord1, coord2):
    """
    Calc distance (km) between two validated GPS coords (decimal degrees).
    Returns float('inf') on error or invalid range.
    """
    if not (isinstance(coord1, tuple) and len(coord1) == 2 and
            isinstance(coord1[0], (int, float)) and isinstance(coord1[1], (int, float))):
        # This pre-check should ideally not be needed if inputs are always parsed correctly
        # print(f"Error: coord1 is not a valid numeric tuple: {coord1}") # Dev debug
        return float('inf')
    if not (isinstance(coord2, tuple) and len(coord2) == 2 and
            isinstance(coord2[0], (int, float)) and isinstance(coord2[1], (int, float))):
        # print(f"Error: coord2 is not a valid numeric tuple: {coord2}") # Dev debug
        return float('inf')

    if not (-90 <= coord1[0] <= 90 and -180 <= coord1[1] <= 180):
        return float('inf')
    if not (-90 <= coord2[0] <= 90 and -180 <= coord2[1] <= 180):
        return float('inf')

    try:
        return geodesic(coord1, coord2).km
    except Exception: 
        return float('inf')

# Match closest points with input parsing
def match_closest_points(points_array1_input, points_array2_input):
    """
    Match each point in points_array1 to closest in points_array2.
    Inputs can be lists of (lat,lon) tuples or "lat,lon" strings.
    Returns list of (original_idx1, original_idx2, distance_km) or [] on error.
    """
    if not isinstance(points_array1_input, list) or not isinstance(points_array2_input, list):
        return []

    parsed_points1, original_indices1 = [], []
    for i, p_in in enumerate(points_array1_input):
        parsed_coord = _parse_coordinate_input(p_in)
        if parsed_coord and (-90 <= parsed_coord[0] <= 90 and -180 <= parsed_coord[1] <= 180):
            parsed_points1.append(parsed_coord)
            original_indices1.append(i)

    parsed_points2, original_indices2 = [], []
    for i, p_in in enumerate(points_array2_input):
        parsed_coord = _parse_coordinate_input(p_in)
        if parsed_coord and (-90 <= parsed_coord[0] <= 90 and -180 <= parsed_coord[1] <= 180):
            parsed_points2.append(parsed_coord)
            original_indices2.append(i)

    if not parsed_points1 or not parsed_points2:
        return []

    matches = []
    for i_parsed, p1 in enumerate(parsed_points1):
        min_dist = float('inf')
        best_p2_parsed_idx = -1
        for j_parsed, p2 in enumerate(parsed_points2):
            dist = calculate_distance(p1, p2)
            if dist < min_dist:
                min_dist = dist
                best_p2_parsed_idx = j_parsed
        
        if best_p2_parsed_idx != -1:
            original_p1_idx = original_indices1[i_parsed]
            original_p2_idx = original_indices2[best_p2_parsed_idx]
            matches.append((original_p1_idx, original_p2_idx, min_dist))
    return matches