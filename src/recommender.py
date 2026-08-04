import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
from src.spatial import prepare_spatial_features

SIMILARITY_WEIGHT = 0.70
PROXIMITY_WEIGHT = 0.30
DECAY_FACTOR = 10
SEARCH_RADIUS_KM = 20

def find_restaurant(
    restaurant_name,
    city,
    restaurants
):

    selected_index = restaurants[
        (restaurants["name"] == restaurant_name) &
        (restaurants["city"] == city)
    ].index[0]

    return selected_index

def get_feature_vector(
    selected_index,
    recommendation_feature_matrix
):

    selected_vector = recommendation_feature_matrix.loc[
        [selected_index]
    ]

    return selected_vector


def calculate_similarity(
    selected_vector,
    recommendation_feature_matrix
):

    similarity_scores = cosine_similarity(
        selected_vector,
        recommendation_feature_matrix
    )

    similarity_df = pd.DataFrame(
        similarity_scores.T,
        columns=["similarity"]
    )

    return similarity_df

def get_top_recommendations(
    similarity_df,
    restaurants,
    selected_index,
    top_n=10,
    exclude_same_chain=False
):

    filtered_df = similarity_df.drop(selected_index)

    filtered_df = filtered_df[
    restaurants.loc[
        filtered_df.index,
        "distance_km"
    ] <= SEARCH_RADIUS_KM
    ]

    filtered_df["proximity_score"] = restaurants.loc[
        filtered_df.index,
        "proximity_score"
    ]

    if exclude_same_chain:
        selected_name = restaurants.loc[selected_index, "name"]

        filtered_df = filtered_df[
            restaurants.loc[filtered_df.index, "name"] != selected_name
        ]

    filtered_df["hybrid_score"] = (
        SIMILARITY_WEIGHT * filtered_df["similarity"]
        + PROXIMITY_WEIGHT * filtered_df["proximity_score"]
    )

    top_similarity_df = filtered_df.nlargest(
        top_n,
        "hybrid_score"
    )

    return top_similarity_df

def format_recommendations(
    top_similarity_df,
    restaurants
):

    recommendation_table = restaurants.loc[
        top_similarity_df.index
    ]

    recommendation_table = recommendation_table[
        [
            "name",
            "city",
            "state",
            "stars",
            "review_count",
            "distance_km"
        ]
    ]

    recommendation_table = pd.concat(
        [recommendation_table, top_similarity_df],
        axis=1
    )

    return recommendation_table

def recommend_restaurants(
    restaurant_name,
    city,
    restaurants,
    recommendation_feature_matrix,
    top_n=10
):

    selected_index = find_restaurant(
        restaurant_name,
        city,
        restaurants
    )

    selected_restaurant = restaurants.loc[selected_index]

    restaurants = prepare_spatial_features(
    restaurants=restaurants,
    selected_restaurant=selected_restaurant

    )
    

    selected_vector = get_feature_vector(
        selected_index,
        recommendation_feature_matrix
    )

    similarity_df = calculate_similarity(
        selected_vector,
        recommendation_feature_matrix
    )

    top_similarity_df = get_top_recommendations(
    similarity_df=similarity_df,
    restaurants=restaurants,
    selected_index=selected_index,
    top_n=top_n,
    exclude_same_chain=True
    )   

    recommendation_table = format_recommendations(
        top_similarity_df,
        restaurants
    )

    return recommendation_table