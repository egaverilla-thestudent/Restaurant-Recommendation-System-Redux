import streamlit as st
import pandas as pd

from src.preprocessing import (
    extract_features,
    build_feature_matrix
)

from src.recommender import (
    recommend_restaurants
)

restaurants = pd.read_csv("/Users/edgardomosesezekielaverilla/Restaurant-Recommendation-System-Redux/data/processed/restaurants_clean.csv")

taxonomy = pd.read_csv("/Users/edgardomosesezekielaverilla/Restaurant-Recommendation-System-Redux/data/reference/category_mapping.csv", encoding="cp1252")

taxonomy_keep = taxonomy[
    taxonomy["Keep"] == "Yes"
]

mapping = taxonomy_keep.set_index(
    "Category"
).to_dict("index")

restaurants = extract_features(
    restaurants,
    mapping
)

recommendation_feature_matrix = build_feature_matrix(
    restaurants,
    cuisine_weight=0.35,
    type_weight=0.25,
    experience_weight=0.20,
    numeric_weight=0.20
)

st.title("Restaurant Recommendation System")

restaurant_name = st.selectbox(
    "Select a Restaurant",
    sorted(restaurants["name"].unique())
)

available_cities = sorted(
    restaurants.loc[
        restaurants["name"] == restaurant_name,
        "city"
    ].unique()
)

city = st.selectbox(
    "Select City",
    available_cities
)

recommend = st.button("Recommend")

if recommend:

    recommendations = recommend_restaurants(
        restaurant_name=restaurant_name,
        city=city,
        restaurants=restaurants,
        recommendation_feature_matrix=recommendation_feature_matrix,
        top_n=10
    )

    st.dataframe(recommendations)


