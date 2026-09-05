"""Offline check of the supplied FASTA against the saved UniProt P68871 record."""
from pathlib import Path
import gzip
import hashlib


ROOT = Path(__file__).resolve().parent
EXPECTED_ARCHIVE_SHA256 = '1daa852d387c52ca6c7702821635c1048850050e0352c27501f74fd49c634682'


def parse_single_fasta(text):
    lines = [line.strip() for line in text.splitlines() if line.strip()]
    assert lines and lines[0].startswith('>'), 'Missing FASTA header'
    assert sum(line.startswith('>') for line in lines) == 1, 'Expected exactly one record'
    sequence = ''.join(lines[1:]).upper()
    assert sequence and set(sequence) <= set('ACDEFGHIKLMNPQRSTVWY'), 'Unexpected protein alphabet'
    return lines[0], sequence


def main():
    archive = ROOT / 'input/A114.fasta.gz'
    archive_hash = hashlib.sha256(archive.read_bytes()).hexdigest()
    assert archive_hash == EXPECTED_ARCHIVE_SHA256, 'Input archive checksum differs'
    with gzip.open(archive, 'rt', encoding='ascii') as stream:
        header, sequence = parse_single_fasta(stream.read())
    reference = ROOT / 'reference/P68871.fasta'
    ref_header, ref_sequence = parse_single_fasta(reference.read_text(encoding='ascii'))
    assert '|P68871|' in ref_header and 'OX=9606' in ref_header
    assert len(sequence) == len(ref_sequence) == 147
    matches = sum(a == b for a, b in zip(sequence, ref_sequence))
    assert sequence == ref_sequence, 'Sequence differs from the saved reference'
    print('Input:', archive.name)
    print('Archive SHA-256:', archive_hash)
    print('Header:', header)
    print('Length:', len(sequence), 'aa')
    print('Reference:', reference.name)
    print('Exact positional matches:', matches, '/', len(sequence))
    print('Identity: 100.0%; length coverage: 100.0%; substitutions: 0; gaps: 0')
    print('Sequence SHA-256:', hashlib.sha256(sequence.encode('ascii')).hexdigest())
    print('Result: exact match to the saved UniProt P68871 canonical sequence')


if __name__ == '__main__':
    main()
