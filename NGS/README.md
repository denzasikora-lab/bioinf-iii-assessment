# NGS: human HBB sequence identification

The [English laboratory notebook PDF](HBB_sequence_report.pdf) identifies the individual [A114.fasta.gz](input/A114.fasta.gz) record as a 147-amino-acid protein exactly matching the pinned [UniProt P68871 reference](reference/P68871.fasta). HBB encodes hemoglobin subunit beta. Homo sapiens is the annotated organism; an exact match to one reference does not prove species uniqueness.

The report documents tools, database queries, individual shell commands, observed outputs, checksums, interpretation, and a relevant Abstract sentence with DOI [10.1016/j.retram.2025.103513](https://doi.org/10.1016/j.retram.2025.103513). Historical server acquisition and the new local reproduction are distinguished explicitly.

## Reproduce the sequence check

From the repository root, with Python 3.9 or newer:

```bash
python3 NGS/verify_sequence.py
```

Expected: `Exact positional matches: 147 / 147`. The verifier uses only the Python standard library and checks the checksum of both the input archive and the saved reference. It raises explicit errors even when Python is run with optimization enabled.

For the complete shell-command transcript, Bash, file, gzip, and shasum are also required:

```bash
bash NGS/reproduce.sh > NGS/reproduction.log 2>&1
cat NGS/reproduction.log
```

The [observed transcript](reproduction.log) was generated on 14 October 2026. Successful `gzip -t` is silent. No new task request or server login is required. The original sequence is not submitted to web services by the offline reproduction.

## Rebuild the PDF

The editable [English source](HBB_sequence_report.md) and [PDF generator](build_report.py) are included. Report generation requires reportlab; sequence verification does not.

```bash
python3 -m pip install -r NGS/report_requirements.txt
python3 NGS/build_report.py
```

Translated task instructions: [assignment_ngs.md](../docs/assignment_ngs.md).
