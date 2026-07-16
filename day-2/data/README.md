# Day 2 dataset

## California Housing data

[`california_housing_combined.csv`](california_housing_combined.csv) is a workshop copy derived from the California Housing dataset. It contains 20,000 rows and nine numeric columns describing California census block groups:

- longitude and latitude;
- median housing age;
- total rooms and bedrooms;
- population and households;
- median income; and
- median house value.

The dataset lineage traces to 1990 United States Census data used by R. Kelley Pace and Ronald Barry in their 1997 paper, “Sparse Spatial Autoregressions.” The commonly distributed full dataset contains 20,640 observations. This repository copy contains 20,000 observations, so it should be treated as a workshop subset or transformed copy rather than an exact reproduction of the full dataset.

## Sources and citation

- R. Kelley Pace and Ronald Barry, “Sparse Spatial Autoregressions,” *Statistics & Probability Letters*, volume 33, issue 3, 1997, pages 291–297. DOI: [10.1016/S0167-7152(96)00140-X](https://doi.org/10.1016/S0167-7152(96)00140-X).
- [scikit-learn California Housing dataset documentation](https://scikit-learn.org/stable/modules/generated/sklearn.datasets.fetch_california_housing.html)
- [Original paper and dataset background maintained by R. Kelley Pace](https://www.spatial-statistics.com/pace_manuscripts/spletters_ms_dir/statistics_prob_lets/html/ms_sp_lets1.html)

When using this workshop copy, cite both the original Pace and Barry paper and this workshop repository.

## Rights and responsible use

The underlying statistical records originate from the 1990 United States Census. Repository licensing does not replace or expand the rights attached to the underlying source data or any intermediate distribution. Users should verify the terms of the source from which they obtain or redistribute another copy.

The rows describe geographic aggregates rather than named individuals, but exact coordinates and combinations of attributes can still reveal small-area information. Treat the schema according to the sensitivity represented in the exercise, avoid making individual-level claims, and do not infer causation from area-level associations.

