import requests
import numpy as np


def get_online_terrain(latitude, longitude):

    # Get elevation at center and nearby points
    points = [
        (latitude, longitude),
        (latitude + 0.001, longitude),
        (latitude - 0.001, longitude),
        (latitude, longitude + 0.001),
        (latitude, longitude - 0.001),
    ]

    latitudes = ",".join(
        str(p[0]) for p in points
    )

    longitudes = ",".join(
        str(p[1]) for p in points
    )

    url = (
        "https://api.open-meteo.com/v1/elevation"
        f"?latitude={latitudes}"
        f"&longitude={longitudes}"
    )

    response = requests.get(
        url,
        timeout=10
    )

    response.raise_for_status()

    elevations = response.json()["elevation"]

    center = elevations[0]

    north = elevations[1]
    south = elevations[2]
    east = elevations[3]
    west = elevations[4]

    # Approximate distance between points
    lat_distance = 111320 * 0.001

    lon_distance = (
        111320
        * np.cos(np.radians(latitude))
        * 0.001
    )

    # Calculate gradients
    dz_dy = (
        (north - south)
        / (2 * lat_distance)
    )

    dz_dx = (
        (east - west)
        / (2 * lon_distance)
    )

    # Calculate slope in degrees
    slope = np.degrees(
        np.arctan(
            np.sqrt(
                dz_dx ** 2 +
                dz_dy ** 2
            )
        )
    )

    return float(center), float(slope)