
# Retrieve and index genome with samtools faidx
curl ftp://ftp.wormbase.org/pub/wormbase/species/c_elegans/sequence/genomic/c_elegans.PRJNA13758.WS248.genomic.fa.gz > c_elegans.PRJNA13758.WS248/c_elegans.PRJNA13758.WS248.genomic.fa.gz
gunzip c_elegans.PRJNA13758.WS248/c_elegans.PRJNA13758.WS248.genomic.fa.gz
bgzip c_elegans.PRJNA13758.WS248/c_elegans.PRJNA13758.WS248.genomic.fa
samtools faidx c_elegans.PRJNA13758.WS248/c_elegans.PRJNA13758.WS248.genomic.fa.gz

# Retrieve python script
curl "http://www.broadinstitute.org/rnai/public/dir/download?dirpath=software&filename=on_target_score_calculator.py" > on_target_score_calculator.py 

# Generate sgRNAs; Note that this filters 
python calculate.py c_elegans.PRJNA13758.WS248/c_elegans.PRJNA13758.WS248.genomic.fa.gz | awk '$5 > 0.7' | bgzip > sgRNA_scores.bed.gz
tabix -f sgRNA_scores.bed.gz

