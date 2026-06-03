# Mock Member Health Analysis

A synthetic healthcare analytics and machine learning portfolio project built to practice Python, exploratory data analysis, feature engineering, classification modeling, regression modeling, model interpretation, and leakage-aware evaluation.

This project uses fully synthetic healthcare-style data generated for portfolio and learning purposes. It does **not** contain real patient data, PHI, claims data, employer data, or production healthcare records. Results should be interpreted as a modeling workflow demonstration, not real-world clinical or financial evidence.

## Executive Summary

| Area                  | Summary                                                                                                                          |
| --------------------- | -------------------------------------------------------------------------------------------------------------------------------- |
| Problem               | Predict AWV completion and monthly healthcare cost using synthetic member-level healthcare data                                  |
| Methods               | EDA, leakage-aware feature engineering, classification modeling, regression modeling, residual diagnostics, and model comparison |
| Classification Result | Logistic Regression was selected as the stronger baseline model for AWV completion prediction                                    |
| Regression Result     | Gradient Boosting was selected as the best model for monthly cost prediction                                                     |
| Caveat                | This is a synthetic workflow project, not real-world healthcare evidence                                                         |

Final regression model performance: Gradient Boosting achieved approximately MAE `$370.87`, RMSE `$643.58`, and R² `0.772` on the held-out test set.

## Project Overview

This project analyzes a synthetic member-level health plan dataset with 3,000 mock members. Each row represents one member and includes simulated demographic, plan, SDOH, engagement, PCP attribution, utilization, cost, prior AWV behavior, and current-year AWV completion fields.

The project includes two supervised learning tracks:

1. **AWV Completion Classification**
   Predict whether a member completed an Annual Wellness Visit.

2. **Monthly Cost Regression**
   Predict simulated monthly healthcare cost.

The main focus of the project is not to prove real healthcare findings, but to demonstrate a complete data science workflow: data generation, EDA, feature engineering, leakage prevention, baseline modeling, model tuning, residual diagnostics, model comparison, and careful interpretation.

## Start Here

Recommended notebooks for a quick review:

| Notebook                                     | Purpose                                                               |
| -------------------------------------------- | --------------------------------------------------------------------- |
| `01_Exploratory_Data_Analysis.ipynb`         | Understand the synthetic member population and key feature patterns   |
| `04_model_interpretation.ipynb`              | Review AWV classification interpretation and threshold logic          |
| `09_residual_diagnostics.ipynb`              | Evaluate regression residual behavior and high-cost prediction errors |
| `15_final_regression_model_comparison.ipynb` | Compare final regression models                                       |
| `16_project_summary.ipynb`                   | Review the full project summary                                       |

## Reproducibility: How to Run This Project

To reproduce the project workflow:

1. Clone the repository.

```bash
git clone https://github.com/doyounghi/synthetic-data-analysis.git
cd synthetic-data-analysis/01_mock_member_health_analysis
```

2. Create and activate a virtual environment.

```bash
python -m venv .venv
```

On Windows:

```bash
.venv\Scripts\activate
```

On Mac/Linux:

```bash
source .venv/bin/activate
```

3. Install required packages.

```bash
pip install -r requirements.txt
```

4. Generate the synthetic dataset.

```bash
python src/generate_data.py
```

5. Launch Jupyter.

```bash
jupyter notebook
```

6. Run the notebooks in order from `01` to `16`.

Notebook outputs may vary slightly depending on package versions and random seeds, but the main modeling workflow and conclusions should remain consistent.

Generated and processed data files are stored under:

```text
data/raw/
data/processed/
```

### Notebook 1 : Exploratory Data Analysis

This notebook performs initial exploratory analysis on a synthetic healthcare member dataset. Each row represents one health plan member with demographic, plan, SDOH, utilization, cost, PCP attribution, and AWV completion fields.

The analysis checks data structure, missing values, duplicate member IDs, categorical distributions, numeric ranges, and basic visualizations. It also compares cost, utilization, and AWV completion patterns across plan type, region, PCP attribution, chronic condition burden, engagement quartiles, and age groups.

Key findings:
- DSNP members showed higher average SDOH risk, ED visits, and monthly cost.
- Rural members showed higher average SDOH risk, lower engagement, and higher ED utilization.
- PCP-attributed members had higher AWV completion and lower average utilization.
- AWV completion increased strongly across engagement score quartiles.
- Non-AWV-compliant members had higher average monthly cost in this synthetic dataset.

These findings are descriptive and should not be interpreted causally.

### Notebook 2 : Feature Engineering

- Loaded the EDA-ready synthetic healthcare member dataset from the prior notebook.
- Created stakeholder-friendly analytical features including age group, engagement quartile, chronic burden group, SDOH risk quartile, prior AWV group, PCP attribution status, acute utilization flag, and high-cost member flag.
- Defined high-cost members as the top 25% of monthly cost, creating a potential future classification target.
- Validated engineered features by checking distributions and grouped summaries.
- Found that higher chronic burden, higher acute utilization, older age, and higher SDOH risk were associated with higher average monthly cost.
- Found that AWV completion was higher among members with stronger engagement and prior AWV history.
- Exported the analysis-ready dataset to `data/processed/member_analysis_ready.csv`.

These findings are descriptive and based on synthetic data. They should not be interpreted causally.

### Notebook 3 : Modeling Baseline

- Built baseline classification models to predict current-year Annual Wellness Visit (AWV) completion.
- Used `awv_completed` as the binary target variable.
- Reviewed the synthetic data-generation logic to confirm which predictors were created before the AWV outcome.
- Excluded identifier fields, cost-related outcome variables, full-dataset quartile features, and redundant engineered grouping variables from the predictor set.
- Specifically excluded `member_id`, `monthly_cost`, `high_cost_member`, `engagement_group`, `sdoh_risk_group`, `age_group`, `chronic_burden_group`, `pcp_status`, `total_acute_visits`, `acute_utilization_group`, `has_acute_utilization`, `prior_awv_count`, and `prior_awv_group`.
- Split the data into training and test sets using an 80/20 stratified split.
- Applied one-hot encoding to categorical variables and standard scaling to numeric variables using a scikit-learn preprocessing pipeline.
- Compared Logistic Regression and Decision Tree Classifier baseline models.
- Evaluated performance using accuracy, precision, recall, F1 score, ROC AUC, confusion matrix, and classification report.
- Logistic Regression performed better than the Decision Tree, with ROC AUC of 0.76 and F1 score of 0.71.
- Treated Logistic Regression as the stronger baseline model for future threshold tuning, coefficient interpretation, and model comparison.
- Results should be interpreted as baseline model performance only, not as a final production model.

### Notebook 4: Model Interpretation and Threshold Tuning

- Rebuilt the baseline Logistic Regression model for AWV completion prediction using the cleaned predictor set from Notebook 3.
- Excluded cost-related outcome variables, full-dataset quartile features, and redundant engineered grouping variables to keep coefficient interpretation cleaner.
- Split the data into training, validation, and test sets so threshold tuning could be performed on validation data while preserving a final untouched test set.
- Applied one-hot encoding to categorical variables and standard scaling to numeric variables using a scikit-learn pipeline.
- Evaluated the model using accuracy, precision, recall, F1 score, ROC AUC, confusion matrix, and classification report.
- Extracted Logistic Regression coefficients and converted them into odds ratios for interpretation.
- Interpreted numeric coefficients as one-standard-deviation changes because numeric predictors were standardized.
- Interpreted categorical coefficients relative to omitted reference categories because one-hot encoding used `drop="first"`.
- Tested classification thresholds from 0.30 to 0.70 and selected 0.40 based on validation F1 score.
- Applied the selected 0.40 threshold once to the final test set, producing test recall of 0.84 and test F1 score of 0.73.
- Results are based on synthetic data and should be interpreted as baseline model behavior, not causal effects or final production performance.

### Notebook 5: Cost Prediction Regression

- Built a baseline multiple linear regression model to predict monthly member cost.
- Used `monthly_cost` as the continuous regression target.
- Excluded `member_id` because it is an identifier and excluded `high_cost_member` because it is derived directly from monthly cost.
- Excluded `awv_completed` to keep the baseline model focused on member characteristics, risk, access, engagement, and utilization features.
- Removed redundant engineered grouping variables where raw source variables were already available, improving coefficient interpretability.
- Applied one-hot encoding to categorical variables and standard scaling to numeric variables using a scikit-learn preprocessing pipeline.
- Evaluated performance using MAE, MSE, RMSE, and R².
- The baseline Linear Regression model achieved MAE of about `$404`, RMSE of about `$654`, and R² of about `0.76` on the test set.
- Reviewed regression coefficients as conditional associations, not causal effects.
- Found that chronic condition count, inpatient admissions, ED visits, and plan type were among the strongest cost-associated predictors.
- Used actual-vs-predicted and residual plots to identify model error patterns.
- Found that the model captured average cost patterns reasonably well but underpredicted some very high-cost members.
- Results are based on synthetic data and should be interpreted as baseline model behavior, not final production performance.

### Notebook 6: Standardized Feature Influence

This notebook extends the baseline monthly cost regression model by comparing feature influence after standardizing numeric predictors. The target variable was monthly_cost. Identifier fields, direct target-derived fields, same-year AWV completion, full-dataset grouped features, and redundant engineered variables were excluded to reduce leakage risk and improve interpretability.

Numeric features were standardized with StandardScaler, and categorical features were one-hot encoded with a dropped reference category. A Linear Regression model was fit using a scikit-learn pipeline.

The model achieved MAE of about $404, RMSE of about $654, and R² of about 0.76 on the test set. Among standardized numeric predictors, chronic condition count, inpatient admissions, and ED visits showed the strongest positive associations with predicted monthly cost. Plan type coefficients were interpreted relative to the omitted reference category.

The results are based on synthetic data and should be interpreted as conditional model associations, not causal effects.

### Notebook 7: Regularized Regression

- Compared baseline Linear Regression with Ridge Regression and Lasso Regression for monthly cost prediction.
- Used `monthly_cost` as the continuous regression target.
- Kept the same clean predictor set from the baseline cost regression notebook to maintain consistency.
- Excluded `member_id`, `high_cost_member`, `awv_completed`, grouped/qcut features, and redundant engineered variables to reduce leakage risk and improve interpretability.
- Applied one-hot encoding to categorical predictors and standard scaling to numeric predictors using a scikit-learn preprocessing pipeline.
- Evaluated all models using MAE, RMSE, and R².
- Found that Linear Regression, Ridge Regression, and Lasso Regression produced nearly identical performance.
- Ridge and Lasso did not materially improve model generalization in this setup.
- Lasso did not set any coefficients to zero at `alpha = 0.1`, so the fitted Lasso model should not be described as sparse.
- Reviewed coefficient shrinkage to understand how regularization affects model coefficients.
- Added a model comparison visualization to show that error metrics were nearly unchanged across models.
- Concluded that the current feature set is already relatively clean and does not show strong evidence that regularization improves prediction performance.
- Identified cross-validated alpha tuning using `RidgeCV`, `LassoCV`, or `GridSearchCV` as a logical next step.

Results should be interpreted as synthetic baseline model behavior, not real-world causal evidence.

### Notebook 8: Regularized Regression Tuning

- Tuned Ridge Regression and Lasso Regression models for monthly cost prediction using cross-validation.
- Used `monthly_cost` as the continuous regression target.
- Used the same cleaned cost-prediction feature set from the previous regression notebooks.
- Excluded `member_id`, `high_cost_member`, `awv_completed`, full-dataset grouped features, and redundant engineered variables to reduce leakage risk and keep comparisons consistent.
- Applied one-hot encoding to categorical predictors and standard scaling to numeric predictors using a scikit-learn preprocessing pipeline.
- Used `GridSearchCV` with 5-fold cross-validation to select regularization strength values for Ridge and Lasso.
- Compared baseline Linear Regression, tuned Ridge Regression, and tuned Lasso Regression on the held-out test set.
- Evaluated models using MAE, RMSE, and R².
- Found that tuned Ridge and tuned Lasso performed only slightly better than baseline Linear Regression.
- Concluded that regularization tuning did not materially improve performance because the cleaned feature set was already relatively stable.
- Reviewed tuned coefficients and Lasso sparsity.
- Results are based on synthetic data and should be interpreted as model-comparison findings, not causal evidence.

### Notebook 9: Residual Diagnostics

- Rebuilt the tuned Ridge regression model to evaluate residual behavior for monthly cost prediction.
- Used the same cleaned cost-prediction feature set as the prior regression notebooks.
- Defined residuals as actual monthly cost minus predicted monthly cost.
- Interpreted positive residuals as underpredictions and negative residuals as overpredictions.
- Evaluated model performance using MAE, RMSE, R², mean residual, and median residual.
- Reviewed actual-vs-predicted plots, residual-vs-predicted plots, residual distribution, largest-error cases, error bands, and residuals by cost group.
- Found that the model captured average cost patterns reasonably well but struggled with high-cost members.
- Found that lower-cost groups were generally overpredicted while high-cost groups were underpredicted.
- Concluded that the tuned Ridge model compresses predictions toward the middle, which is common when modeling right-skewed healthcare cost data with linear models.
- Identified log-transformed regression, Random Forest, and Gradient Boosting as logical next approaches for handling skewed cost outcomes.

### Notebook 10: Tree-Based Regression

- Compared an unrestricted Decision Tree Regressor with a controlled Decision Tree Regressor for monthly cost prediction.
- Used the same cleaned cost-prediction feature set as the previous regression notebooks.
- Excluded leakage-prone fields, full-dataset grouped features, and redundant engineered variables.
- Evaluated train and test performance using MAE, RMSE, and R².
- Found that the unrestricted decision tree perfectly memorized the training data, producing train MAE of 0, train RMSE of 0, and train R² of 1.0.
- Found that the unrestricted tree performed much worse on the test set, showing clear overfitting.
- Built a controlled decision tree using `max_depth=5` and `min_samples_leaf=25`.
- Found that the controlled tree had worse training performance but better test performance than the unrestricted tree, indicating improved generalization.
- Added a train-vs-test visualization to show overfitting behavior.
- Reviewed residual behavior and feature importance for the controlled tree.
- Found that chronic condition count, inpatient admissions, and ED visits were the most important split variables.
- Concluded that a controlled decision tree captures some nonlinear patterns but does not outperform the tuned Ridge regression model in this synthetic dataset.
- Identified Random Forest and Gradient Boosting as logical next ensemble tree methods.

### Notebook 11: Random Forest Regression

- Built a Random Forest Regressor for monthly cost prediction.
- Used the same cleaned cost-prediction feature set as the previous regression notebooks.
- Excluded `member_id`, `high_cost_member`, `awv_completed`, full-dataset grouped features, and redundant engineered variables to reduce leakage risk and maintain comparison consistency.
- Applied preprocessing through a scikit-learn pipeline.
- Evaluated train and test performance using MAE, RMSE, and R².
- Found that the Random Forest performed better on the training set than the test set, suggesting some overfitting.
- Found that Random Forest generalized much better than a single unrestricted decision tree.
- Compared Random Forest against the controlled Decision Tree from Notebook 10.
- Found that Random Forest improved over the controlled Decision Tree on test-set error.
- Reviewed residual behavior and feature importance.
- Found that chronic condition count, inpatient admissions, and ED visits were the most important predictors in the fitted Random Forest model.
- Concluded that Random Forest improved over a single decision tree but did not clearly outperform the tuned Ridge regression model.
- Identified Random Forest hyperparameter tuning as the next step.

### Notebook 12: Random Forest Hyperparameter Tuning

- Tuned a Random Forest Regressor for monthly cost prediction using cross-validation.
- Used the same cleaned cost-prediction feature set as the previous regression notebooks.
- Excluded leakage-prone fields, full-dataset grouped features, and redundant engineered variables.
- Used `GridSearchCV` with 5-fold cross-validation to tune Random Forest hyperparameters.
- Tuned parameters included number of trees, maximum tree depth, minimum samples per leaf, and maximum features considered at each split.
- Rebuilt the baseline Random Forest inside the notebook to ensure a fair comparison using the same train/test split.
- Compared baseline Random Forest and tuned Random Forest using MAE, RMSE, and R² on the held-out test set.
- Found that the tuned Random Forest slightly improved over the baseline Random Forest.
- Concluded that the improvement was small and not practically meaningful.
- Reviewed feature importance from the tuned model.
- Found that chronic condition count, inpatient admissions, and ED visits remained the most important predictors.
- Concluded that Random Forest tuning helped slightly but did not clearly outperform the tuned Ridge model or later Gradient Boosting model.

### Notebook 13: Gradient Boosting Regression

- Built a Gradient Boosting Regressor for monthly cost prediction.
- Used the same cleaned cost-prediction feature set as the prior regression notebooks.
- Excluded `member_id`, `high_cost_member`, `awv_completed`, full-dataset grouped features, and redundant engineered variables to reduce leakage risk.
- Tested whether a sequential tree-based ensemble could improve prediction performance compared with Random Forest and regularized linear models.
- Evaluated train and test performance using MAE, RMSE, and R².
- Found that Gradient Boosting achieved strong test-set performance, with lower MAE and RMSE than the prior Random Forest models.
- Reviewed actual-vs-predicted and residual plots to evaluate prediction behavior.
- Reviewed feature importance from the fitted Gradient Boosting model.
- Found that chronic condition count, inpatient admissions, and ED visits were the most important predictors.
- Compared Gradient Boosting against prior models, including tuned Ridge, controlled Decision Tree, baseline Random Forest, and tuned Random Forest.
- Found that Gradient Boosting produced the strongest test-set performance among the models compared up to this point.
- Concluded that Gradient Boosting captured nonlinear cost patterns better than the previous models in this synthetic dataset.

### Notebook 14: Gradient Boosting Hyperparameter Tuning

- Tuned a Gradient Boosting Regressor for monthly cost prediction using cross-validation.
- Used the same cleaned cost-prediction feature set as the prior regression notebooks.
- Excluded leakage-prone fields, full-dataset grouped features, and redundant engineered variables.
- Used `GridSearchCV` with 5-fold cross-validation to tune Gradient Boosting hyperparameters.
- Tuned parameters included number of boosting stages, learning rate, maximum tree depth, and minimum samples per leaf.
- Evaluated the tuned model on the held-out test set using MAE, RMSE, and R².
- Compared tuned Gradient Boosting against baseline Gradient Boosting.
- Found that tuned Gradient Boosting performed almost the same as baseline Gradient Boosting.
- Found that MAE and RMSE were slightly worse after tuning, while R² was only slightly better.
- Concluded that hyperparameter tuning did not materially improve Gradient Boosting performance in this run.
- Reviewed actual-vs-predicted plots, residual plots, and feature importance.
- Found that chronic condition count, inpatient admissions, and ED visits remained the most important predictors.
- Concluded that the baseline Gradient Boosting model remained the stronger practical choice.

### Notebook 15: Final Regression Model Comparison

- Compared all regression models developed for monthly cost prediction.
- Included Linear Regression, Ridge Regression, Lasso Regression, Decision Tree, Random Forest, Tuned Random Forest, Gradient Boosting, and Tuned Gradient Boosting.
- Manually collected held-out test-set metrics from prior regression notebooks.
- Stored model results using numeric MAE, RMSE, and R² values to support ranking and visualization.
- Ranked models by MAE, RMSE, and R².
- Used RMSE as the primary model-selection metric because healthcare cost prediction is sensitive to large errors among high-cost members.
- Found that Gradient Boosting had the lowest MAE, lowest RMSE, and highest R² among the compared models.
- Found that Tuned Gradient Boosting did not outperform baseline Gradient Boosting.
- Selected baseline Gradient Boosting Regressor as the final regression model.
- Explained why the tuned Gradient Boosting model was not selected despite additional tuning.
- Added visual comparisons for RMSE, MAE, and R².
- Added limitations explaining that the results are based on synthetic data, manually collected metrics, and tested models only.
- Concluded that Gradient Boosting was the strongest model in this synthetic monthly cost prediction project, while emphasizing that results are predictive and not causal.

### Notebook 16: Project Summary

- Summarized the full synthetic healthcare analytics and machine learning workflow.
- Reviewed the two supervised learning tracks: AWV completion classification and monthly cost regression.
- Highlighted key modeling decisions, including leakage prevention, feature selection, model comparison, and final model selection.
- Explained why Logistic Regression was selected as the stronger AWV classification baseline.
- Explained why Gradient Boosting was selected as the final monthly cost regression model.
- Reinforced that results are based on synthetic data and should be interpreted as workflow demonstration, not real-world healthcare evidence.