# Run Quast 

## Running The Code:
### Step 1: 
```
python QuastXX_step1.py -l 10000 -i ../Lysis_Cr_0.2/supernova_contig.fasta -o_dir ../Lysis_Cr_0.2/ -r /oak/stanford/groups/arend/Xin/SimProj/Quast_results/genome_na12878.fa.gz
```
```
usage: QuastXX_step1.py [-h] [--lines LINES] [--input_file INPUT_FILE]
                        [--out_dir OUT_DIR] [--reference REFERENCE]

Run Quast for 10X data -- step1: Split WGS contig file to multiple small files
(maximum 100 files, so make sure total_lines_of_WGS_contig_file/lines <= 100),
and run Quast separately

optional arguments:
  -h, --help            show this help message and exit
  --lines LINES, -l LINES
                        line number for each small contig file
  --input_file INPUT_FILE, -i INPUT_FILE
                        Input contig filename
  --out_dir OUT_DIR, -o_dir OUT_DIR
                        Directory to store outputs
  --reference REFERENCE, -r REFERENCE
                        Referece fasta file
```

### Step 2: 
```
python QuastXX_step2.py -o_dir ../Lysis_Cr_0.2/
```
```
usage: QuastXX_step2.py [-h] [--out_dir OUT_DIR]

Run Quast for 10X data -- step2: Concatenate all quast alignment files
together to generate file: all_alignments_supernova_contig-fasta.tsv

optional arguments:
  -h, --help            show this help message and exit
  --out_dir OUT_DIR, -o_dir OUT_DIR
                        Directory to store outputs
```
