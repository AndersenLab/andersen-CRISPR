from subprocess import Popen, PIPE
from on_target_score_calculator import calc_score
from itertools import islice
import sys

fasta = sys.argv[1]

dna_dict = {"A": "T",
            "T": "A",
            "G": "C",
            "C": "G",
            "N": "N",
            "n": "n"}


def window(seq, n=30):
    "Returns a sliding window (of width n) over data from the iterable"
    "   s -> (s0,s1,...s[n-1]), (s1,s2,...,sn), ...                   "
    it = iter(seq)
    result = tuple(islice(it, n))
    if len(result) == n:
        yield ''.join(result)
    for elem in it:
        result = result[1:] + (elem,)
        yield ''.join(result)


def calc_crispr(chrom, seq_set):
    pos = 0
    for sgrna in window(seq_set):
        if sgrna[4:24].endswith("G"):
            score = calc_score(sgrna)
            sgline = map(str,[chrom, pos+4, pos + 24, sgrna[4:24], score, "+"])
            print('\t'.join(sgline))
        r_sgrna = ''.join([dna_dict[x] for x in sgrna])[::-1]
        if r_sgrna[4:24].endswith("G"):
            score = calc_score(r_sgrna)
            sgline = map(str,[chrom, pos+4, pos+24, r_sgrna[4:24], score, "-"])
            print('\t'.join(sgline))
        pos += 1


sequence = ""
for line in Popen(["gzcat", fasta], stdout = PIPE).stdout:
    if line.startswith(">"):
        if sequence != "":
            sequence = sequence.upper()
            calc_crispr(chrom, sequence)
            sequence = ""
        chrom = line.strip().replace(">", "")
    else:
        sequence += line.replace("\n","")

