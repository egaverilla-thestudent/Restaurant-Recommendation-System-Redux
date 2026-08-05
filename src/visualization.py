import folium

def create_recommendation_map(
    selected_restaurant,
    recommendations,
    restaurants
):

    restaurant_map = folium.Map(
        location=[
            selected_restaurant["latitude"],
            selected_restaurant["longitude"]
        ],
        zoom_start=15
    )

    folium.Marker(
        location=[
            selected_restaurant["latitude"],
            selected_restaurant["longitude"]
        ],
        popup=selected_restaurant["name"],
        tooltip="Selected Restaurant",
        icon=folium.Icon(
            color="red",
            icon="star"
        )
    ).add_to(restaurant_map)

    for _, recommendation in recommendations.iterrows():

        restaurant = restaurants.loc[
            recommendation.name
        ]

        folium.Marker(
            location=[
                restaurant["latitude"],
                restaurant["longitude"]
            ],
            popup=f"""
            <b>{restaurant['name']}</b><br>
            Hybrid Score: {recommendation['hybrid_score']:.3f}<br>
            Similarity: {recommendation['similarity']:.3f}<br>
            Distance: {recommendation['distance_km']:.2f} km
            """,
            icon=folium.Icon(color="blue")
        ).add_to(restaurant_map)

    return restaurant_map