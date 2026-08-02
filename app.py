import streamlit as st
import pandas as pd
from src.recommender import (
    find_restaurant,
    get_feature_vector,
    calculate_similarity,
    recommend_restaurants
)

st.title("Restaurant Recommendation System")

restaurants = pd.read_csv("/Users/edgardomosesezekielaverilla/Restaurant-Recommendation-System-Redux/data/processed/restaurants_clean.csv")

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

st.write("You selected:", restaurant_name)

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


