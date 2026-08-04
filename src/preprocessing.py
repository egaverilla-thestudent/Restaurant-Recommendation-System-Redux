import pandas as pd

from sklearn.preprocessing import (
    MultiLabelBinarizer,
    StandardScaler
)

# ============================================
# Feature Extraction
# ============================================

def extract_category_features(category_string, mapping):

    features = {
        "Cuisine": set(),
        "Restaurant Type": set(),
        "Experience": set()
    }

    categories = [
        category.strip()
        for category in category_string.split(",")
    ]

    for category in categories:

        if category in mapping:

            info = mapping[category]

            feature_type = info["Feature Type"]

            value = info["Standardized Value"]

            if feature_type in features and pd.notna(value):
                features[feature_type].add(value)

    return {
        key: list(value)
        for key, value in features.items()
    }


# ============================================
# Category Feature Extraction
# ============================================

def extract_features(restaurants, mapping):

    restaurants = restaurants.copy()

    restaurants["Extracted Features"] = (
        restaurants["categories"].apply(
            lambda x: extract_category_features(x, mapping)
        )
    )

    restaurants["Cuisine"] = (
        restaurants["Extracted Features"].apply(
            lambda x: x["Cuisine"]
        )
    )

    restaurants["Restaurant Type"] = (
        restaurants["Extracted Features"].apply(
            lambda x: x["Restaurant Type"]
        )
    )

    restaurants["Experience"] = (
        restaurants["Extracted Features"].apply(
            lambda x: x["Experience"]
        )
    )

    return restaurants

# ============================================
# Encoding
# ============================================

def create_multilabel_matrix(
    restaurants,
    column_name
):

    encoder = MultiLabelBinarizer()

    encoded = encoder.fit_transform(
        restaurants[column_name]
    )

    encoded_df = pd.DataFrame(
        encoded,
        columns=encoder.classes_,
        index=restaurants.index
    )

    return encoded_df

# ============================================
# Scaling
# ============================================

def scale_numeric_features(restaurants):

    numeric_features = restaurants[
        [
            "latitude",
            "longitude",
            "stars",
            "review_count"
        ]
    ]

    scaler = StandardScaler()

    scaled = scaler.fit_transform(
        numeric_features
    )

    scaled_numeric_df = pd.DataFrame(
        scaled,
        columns=numeric_features.columns,
        index=restaurants.index
    )

    return scaled_numeric_df


# ============================================
# Feature Matrix
# ============================================

def build_feature_matrix(
    restaurants,
    cuisine_weight,
    type_weight,
    experience_weight,
    numeric_weight
):

    cuisine_df = create_multilabel_matrix(
        restaurants,
        "Cuisine"
    )

    restaurant_type_df = create_multilabel_matrix(
        restaurants,
        "Restaurant Type"
    )

    experience_df = create_multilabel_matrix(
        restaurants,
        "Experience"
    )

    scaled_numeric_df = scale_numeric_features(
        restaurants
    )

    weighted_cuisine = cuisine_df * cuisine_weight

    weighted_type = restaurant_type_df * type_weight

    weighted_experience = experience_df * experience_weight

    weighted_numeric = scaled_numeric_df * numeric_weight

    recommendation_feature_matrix = pd.concat(
        [
            weighted_cuisine,
            weighted_type,
            weighted_experience,
            weighted_numeric
        ],
        axis=1
    )

    return recommendation_feature_matrix