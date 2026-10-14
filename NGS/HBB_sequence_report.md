# HBB sequence identification

Laboratory notebook | BIOINF III assessment

Author: Egor Fedosov. Stepik ID: 1370242994.

Original analysis: 5 September 2026. English revision and local reproduction: 14 October 2026. The original individual archive and the saved reference FASTA remain unchanged.

## 1. Identification and evidence

The input is one protein sequence of 147 amino acids. It exactly matches the saved canonical UniProtKB P68871 sequence, named HBB_HUMAN: hemoglobin subunit beta, gene HBB. Homo sapiens (NCBI Taxonomy ID 9606) is the organism annotated in both records.

The supplied header already provides a candidate identity. The local comparison verifies the amino-acid sequence against a separately saved reference; it is not an independent blind discovery of the gene. Exact identity to one reference does not prove that no other species has the same protein sequence.

The workflow is: inspect the individual archive, form a hypothesis from its header, check public accession annotation, compare the actual residues with the reference, and connect the identification to a relevant article. Every local command below was executed during this revision; the complete command-and-output transcript is saved in NGS/reproduction.log.

## 2. Acquisition provenance

The previous report records a single request on 5 September 2026 using the commands below. The entered details were Egor, Fedosov, and Stepik ID 1370242994. The assigned archive was A114.fasta.gz; the report states that it was downloaded with scp and that the session was closed.

```bash
ssh -p 8126 bioinf3_abit@smp4.icgbio.ru
bioinf3-testtask
exit
```

These are historical commands transcribed from the previous report, not commands rerun for this revision. The original scp command and absolute server path were not retained, so they cannot be reconstructed as an observed transcript. No new task request is needed to reproduce the analysis: use the archive already included in the repository.

## 3. Reproduce from the repository root

Python 3.9 or later is sufficient for sequence verification. The Bash wrapper additionally uses file, gzip, and shasum. It enables command tracing and stops on the first failure. The local reproduction used Python 3.14.3.

```bash
bash NGS/reproduce.sh > NGS/reproduction.log 2>&1
cat NGS/reproduction.log
```

The following pages associate each individual command with its observed result. Silent success of gzip -t means that the archive passed its integrity check; the wrapper continues only when its exit status is zero.

<!-- pagebreak -->

## 4. Archive inspection: commands and outputs

Command:

```bash
file NGS/input/A114.fasta.gz
gzip -t NGS/input/A114.fasta.gz
```

Observed result: file identified gzip-compressed data whose original name was A114.fasta and whose uncompressed size was 236 bytes. gzip -t exited with status zero and produced no output.

Command:

```bash
shasum -a 256 NGS/input/A114.fasta.gz NGS/reference/P68871.fasta
```

Observed archive SHA-256:

```text
1daa852d387c52ca6c7702821635c1048850050e0352c27501f74fd49c634682
```

Observed saved-reference SHA-256:

```text
a976e8ef07b298781398d4a66d52ddf13b796e991baa7e4e499732ecc6689107
```

Command:

```bash
gzip -cd NGS/input/A114.fasta.gz
```

Observed FASTA record (header wrapped here for layout; the stored record has one header line):

```text
>sp|P68871|HBB_HUMAN Hemoglobin subunit beta
OS=Homo sapiens OX=9606 GN=HBB PE=1 SV=2
MVHLTPEEKSAVTALWGKVNVDEVGGEALGRLLVVYPWTQRFFESFGDLSTPDAVMGNPK
VKAHGKKVLGAFSDGLAHLDNLKGTFATLSELHCDKLHVDPENFRLLGNVLVCVLAHHFG
KEFTPPVQAAYQKVVAGVANALAHKYH
```

Interpretation: sp marks a reviewed Swiss-Prot record. The accession, entry name, organism, taxonomy identifier, and gene symbol are explicit in the header. The sequence contains E, F, L, and P, among other amino-acid symbols outside the DNA alphabet, and therefore represents protein rather than nucleotide sequence.

<!-- pagebreak -->

## 5. Reference lookup and exact sequence verification

UniProtKB query: P68871. The reviewed entry annotates hemoglobin subunit beta, gene HBB, Homo sapiens, and 147 amino acids. The reference snapshot was saved on 5 September 2026 from the official REST endpoint. Its checksum pins the exact bytes used for the offline comparison.

Reference source: [UniProt FASTA endpoint](https://rest.uniprot.org/uniprotkb/P68871.fasta). Human-readable annotation: [UniProtKB P68871](https://www.uniprot.org/uniprotkb/P68871/entry).

For an optional fresh download, use this explicit command. It is a reproduction instruction, not an assertion that the identical command was retained from the original session. A current response may differ in formatting or annotation and must not silently replace the pinned reference.

```bash
curl -fL 'https://rest.uniprot.org/uniprotkb/P68871.fasta' \
  -o /tmp/P68871.current.fasta
shasum -a 256 /tmp/P68871.current.fasta
```

The previous report also records an NCBI Gene lookup with query HBB Homo sapiens and Gene ID 3043. The gene annotation identifies HBB as a protein-coding gene on chromosome 11 and links RefSeq protein NP_000509.1. This is an annotation cross-check, not a second sequence-alignment result. Source: [NCBI Gene 3043](https://www.ncbi.nlm.nih.gov/gene/3043).

Command actually executed on 14 October 2026:

```bash
python3 NGS/verify_sequence.py
```

Observed result:

```text
Length: 147 aa
Exact positional matches: 147 / 147
Identity: 100.0%; length coverage: 100.0%; substitutions: 0; gaps: 0
Sequence SHA-256:
9ebf320eb707d71644444fe5006ed58af56a0bf0ec9568eb6a3a65e0e8191465
Result: exact match to the saved UniProt P68871 canonical sequence
```

The Python script verifies checksums for both files, a single FASTA record in each file, the standard amino-acid alphabet, the reference annotation, length, and exact residue equality. Equal lengths and identical residues give 100% positional identity and length coverage without an alignment algorithm. BLAST was not run. A direct comparison is sufficient to verify this known-accession hypothesis, but does not search for alternative matches in a database.

<!-- pagebreak -->

## 6. Biological interpretation and relevant publication

HBB encodes the beta subunit of hemoglobin. Human adult hemoglobin HbA contains two alpha and two beta subunits and carries oxygen. The individual task supplies a protein sequence; it does not supply a nucleotide sequence or a participant genotype.

Relevant article: Hassan H. Almasoudi. Therapeutic promise of CRISPR-Cas9 gene editing in sickle cell disease and beta-thalassemia: A current review. Current Research in Translational Medicine, 2025, 73(3):103513. DOI: [10.1016/j.retram.2025.103513](https://doi.org/10.1016/j.retram.2025.103513). PMID: 40252393. The title above transliterates the Greek beta symbol for consistent English typography.

Bibliographic query in the previous report: EXT_ID:40252393 AND SRC:MED in Europe PMC. The DOI and the following Abstract sentence were rechecked against the [PubMed record](https://pubmed.ncbi.nlm.nih.gov/40252393/) on 14 October 2026.

> "Mutations in the hemoglobin subunit beta (HBB) gene are responsible for causing both BT and SCD."

This Abstract sentence directly connects the identified gene to beta-thalassemia and sickle cell disease. The article reviews CRISPR-Cas9 approaches in human hemoglobinopathies; it is a review rather than a new individual experiment. The citation does not imply that the supplied canonical protein carries a disease-associated variant.

## 7. Conclusion and limits of inference

The supplied record is the canonical HBB protein sequence represented by UniProtKB P68871. The complete 147-residue match and compatible annotation support this identification. Homo sapiens is the annotated organism; species uniqueness has not been established by a database-wide search. No additional model species is assigned.

Amino-acid identity does not reconstruct codons, introns, regulatory regions, or nucleotide variants. It also does not establish a person's genotype. Protein conservation can make species assignment ambiguous when only one reference is compared.

The included archive, pinned reference, Python verifier, Bash wrapper, and observed transcript reproduce the computational result offline. Internet access is needed only to revisit annotation and bibliography. The English report is generated from this Markdown source using NGS/build_report.py; this keeps future edits auditable.

## 8. Sources and access history

Original reference snapshot and annotation checks: 5 September 2026. Local checks, English revision, and PubMed verification: 14 October 2026.

* [UniProtKB P68871](https://www.uniprot.org/uniprotkb/P68871/entry).
* [Official reference FASTA](https://rest.uniprot.org/uniprotkb/P68871.fasta).
* [NCBI Gene 3043](https://www.ncbi.nlm.nih.gov/gene/3043), recorded in the original report.
* [PubMed PMID 40252393](https://pubmed.ncbi.nlm.nih.gov/40252393/).
* [Europe PMC MED/40252393](https://europepmc.org/article/MED/40252393), original bibliographic query.
