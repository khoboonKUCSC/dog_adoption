# ML work state

Status: v2 implemented, executed in the notebook, and verified on 2026-10-27.

## Completed in v2

- Replaced the v1 kitchen-sink feature set with features that survived a likelihood-ratio screen: `behavior_risk_mean`, `pets_reactivity`, `pets_reactivity_unmet`, `risk_flag_count`, `age_2plus`, and `weight_10plus`.
- Removed `class_weight='balanced'` so predicted probabilities stay on the real ~15% return scale; Brier score improved from 0.201 to 0.111.
- Model selection now uses 5-fold stratified cross-validation on the training half; the test set is touched once.
- The F2 review threshold is now chosen from out-of-fold training predictions instead of the test set.
- Added bootstrap confidence intervals, a calibration curve, a review-capacity table, and a risk-tier table.
- Removed the superseded v1 ML cells from `Untitled5.ipynb`; the final cell is self-contained and has 9 executed output blocks.

## Verification result

Dataset: 42,000 rows; 15.0% returned; 8,400-row held-out test set.

| Model | CV PR-AUC | Test PR-AUC | Test ROC-AUC | Test Brier |
| --- | ---: | ---: | ---: | ---: |
| Logistic Regression, raw features | 0.368 ± 0.015 | 0.375 | 0.759 | 0.111 |
| **Logistic Regression, engineered (selected)** | **0.371 ± 0.015** | **0.381** | **0.762** | **0.111** |
| Histogram Gradient Boosting, engineered | 0.356 ± 0.017 | 0.355 | 0.748 | 0.113 |

The selected model has a test PR-AUC of 0.381 (95% bootstrap CI 0.353–0.410) and ROC-AUC of 0.762 (95% CI 0.749–0.776).

Its out-of-fold F2 threshold is `0.107`, which flags 51.4% of test dogs and catches 82% of returns with 24% precision. Risk tiers show a clear gradient:

| Predicted risk | Dogs | Observed return rate |
| --- | ---: | ---: |
| < 5% | 1,734 | 2.8% |
| 5–10% | 2,111 | 7.0% |
| 10–15% | 1,446 | 12.7% |
| 15–25% | 1,599 | 19.4% |
| 25%+ | 1,510 | 37.7% |

For a smaller review budget, flagging the top 10% catches 29.9% of returns with 44.9% precision (3.0× lift over the 15% base rate); the top 20% catches 48.4% with 36.2% precision (2.4× lift).

Top permutation-importance signals: `aggression_score`, `pets_reactivity`, `expectation_score`, `training_level`, `behavior_risk_mean`, and `energy_mismatch`.

## v1 versus v2

| | v1 | v2 |
| --- | ---: | ---: |
| Test PR-AUC | 0.380 | 0.381 |
| Test Brier | 0.201 | 0.111 |
| F2 threshold | 0.40 (inflated scale) | 0.107 (real risk scale) |
| Model selection | single holdout | 5-fold CV on training half |
| Threshold selection | test set | out-of-fold training predictions |

## Honest interpretation

The gain in PR-AUC is small: +0.003 cross-validated and +0.007 on the test set versus the raw-feature baseline, and the bootstrap interval overlaps the baseline. The meaningful gains are calibrated probabilities and a more trustworthy evaluation. The dataset appears to have a largely additive signal; HGB, Random Forest, an MLP, and explicit pairwise interactions did not improve PR-AUC, so the linear model is close to the information ceiling.

## Next optional work

- Review the F2 threshold and review capacity with shelter stakeholders; the top-10%/top-20% rows are the practical alternatives to the recall-heavy F2 point.
- Turn the PR curve, risk-tier table, capacity table, and importance chart into final presentation slides.
- Validate on a later time period rather than only a random split.
- If more predictive power is needed, collect new pre-adoption signals (for example home visit, adopter experience details, or a follow-up call) instead of adding model complexity.
