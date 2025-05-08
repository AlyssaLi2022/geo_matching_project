# main_app.py

import geo_matcher 
import re # For parsing complex coordinate strings

def parse_single_geo_value(value_str: str):
    """
    Parse single coordinate string (lat or lon) to decimal degrees float.
    Supports DMS (e.g., 31°13'27"N), DD with symbol (e.g., 31.2242°), plain DD.
    Returns float or None on parsing failure.
    """
    value_str = str(value_str).strip() # Ensure string and strip

    # DMS: e.g., 31°13'27"N or 31d 13m 27s N or 31 13 27N
    # Uses common ' and " for quotes. Handles optional decimal seconds.
    dms_pattern = re.compile(
        r"^\s*(\d{1,3})\s*[°d:\s]\s*"      # Degrees
        r"(\d{1,2})\s*['m:\s]\s*"          # Minutes
        r"(?:(\d{1,2}(?:\.\d+)?)\s*[\"sS\s]*)?"  # Optional Seconds
        r"\s*([NSEWnsew])?\s*$", re.IGNORECASE # Optional Direction
    )
    match = dms_pattern.match(value_str)
    if match:
        try:
            deg = float(match.group(1))
            mnt = float(match.group(2))
            sec = float(match.group(3)) if match.group(3) else 0.0
            direction = match.group(4).upper() if match.group(4) else None

            if not (0 <= mnt < 60 and 0 <= sec < 60): return None # Invalid minute/second values
            
            dd = deg + (mnt / 60) + (sec / 3600)
            if direction in ['S', 'W']: dd = -dd
            return dd
        except (ValueError, TypeError):
            return None # Error during conversion

    # DD with degree symbol: e.g., "31.2242°"
    dd_deg_symbol_pattern = re.compile(r"^\s*([+-]?\d+(?:\.\d+)?)\s*°\s*$")
    match = dd_deg_symbol_pattern.match(value_str)
    if match:
        try: return float(match.group(1))
        except ValueError: return None

    # Plain DD (float): e.g., "+31.2242", "31.2242"
    try: return float(value_str)
    except ValueError: return None # Final attempt failed

def get_coordinates_interactive(array_name: str) -> list:
    """
    Interactively get list of (lat, lon) tuples from user.
    User inputs latitude and longitude strings separately for each point.
    """
    coordinates = []
    print(f"\n--- Enter coordinates for {array_name} ---")
    print("For each point, enter Latitude, then Longitude.")
    print("Supported formats for a single value (lat or lon):")
    print("  - DMS: e.g., 31°13'27\"N  or  121d 28m 15s E")
    print("  - DD with symbol: e.g., 31.2242°")
    print("  - DD (plain number): e.g., +31.2242 or -74.006")
    print("Type 'done' (for Latitude) to finish this array.")

    point_num = 1
    while True:
        print(f"\n-- Point {point_num} for {array_name} --")
        lat_input_str = input(f"Enter Latitude for Point {point_num} (or 'done'): ").strip()
        if lat_input_str.lower() == 'done':
            if not coordinates: print(f"Info: {array_name} is empty.")
            break
        
        lon_input_str = input(f"Enter Longitude for Point {point_num}: ").strip()

        lat_val = parse_single_geo_value(lat_input_str)
        lon_val = parse_single_geo_value(lon_input_str)

        valid_point = True
        if lat_val is None:
            print(f"  Error: Could not parse Latitude: '{lat_input_str}'. Try Point {point_num} again.")
            valid_point = False
        elif not (-90 <= lat_val <= 90):
            print(f"  Error: Parsed Latitude {lat_val:.4f}° is out of range [-90, 90]. Try Point {point_num} again.")
            valid_point = False
        
        if lon_val is None:
            print(f"  Error: Could not parse Longitude: '{lon_input_str}'. Try Point {point_num} again.")
            valid_point = False
        elif not (-180 <= lon_val <= 180):
            print(f"  Error: Parsed Longitude {lon_val:.4f}° is out of range [-180, 180]. Try Point {point_num} again.")
            valid_point = False
        
        if valid_point:
            coordinates.append((lat_val, lon_val))
            print(f"  Added Point {point_num}: ({lat_val:.4f}, {lon_val:.4f})")
            point_num += 1
        # If not valid_point, loop continues, user retries current point_num
            
    return coordinates

if __name__ == "__main__":
    print("=== Interactive Geo Location Matcher (Enhanced Input) ===")
    
    # Get coordinates for the first array
    points1 = get_coordinates_interactive("Primary Array (Array 1)")
    
    # Get coordinates for the second array
    points2 = get_coordinates_interactive("Secondary Array (Array 2)")

    if not points1 or not points2:
        print("\nOne or both coordinate arrays are effectively empty. Cannot perform matching.")
    else:
        print("\n--- Performing Matching ---")
        print(f"Primary Array (parsed): {points1}")
        print(f"Secondary Array (parsed): {points2}")
        
        # points1 and points2 are now lists of (float,float) tuples,
        # which geo_matcher.match_closest_points can handle directly
        # via its internal _parse_coordinate_input recognizing tuples.
        matches_result = geo_matcher.match_closest_points(points1, points2)
        
        if matches_result:
            print("\n--- Match Results ---")
            for idx1, idx2, dist in matches_result:
                p1_disp = points1[idx1] 
                p2_disp = points2[idx2]
                
                print(f"  Point from Primary Array (idx {idx1}): ({p1_disp[0]:.4f}, {p1_disp[1]:.4f})")
                print(f"  is closest to Point from Secondary Array (idx {idx2}): ({p2_disp[0]:.4f}, {p2_disp[1]:.4f})")
                print(f"  Distance: {dist:.2f} km")
        else:
            print("\nNo valid matches found by the geo_matcher module.")
            print("  This could be because no valid points remained after internal parsing/validation,")
            print("  or no geographical proximity between the valid points in the two arrays.")

    print("\n=== Program Finished ===")