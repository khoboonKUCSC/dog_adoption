# Dog adoption return-risk modelling plan

## Objective

Predict whether an adopted dog will be returned (`returned = 1`) using information available at, or before, the adoption decision. The result supports a human review of potentially risky matches; it is not an automatic adoption decision.

## Guardrail: prevent target leakage

Never train on `adoption_id`, `return_reason`, `days_to_return`, `success`, or `outcome`. The last four are known only after the adoption outcome (and `success`/`outcome` are derived from `returned`).

## Workflow (v2)

1. Reload the unmodified master CSV and create a stratified 80/20 train/test split (`random_state=42`). The test half is held out until the final report.
2. Engineer pre-adoption features:
   - behavioural burden (`behavior_risk_mean`) and a `risk_flag_count`;
   - pet/reactivity match (`pets_reactivity`, `pets_reactivity_unmet`);
   - change-of-slope indicators for age and weight (`age_2plus`, `weight_10plus`).
   Retain only interactions that survived a likelihood-ratio screen; the earlier "kitchen-sink" feature set is dropped.
3. Median-impute numeric values and one-hot encode categorical values inside a pipeline, so imputation/encoding are fitted on training folds only.
4. Compare three candidates with 5-fold stratified cross-validation **on the training half**:
   - Logistic Regression on raw features (baseline);
   - Logistic Regression on engineered features (selected);
   - Histogram Gradient Boosting on engineered features (non-linear benchmark).
   Select by PR-AUC because returned dogs are the ~15% minority; report ROC-AUC as a secondary metric.
5. Evaluate the selected model once on the 20% test set: PR-AUC and ROC-AUC with bootstrap confidence intervals, Brier score, and a calibration curve.
6. Choose the review threshold by F2 on **out-of-fold training predictions**, prioritising recall without tuning on the test set. Report the confusion matrix.
7. Add review-capacity and risk-tier tables so stakeholders can trade review effort for caught returns.
8. Use permutation importance on held-out data (8 repeats, PR-AUC) for the presentation-ready ranking of influential factors.

## Why class weighting was removed

`class_weight='balanced'` leaves the ranking almost unchanged but inflates predicted probabilities (mean risk ≈ 0.50 instead of 0.15). That makes the threshold and Brier score misleading. The unweighted likelihood keeps probabilities on the real return-rate scale, so a 10% score means roughly a 10% observed return risk.

## Ceiling note

The signal in this dataset is predominantly additive. Simulating labels from the fitted probabilities puts the expected PR-AUC at about 0.387; the selected model reaches about 0.381 on the test set. Histogram Gradient Boosting, Random Forest, an MLP, and L1-regularised pairwise interactions all failed to beat the linear model. Further gains require new pre-adoption predictors or validation on a later time period, not a more complex algorithm.

## Deliverable

The executable pipeline is the final code cell in `Untitled5.ipynb`. It prints the cross-validated model comparison, test metrics with confidence intervals, precision-recall curves, confusion matrix, calibration plot, review-capacity and risk-tier tables, and the ranked permutation-importance chart.
