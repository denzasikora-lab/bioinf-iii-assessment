"""Offline check of the supplied FASTA against the saved UniProt P68871 record."""
from pathlib import Path
import gzip
import hashlib


ROOT = Path(__file__).resolve().parent
EXPECTED_ARCHIVE_SHA256 = '1daa852d387c52ca6c7702821635c1048850050e0352c27501f74fd49c634682'
EXPECTED_REFERENCE_SHA256 = 'a976e8ef07b298781398d4a66d52ddf13b796e991baa7e4e499732ecc6689107'


def parse_single_fasta(text):
    lines = [line.strip() for line in text.splitlines() if line.strip()]
    if not lines or not lines[0].startswith('>'):
        raise ValueError('Missing FASTA header')
    if sum(line.startswith('>') for line in lines) != 1:
        raise ValueError('Expected exactly one record')
    sequence = ''.join(lines[1:]).upper()
    if not sequence or not set(sequence) <= set('ACDEFGHIKLMNPQRSTVWY'):
        raise ValueError('Unexpected protein alphabet')
    return lines[0], sequence


def main():
    archive = ROOT / 'input/A114.fasta.gz'
    archive_hash = hashlib.sha256(archive.read_bytes()).hexdigest()
    if archive_hash != EXPECTED_ARCHIVE_SHA256:
        raise ValueError('Input archive checksum differs')
    with gzip.open(archive, 'rt', encoding='ascii') as stream:
        header, sequence = parse_single_fasta(stream.read())
    reference = ROOT / 'reference/P68871.fasta'
    reference_hash = hashlib.sha256(reference.read_bytes()).hexdigest()
    if reference_hash != EXPECTED_REFERENCE_SHA256:
        raise ValueError('Saved reference checksum differs')
    ref_header, ref_sequence = parse_single_fasta(reference.read_text(encoding='ascii'))
    if '|P68871|' not in ref_header or 'OX=9606' not in ref_header:
        raise ValueError('Saved reference annotation differs')
    if len(sequence) != 147 or len(ref_sequence) != 147:
        raise ValueError('Expected two sequences of 147 amino acids')
    matches = sum(a == b for a, b in zip(sequence, ref_sequence))
    if sequence != ref_sequence:
        raise ValueError('Sequence differs from the saved reference')
    print('Input:', archive.name)
    print('Archive SHA-256:', archive_hash)
    print('Header:', header)
    print('Length:', len(sequence), 'aa')
    print('Reference:', reference.name)
    print('Reference SHA-256:', reference_hash)
    print('Exact positional matches:', matches, '/', len(sequence))
    print('Identity: 100.0%; length coverage: 100.0%; substitutions: 0; gaps: 0')
    print('Sequence SHA-256:', hashlib.sha256(sequence.encode('ascii')).hexdigest())
    print('Result: exact match to the saved UniProt P68871 canonical sequence')


if __name__ == '__main__':
    main()
