## Notes

During testing, two different restaurants achieved a cosine similarity of 1.0.

Investigation showed that this was expected because the current recommendation engine only uses:

- Cuisine
- Restaurant Type
- Experience
- Star Rating
- Review Count

The two restaurants had identical values for all engineered features, resulting in identical feature vectors.

This validates the correctness of the cosine similarity implementation while highlighting an opportunity for future feature engineering.

---------------------------------------------------------------------------------------------------------------------------------------------
## Lab Notes 001

07/21/2026

After initial testing, we found out that we need to further tune the features of the project. In one instance we used the index for sonic burgers and the top 1 recommendation is a DQ store. Which is weird if you are looking for a burger joint and not a desserts place. 

The goal for tonight is to check how to further improve the features of projects. There are a couple of techniques to use. I'll list them below:

- Feature Scaling:
    - Min-Max Scaling
    - Standardization (Z-score)
    - Robust Scaling

- Weighted Features
    - Manual feature weighting
    - Domain Knowledge

- Similarity Metrics
    - Euclidean Distance
    - Manhattan Distance
    - Jaccard Similarity
    - Pearson Correlation


## What I learned

Min-Max Scaling:

Brings features to a common scale; the goal is to rescale the numerical features to any arbitrary range, commonly [0,1].

Standardization (Z-Score):

Similar to min-max scaling this is a preprocessing technique to scale features within a range so that not one feature can dominate the other feature.

Robust Scaling:

Uses the median and interquartile range. The strength of this is its less senstivity on outliers and skewed data

Manual feature weighting

This is a rare technique into manually assigning importance of the feature since there are algoritms that can automatically do this

Domain Knowledge

This tie up with manual feature weighting, domain knowledge is exactly what it is, if you are an expert in the field then you have the expertise on determining important features from not


## Questions I still have

The main question to answer is what preprocessing techniques to use to further improve the output of the system. Well based from exploring the data, we can just implement, min-max scaling or a simple standardization. What i think is that the number of reviews affected the output since it is not scaled.

## Decisions I made

I'll implement the scalers, and weighted features.

## Ideas for V2

Initially I really want to implement geo restrictions since we have the lat/long, i'll implement it now on V2

--end

Our Mother of Victory, Pray for Us.