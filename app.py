import streamlit as st
import pandas as pd
from streamlit_folium import st_folium

from src.preprocessing import (
    extract_features,
    build_feature_matrix
)

from src.recommender import (
    recommend_restaurants,
    find_restaurant
)

from src.taxonomy import (
    create_taxonomy_mapping
)

from src.visualization import (
    create_recommendation_map
)

restaurants = pd.read_csv("/Users/edgardomosesezekielaverilla/Restaurant-Recommendation-System-Redux/data/processed/restaurants_clean.csv")

taxonomy = pd.read_csv("/Users/edgardomosesezekielaverilla/Restaurant-Recommendation-System-Redux/data/reference/category_mapping.csv", encoding="cp1252")

mapping = create_taxonomy_mapping(
    taxonomy
)

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

if st.button("Recommend"):

    st.session_state["recommendations"] = recommend_restaurants(
        restaurant_name=restaurant_name,
        city=city,
        restaurants=restaurants,
        recommendation_feature_matrix=recommendation_feature_matrix,
        top_n=10
    )

    selected_index = find_restaurant(
        restaurant_name,
        city,
        restaurants
    )

    st.session_state["selected_restaurant"] = (
        restaurants.loc[selected_index]
    )

if "recommendations" in st.session_state:

    recommendations = st.session_state["recommendations"]

    selected_restaurant = st.session_state["selected_restaurant"]

    restaurant_map = create_recommendation_map(
        selected_restaurant=selected_restaurant,
        recommendations=recommendations,
        restaurants=restaurants
    )

    st_folium(
        restaurant_map,
        width=900,
        height=600
    )

    st.dataframe(recommendations)
