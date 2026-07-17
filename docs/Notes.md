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