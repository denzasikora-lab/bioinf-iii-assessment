# ML: systolic blood-pressure regression

The [executed notebook](blood_pressure_regression.ipynb) is self-contained and split into 41 cells, including 27 focused code cells. It preserves participant separation, explains all column decisions, analyzes all 21 protocol inputs, compares seven-input and 21-input Ridge with Extra Trees on 25 identical CV folds, and reports quantitative training/test errors by observed pressure range.

The simplicity rule selects **Ridge (7 inputs)**. On 1,343 reused test participants: **MAE 11.570 mm Hg**, **RMSE 15.736 mm Hg**, **R2 0.404**. The best same-input tree improvement is below 1%, and its corrected paired interval includes zero. Feature-protocol and model-selection choices are internal analyses informed by feedback, not preregistered external validation.

All 194 column decisions are in [feature_audit.csv](results/feature_audit.csv). The other [result tables](results) contain EDA summaries, fold/repeat CV scores, paired intervals, predictions, model interpretation, and error-range tables with counts, bias, MAE, RMSE, and conditional bootstrap intervals.

From the repository root after installing [requirements.txt](requirements.txt):

```bash
python ML/execute_notebook.py
```

The runner uses the active Python environment and overwrites the notebook only after successful execution. Interactive instructions are in the [main README](../README.md#reproduce-ml). CSV inputs are local and remain unchanged.

Translated instructions: [assignment_ml.md](../docs/assignment_ml.md).
