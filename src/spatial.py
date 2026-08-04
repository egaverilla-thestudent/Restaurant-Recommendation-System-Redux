import numpy as np

from sklearn.metrics.pairwise import (
    haversine_distances
)

EARTH_RADIUS_KM = 6371

DEFAULT_RADIUS_KM = 20

DEFAULT_DECAY_FACTOR = 10


# ============================================
# Spatial Filtering
# ============================================

def filter_by_radius(
    restaurants,
    selected_restaurant,
    radius_km=DEFAULT_RADIUS_KM
):
    """
    Return restaurants within a given radius of the
    selected restaurant.
    """

    selected_coords = np.radians([
        [
            selected_restaurant["latitude"],
            selected_restaurant["longitude"]
        ]
    ])

    restaurant_coords = np.radians(
        restaurants[
            ["latitude", "longitude"]
        ]
    )

    distances = haversine_distances(
        selected_coords,
        restaurant_coords
    )[0]

    distances_km = distances * EARTH_RADIUS_KM

    restaurants_with_distance = restaurants.copy()

    restaurants_with_distance["distance_km"] = distances_km

    return restaurants_with_distance


# ============================================
# Distance Scoring
# ============================================

def calculate_proximity_score(
    distance_km,
    decay_factor=DEFAULT_DECAY_FACTOR
):
    distance_km = np.maximum(distance_km, 0)
    return np.exp(-distance_km / decay_factor)


# ============================================
# Spatial Preparation
# ============================================

def prepare_spatial_features(
    restaurants,
    selected_restaurant,
    radius_km=DEFAULT_RADIUS_KM,
    decay_factor=DEFAULT_DECAY_FACTOR
):

    restaurants = filter_by_radius(
        restaurants=restaurants,
        selected_restaurant=selected_restaurant,
        radius_km=radius_km
    )

    restaurants["proximity_score"] = calculate_proximity_score(
        restaurants["distance_km"],
        decay_factor=decay_factor
    )

    return restaurants