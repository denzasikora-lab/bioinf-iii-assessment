# Assessment feedback and revision evidence

Revision date: 14 October 2026. All repository narrative, including the assignment translations, notebook, generated outputs, and PDF report, is in English. Original data, metadata, archive, and reference sequence remain unchanged.

| Feedback | Revision | Inspectable evidence |
| --- | --- | --- |
| Selection of 21 variables from the original table was vague. | Declare an explicit input protocol and a reason for every column; distinguish a fixed scope choice from statistical feature selection; compare a seven-input protocol. | ML notebook sections 3-6; ML/results/feature_audit.csv; feature_overview.csv; paired_comparisons.csv. |
| EDA focused on target, age, sex, BMI, and waist only. | Summarize all retained inputs, numeric distributions and associations, category counts, and missingness. | Notebook section 4; numeric_eda.csv; categorical_eda.csv. |
| Extra Trees had only a small advantage over Ridge. | Use identical 5x5 repeated folds, retain all paired scores, report a dependence-corrected interval, and apply a 1% complexity margin. | Notebook section 6; cv_fold_scores.csv; cv_repeat_scores.csv; paired_comparisons.csv. |
| High pressure underprediction lacked quantitative follow-up. | Report fixed-bin counts, MAE, RMSE, signed bias, underprediction frequency, large-error frequency, squared-error contributions, and conditional intervals; add training OOF diagnostics. | Notebook sections 7-8; training_errors_by_range.csv; test_errors_by_range.csv. |
| Code cells were too large. | Separate imports, audit, cleaning/split, protocol, EDA, pipelines, folds, scoring, comparison, selection, diagnostics, evaluation, and interpretation. | 41 notebook cells / 27 code cells, all executed sequentially. |
| NGS outputs lacked the corresponding shell commands. | Pair individual commands with observed outputs in the PDF; add an executable wrapper and actual transcript; distinguish historical server steps from current checks. | NGS/HBB_sequence_report.pdf and .md; reproduce.sh; reproduction.log. |

The source table has 193 non-identifier columns including the target: 192 possible inputs. The audit accounts for 194 original columns as 21 retained inputs, 171 exclusions, one target, and one identifier. This corrects the ambiguous denominator in the earlier explanation.

The 21-input Ridge improves mean RMSE over the seven-input version by 0.805%. Extra Trees improves on the 21-input Ridge by 0.898%, with an approximate corrected 95% interval of [-0.051, 0.331] mm Hg. Comparing trees against the best Ridge avoids justifying extra complexity against a deliberately reduced baseline. The declared simplicity rule selects Ridge (7 inputs).

Validated: all 27 notebook code cells executed in a fresh Python 3.14.3 kernel; no overlap of participants within train/test or CV; all prediction counts and range totals agree. The saved test result is MAE 11.570, RMSE 15.736 mm Hg, R2 0.404. The NGS wrapper completes with 147/147 exact matches and validates both file checksums. PDF pages were rendered and visually inspected.

The revised internal test set has been seen previously. The stronger CV comparison and clearer reporting do not remove that limitation. The feature and model choices were informed by the review and earlier results; no independent validation or guaranteed metric improvement is claimed.
