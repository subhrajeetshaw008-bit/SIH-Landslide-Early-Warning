from online_terrain import get_online_terrain


def get_terrain(latitude, longitude):
    try:
        elevation, slope = get_online_terrain(
            latitude,
            longitude
        )

        return {
            "elevation": elevation,
            "slope": slope
        }

    except Exception:
        return None