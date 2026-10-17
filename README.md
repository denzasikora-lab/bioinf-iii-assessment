# BIOINF III: ML and NGS assessment solutions

Author: **Egor Fedosov**. Original analysis: 5 September 2026. English revision and reproduction: 14 October 2026.

This repository contains a reproducible regression notebook and an English laboratory notebook for protein-sequence identification. The revision makes feature selection auditable, strengthens model comparison, quantifies errors across target ranges, splits the notebook into focused cells, and pairs NGS commands with their actual outputs.

| Part | Deliverable | Main result |
| --- | --- | --- |
| ML | [Executed notebook](ML/blood_pressure_regression.ipynb) | Ridge (7 inputs): MAE 11.570, RMSE 15.736 mm Hg, R2 0.404 |
| NGS | [English PDF laboratory notebook](NGS/HBB_sequence_report.pdf) | HBB / hemoglobin subunit beta, 147 amino acids; exact match to UniProt P68871 |

## ML: predicting systolic blood pressure

The supplied [NHANES CSV and metadata](ML/data) have 8,533 rows and 194 columns. Removing 167 exact duplicate rows leaves 8,366 unique participants, including 6,714 with a measured target. Participants with no target are excluded from supervised learning. The unchanged corrected split has 5,371 training and 1,343 test participants. All EDA uses training participants; preprocessing is fitted inside each CV training fold.

The 193 non-identifier variables include the target, so there are 192 potential inputs. The [complete column audit](ML/results/feature_audit.csv) records one decision and reason for every original column: one identifier, one target, 21 retained protocol inputs, and 171 excluded inputs. This is a declared screening protocol, not an assertion that excluded variables are irrelevant. It assumes access to specified metabolic laboratory results and excludes the entire blood-pressure examination. The notebook analyzes all 21 retained inputs and compares them with seven demographic/anthropometric inputs.

The median baseline, two fixed Ridge protocols, and Extra Trees use the same 25 training-only folds (five folds repeated five times). [Fold-level results](ML/results/cv_fold_scores.csv), [repeat-level results](ML/results/cv_repeat_scores.csv), and [corrected paired comparisons](ML/results/paired_comparisons.csv) are included.

| Candidate | Mean CV RMSE, mm Hg | Mean CV MAE, mm Hg |
| --- | ---: | ---: |
| Extra Trees (21 inputs) | 15.460 | 11.262 |
| Ridge (21 inputs) | 15.600 | 11.491 |
| Ridge (7 inputs) | 15.726 | 11.567 |
| Median baseline | 20.682 | 15.469 |

Extra Trees improves mean RMSE over the 21-input Ridge by only **0.898%**. Its approximate 95% corrected paired interval for the RMSE reduction is **[-0.051, 0.331] mm Hg**, including zero. The seven-input Ridge is only **0.81%** worse than the 21-input Ridge. The declared 1% practical margin and corrected-interval rule therefore select **Ridge (7 inputs)**. This trades a small internal CV difference for fewer inputs and a simpler model. The margin is an analysis choice, not a clinical criterion.

On the reused internal test split: **MAE 11.570 mm Hg**, **RMSE 15.736 mm Hg**, **R2 0.404**. Errors are quantified rather than assessed from plots alone:

| Observed pressure, mm Hg | Participants | MAE | RMSE | Bias: predicted - observed |
| --- | ---: | ---: | ---: | ---: |
| <100 | 136 | 12.69 | 15.33 | 12.69 |
| 100 to <120 | 579 | 9.63 | 12.59 | 6.55 |
| 120 to <140 | 401 | 7.89 | 9.83 | -0.49 |
| 140 to <160 | 157 | 14.80 | 17.00 | -14.72 |
| >=160 | 70 | 39.27 | 42.21 | -39.27 |

At >=160 mm Hg, **70 participants** have a mean error of **-39.27 mm Hg**, and **100.0%** are underpredicted. This bin contributes **37.5%** of total squared error. [Detailed range results](ML/results/test_errors_by_range.csv) include conditional bootstrap intervals and large-error frequencies; [training out-of-fold diagnostics](ML/results/training_errors_by_range.csv) show whether the pattern is already present in training validation predictions.

The test participants were inspected in earlier versions and again for this revision, which was informed by assessment feedback. These are internal results, not independent external validation. No post-test optimization is claimed. The analysis does not incorporate the NHANES survey design or weights and cannot establish population-wide or clinical performance.

## Reproduce ML

Tested with Python 3.14.3. From the repository root:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r ML/requirements.txt
python ML/execute_notebook.py
```

The runner executes all 27 code cells in a fresh kernel using the active Python interpreter and saves outputs to the notebook. CSV results are regenerated in `ML/results`. Data are already included; execution needs no network. The full repeated tree comparison takes longer than a single five-fold run.

For interactive work:

```bash
python -m ipykernel install --prefix .venv --name bioinf-iii --display-name 'BIOINF III'
python -m jupyterlab
```

Open `ML/blood_pressure_regression.ipynb`, select **BIOINF III**, and choose **Restart Kernel and Run All Cells**. Dependencies are pinned in [requirements.txt](ML/requirements.txt).

## NGS: sequence identification

The individual [A114.fasta.gz](NGS/input/A114.fasta.gz) archive contains a single protein sequence of **147 amino acids**. Its header identifies P68871 / HBB_HUMAN, HBB, Homo sapiens, and Taxonomy ID 9606. Comparing the actual sequence with the pinned [UniProt reference](NGS/reference/P68871.fasta) confirms **147/147 positional matches**, **100% identity**, and **100% length coverage**, with no substitutions or gaps. Organism assignment follows the annotation; a one-reference comparison does not prove species uniqueness.

The [English PDF](NGS/HBB_sequence_report.pdf) contains commands, outputs, checksum validation, annotation queries, reasoning, limits, and one short Abstract quotation with DOI [10.1016/j.retram.2025.103513](https://doi.org/10.1016/j.retram.2025.103513). An [editable report source](NGS/HBB_sequence_report.md), [PDF generator](NGS/build_report.py), and [actual command transcript](NGS/reproduction.log) are included. Missing details of the historical server download are identified explicitly.

## Reproduce NGS

Python 3.9 or newer; no third-party packages are needed for sequence verification:

```bash
python3 NGS/verify_sequence.py
```

Expected: `Exact positional matches: 147 / 147`. For all inspection commands with tracing (Bash, file, gzip, and shasum required):

```bash
bash NGS/reproduce.sh > NGS/reproduction.log 2>&1
```

The verifier checks both input and reference checksums, format, alphabet, annotation, length, and exact identity. The original task request must not be repeated. See [NGS/README.md](NGS/README.md) for PDF regeneration.

## Additional preparation and task provenance

The [certificate portfolio](https://denzasikora-lab.github.io/demo/cert/) contains additional training in bioinformatics, ML, and AI, including Wellcome Connecting Science courses in Linux, Bash, and R for biologists, the Stanford Machine Learning Specialization, and Harvard CS50 AI with Python, with document-verification links.

English translations of the supplied task instructions are in [docs](docs). The original task source is [BIOINF-III-assessment](https://github.com/bioinformaticsinstitute/BIOINF-III-assessment). [Revision notes](docs/revision_notes.md) map the assessment feedback to the changes and validation evidence.
