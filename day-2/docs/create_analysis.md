# California Housing Analysis Notebook Specification

Act as a senior data analyst, statistician, and machine-learning engineer.

Create a complete, reproducible Jupyter Notebook that analyzes a local California housing dataset using privacy-conscious local analysis practices.

The notebook must generate analytical code and aggregate results without printing, displaying, transmitting, or exporting raw records or exact longitude–latitude pairs.

This is an area-level observational dataset. Do not claim that the procedures guarantee anonymity, regulatory compliance, or protection from every re-identification risk.

---

## 1. Required Deliverable

Create and return a valid Jupyter Notebook named:

`mdsp_california_housing_analysis.ipynb`

The deliverable must:

- Follow the `nbformat` specification.
- Contain separate Markdown and code cells.
- Be runnable from beginning to end.
- Contain no unfinished placeholders.
- Include sufficient documentation for another analyst to understand and reproduce the analysis.

Do not return only:

- A Python script.
- Notebook-style code fragments.
- An outline.
- Pseudocode.
- Instructions for manually assembling the notebook.
- TODO comments or omitted implementations.

If the environment cannot create an `.ipynb` file directly, return valid notebook JSON that can be saved without modification as an `.ipynb` file.

Prioritize a complete, executable core notebook over excessive methodological breadth.

---

## 2. Data and Execution Context

The analysis must run locally on a pandas DataFrame named `mydata`.

At the beginning of the notebook:

1. Check whether `mydata` already exists.
2. Verify that it is a pandas DataFrame.
3. If it does not exist, provide a clearly marked configuration cell where the user can specify a local CSV path.
4. Load only from that local path.
5. Do not make network calls.
6. Do not upload or transmit the dataset.
7. Do not print or display raw records.
8. Do not display exact longitude–latitude pairs.
9. Do not save transformed or row-level copies of the dataset.
10. Use a fixed random seed and report relevant package versions.

---

## 3. Expected Schema

The dataset is expected to contain approximately 20,000 rows and these nine numeric columns:

1. `longitude`
2. `latitude`
3. `housing_median_age`
4. `total_rooms`
5. `total_bedrooms`
6. `population`
7. `households`
8. `median_income`
9. `median_house_value`

Do not assume that the supplied dimensions, data types, completeness, or validity are correct. Verify them locally before analysis.

If required columns are missing, stop with an informative error identifying the missing columns.

---

## 4. Package Requirements

The core notebook should use:

- pandas
- NumPy
- Matplotlib
- scikit-learn
- SciPy
- statsmodels, when available

At the beginning of the notebook:

- Check whether required packages are installed.
- Report missing packages clearly.
- Provide commented-out installation commands when useful.
- Do not install packages automatically.
- Do not require internet access.

Optional packages must be isolated in clearly marked optional cells. Failure to import an optional package must not prevent the core notebook from running.

Optional libraries may include:

- SHAP
- XGBoost
- LightGBM
- CatBoost
- GAM-related packages

The notebook must remain complete without these optional packages.

---

## 5. Privacy-Conscious Output Restrictions

Do not print, display, or export row-level:

- Feature values.
- Coordinate pairs.
- Predictions.
- Residuals.
- Geographic-block assignments.
- Cross-validation fold assignments.
- Influence statistics.
- Error records.
- Transformed observations.

Report only:

- Aggregate statistics.
- Aggregate model metrics.
- Aggregate diagnostic results.
- Model summaries.
- Privacy-conscious figures.
- Counts and percentages of affected observations.
- Group-level results with adequate group sizes.

Do not export coordinate lookup tables, transformed datasets, row-level model outputs, or intermediate data copies.

---

## 6. Analytical Principles

Apply the following principles throughout the notebook:

- Treat every row as an area-level observation, not an individual property or household.
- Warn explicitly about ecological fallacy.
- Describe findings as associations or predictive relationships.
- Do not make causal claims.
- Distinguish statistical significance from practical significance.
- Report effect sizes and uncertainty rather than relying on p-values alone.
- Do not interpret a statistical outlier flag as proof of a data error.
- Do not remove or modify observations automatically.
- Keep the original DataFrame unchanged.
- Prevent preprocessing and model-selection leakage.
- Treat spatial validation as the primary estimate of geographic generalization.
- Use random validation only as a secondary comparison.

---

## 7. Notebook Structure

Use separate, clearly titled Markdown and code cells for:

1. Title and analytical objectives
2. Privacy-conscious analysis statement
3. Observational-data and ecological-inference limitations
4. Reproducibility settings
5. Package and environment checks
6. Safe local data acquisition
7. Schema and data-type validation
8. Data-quality assessment
9. Missing and invalid value analysis
10. Distribution and outlier diagnostics
11. Target top-coding investigation
12. Privacy-conscious exploratory visualization
13. Feature engineering
14. Spatial-block construction
15. Statistical analysis for Research Question 1
16. Statistical analysis for Research Question 2
17. Statistical analysis for Research Question 3
18. Statistical analysis for Research Question 4
19. Predictive modeling for Research Question 5
20. Random versus spatial validation comparison
21. Model interpretation
22. Sensitivity and robustness analyses
23. Answers to the five research questions
24. Limitations
25. Reproducibility and output summary

Every major result must be followed by a concise Markdown interpretation.

---

## 8. Data-Quality Assessment

Validate and summarize:

- Dataset dimensions.
- Required columns.
- Data types.
- Missing values.
- Infinite values.
- Duplicate rows.
- Constant and near-constant variables.
- Zero or negative denominators.
- Impossible or contextually suspicious values.
- Distribution skewness.
- Extreme observations.
- Multicollinearity.
- Possible target top-coding.
- Unusually influential observations.

Use complementary diagnostics when appropriate, including:

- Interquartile-range flags.
- Robust z-scores based on median absolute deviation.
- Distribution plots.
- Regression leverage and influence summaries.
- Model residual diagnostics.

Do not display row-level flagged observations.

For every treatment decision:

- Describe the evidence.
- Explain why treatment is or is not appropriate.
- Report the affected count and percentage.
- Preserve the original data.
- Compare results under an alternative treatment when conclusions could materially change.

---

## 9. Missing and Invalid Values

Check both original and engineered features for:

- Missing values.
- Positive and negative infinity.
- Invalid divisions.
- Impossible values.

Do not assume that the absence of null values means the data are valid.

If imputation is necessary:

- Select the method based on the observed distribution and missingness pattern.
- Fit the imputer only inside training folds.
- Implement it within a scikit-learn pipeline.
- Avoid target-informed imputation.
- Explain why the chosen method is appropriate.
- Report missingness only in aggregate.

Missingness indicators may be added only when justified.

---

## 10. Outlier Handling

Do not delete, cap, winsorize, or transform observations merely because they exceed an IQR or z-score threshold.

Distinguish among:

- Data-entry or measurement errors.
- Structurally impossible values.
- Plausible but extreme communities.
- Influential observations.
- Target censoring or top-coding.

Prefer robust transformations, robust estimators, or sensitivity analyses when extreme values are plausible.

If any observations are excluded:

- State the exact aggregate rule.
- Report the number and percentage excluded.
- Provide a substantive justification.
- Compare the primary conclusion with and without the exclusion.
- Never display the excluded records.

---

## 11. Target Top-Coding

Investigate whether `median_house_value` is top-coded by checking:

- The maximum observed value.
- The frequency concentrated at the maximum.
- The frequency at or near 500001.
- The target distribution near its upper boundary.

Do not assume top-coding solely because 500001 is mentioned here. Confirm it empirically.

If top-coding is detected:

- Report the affected count and percentage.
- Explain why ordinary regression cannot recover values above the cap.
- Keep the full dataset as the primary preserved source.
- Conduct at least one sensitivity analysis, such as:
  - Evaluating capped and uncapped observations separately.
  - Excluding capped observations only in a secondary analysis.
  - Using a censoring-aware method if already available and justified.
- Explain that predictions concern recorded values rather than uncensored market values.

---

## 12. Feature Engineering

Create these features safely:

- `population_per_household`
- `rooms_per_household`
- `bedrooms_per_household`
- `bedroom_to_room_ratio`

Before division:

- Validate denominators.
- Treat zero or invalid denominators explicitly.
- Convert invalid results to missing values instead of infinity.
- Report affected counts in aggregate.

Assess:

- Feature distributions.
- Skewness.
- Extreme ratios caused by small denominators.
- Correlations and multicollinearity.
- Whether logarithmic or robust transformations are justified.

Keep raw and engineered variables conceptually separate.

Do not call these ratios direct measurements of crowding unless scientifically justified. Describe them as area-level proxies.

---

## 13. Validation Protocol

Use reproducible nested cross-validation.

### Primary evaluation: spatial validation

Create geographic groups locally from longitude and latitude using quantile-based spatial bins or another clearly justified spatial-blocking method.

Requirements:

1. Do not display or export exact coordinate-to-group mappings.
2. Use five outer spatial folds when group size permits.
3. Perform hyperparameter selection only within each outer-training partition.
4. Use three inner folds for tuning.
5. Apply identical outer folds to every candidate model.
6. Report fold-level metrics only in aggregate.
7. Do not silently fall back to random validation.

If the data cannot support five spatial folds, reduce the number of folds and document why.

### Secondary evaluation: random validation

Use shuffled five-fold cross-validation with the same random seed and evaluation metrics.

Report spatial and random results separately. Treat spatial results as the primary estimate of geographic generalization.

Explain why random validation may be optimistic when nearby observations appear in both training and validation folds.

---

## 14. Research Question 1

### How strongly is household income associated with recorded housing value?

Analyze the relationship between:

- `median_income`
- `median_house_value`

Include:

- A density-aware scatterplot, hexbin plot, or equivalent.
- Pearson correlation when appropriate.
- Spearman correlation.
- Simple linear regression.
- A nonlinear alternative.
- Effect sizes and confidence intervals.
- Model fit.
- Residual diagnostics.
- Sensitivity to target top-coding.

For each inferential analysis, state:

- Null hypothesis.
- Alternative hypothesis.
- Assumptions.
- Diagnostic results.
- Estimate or test statistic.
- Confidence interval.
- P-value when appropriate.
- Practical interpretation.
- Limitations.

Do not interpret association as causation.

---

## 15. Research Question 2

### How much additional predictive information does geographic location provide after adjusting for income and housing characteristics?

Compare nested models:

- Model A: median income only.
- Model B: income plus non-geographic housing characteristics.
- Model C: Model B plus longitude and latitude.
- Model D: a justified nonlinear or interaction-based geographic model.

Compare their incremental cross-validated performance.

Use spatial validation as the primary result and random validation as a secondary comparison.

Describe the result as:

- Conditional association.
- Incremental predictive information.
- Improvement in out-of-sample prediction.

Do not describe it as the causal effect of location.

### Geographic visualization restrictions

Geographic figures must:

- Aggregate observations into spatial bins.
- Avoid one visible point per source row.
- Suppress bins containing fewer than five observations.
- Avoid interactive hover tools.
- Avoid labels or annotations revealing exact coordinates.
- Avoid exporting geographic lookup tables.

---

## 16. Research Question 3

### Are community-density and crowding proxies associated with housing values?

Evaluate:

- `population_per_household`
- `rooms_per_household`
- `bedrooms_per_household`
- `bedroom_to_room_ratio`

Adjust for:

- Median income.
- Geographic location.
- Housing age.
- Relevant community-size variables.

Check:

- Skewness.
- Influential observations.
- Multicollinearity.
- Nonlinear relationships.
- Effect sizes.
- Confidence intervals.
- Robustness to extreme ratios.

Clearly distinguish area-level proxies from direct measurements of physical crowding.

---

## 17. Research Question 4

### What is the adjusted relationship between housing-stock age and recorded housing value?

Compare:

- A linear age effect.
- A nonlinear age specification.
- Interactions with income or geographic location only when justified.

Adjust for relevant socioeconomic, geographic, and community variables.

Include:

- Effect estimates.
- Confidence intervals.
- Model diagnostics.
- A partial-effect visualization.
- A test of whether nonlinear specification improves out-of-sample performance.

Do not claim that housing age causes the observed value differences.

---

## 18. Research Question 5

### Which combination of socioeconomic, geographic, and housing characteristics best predicts recorded median housing value?

The required core models are:

- Mean or median baseline.
- Ridge regression.
- `ExtraTreesRegressor`.
- `HistGradientBoostingRegressor`.

Elastic Net may be included when convergence is stable.

Optional models may be included only if their libraries are already installed:

- XGBoost.
- LightGBM.
- CatBoost.

Use identical outer folds for all model comparisons.

All preprocessing, transformations, scaling, imputation, and feature selection must occur inside leakage-safe pipelines.

---

## 19. Model Evaluation

Use:

- Mean absolute error as the primary metric.
- Root mean squared error as a penalty-sensitive secondary metric.
- R² as a descriptive metric.
- Median absolute error when useful.

Report:

- Aggregate outer-fold performance.
- Fold-to-fold variability.
- Confidence intervals when defensible.
- Improvement over the baseline.
- Spatial-validation results.
- Random-validation results.

Never:

- Tune on the final evaluation fold.
- Fit preprocessing on the full dataset before validation.
- Compare models using different folds.
- Present only training performance.
- Hide convergence or fitting failures.

---

## 20. Model Interpretation

Use methods appropriate to each model:

- Standardized coefficients and confidence intervals for linear models.
- Permutation importance on held-out data.
- Partial-dependence plots or accumulated-local-effect plots.
- SHAP only when installed and computationally feasible.

Do not rely solely on impurity-based feature importance.

Explain that:

- Predictive importance does not establish causality.
- Correlated predictors can divide or obscure importance.
- Importance estimates can vary across validation folds.

Do not produce row-level explanation outputs.

---

## 21. Statistical Reporting

For each formal inferential procedure, provide:

- Research hypothesis.
- Null and alternative hypotheses.
- Assumptions.
- Diagnostic checks.
- Test statistic or model estimate.
- Effect size.
- Confidence interval.
- P-value when appropriate.
- Practical interpretation.
- Limitations.

Use heteroskedasticity-robust standard errors when diagnostics indicate they are appropriate.

If multiple related hypotheses are tested, apply and explain an appropriate multiple-comparison adjustment.

With 20,000 observations, emphasize practical importance because very small effects may be statistically significant.

---

## 22. Visualization Requirements

Produce publication-ready figures using measurable standards:

- Consistent typography and theme.
- Colorblind-safe palette.
- Descriptive captions.
- Labeled axes and measurement units.
- Readable legends.
- Uncertainty intervals when relevant.
- Density-aware representations for large samples.
- No unnecessary 3D effects.
- No misleading axis truncation.
- Constrained or tight layout.
- Sizes suitable for single- or double-column publication.
- Vector PDF or SVG export when supported.
- PNG fallback at a minimum of 300 DPI.

Do not claim universal compliance with every IEEE, Elsevier, or Springer journal. State that the figures follow common publication-readiness principles and may require journal-specific adjustments.

---

## 23. Error Handling

Use targeted error handling for:

- Missing local files.
- Invalid `mydata` objects.
- Missing required columns.
- Unavailable packages.
- Invalid denominators.
- Insufficient observations after filtering.
- Model convergence failures.
- Model-fitting failures.
- Figure-export failures.

Do not use broad exception handling that silently suppresses analytical errors.

Use explicit assertions and informative validation messages so critical failures stop execution.

---

## 24. References

Do not add literature citations unless the bibliographic information is known with high confidence.

Permitted references include:

- Official package documentation.
- Standard textbooks.
- Publications with complete and verifiable DOI information.

Do not invent:

- Authors.
- Titles.
- Publication years.
- Journals.
- URLs.
- DOI identifiers.

References are optional and must not be required for notebook execution.

---

## 25. Required Final Outputs

The notebook must conclude with:

1. A concise answer to each research question.
2. A comparison table of models.
3. Separate spatial- and random-validation results.
4. A summary of data-quality findings.
5. A record of preprocessing and exclusion decisions.
6. The number and percentage of top-coded observations, if detected.
7. A discussion of spatial dependence.
8. A discussion of ecological inference.
9. A discussion of residual confounding.
10. A statement distinguishing supported from unsupported conclusions.
11. A reproducibility summary.
12. A list of generated aggregate figures and output files.

The conclusions must distinguish among:

- Descriptive findings.
- Statistical associations.
- Predictive findings.
- Sensitivity-analysis findings.
- Unsupported causal interpretations.