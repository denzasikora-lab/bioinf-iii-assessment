#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "${BASH_SOURCE[0]}")/.."
set -x
date -u '+%Y-%m-%d UTC'
python3 --version
file NGS/input/A114.fasta.gz
gzip -t NGS/input/A114.fasta.gz
shasum -a 256 NGS/input/A114.fasta.gz NGS/reference/P68871.fasta
gzip -cd NGS/input/A114.fasta.gz
python3 NGS/verify_sequence.py
