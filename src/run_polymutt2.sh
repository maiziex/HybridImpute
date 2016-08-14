#!/bin/bash

set -x

input1=${1}
input2=${2}
output=${3}

cat NA12878_GRCh37.vcf | awk '{if($1=="'${input1}'") print $0}' > trio_NA12878_chrxx.vcf
cat header.vcf trio_NA12878_chrxx.vcf > trio_NA12878_chrxx_final.vcf

/home/xzhou15/Software/polymutt2_v0.2/bin/vcf2map --vcf trio_NA12878_chrxx_final.vcf --ped ../CEU/trio_2.ped --map ../CEU/GeneticMap/${input2} --include_list ../CEU/1000G.SNV.clean.MAF0.05.tbl.gz --out_map chrxx.map

/home/xzhou15/Software/polymutt2_v0.2/bin/polymutt2 -p ../CEU/trio_2.ped -m chrxx.map --in_vcf trio_NA12878_chrxx_final.vcf --out_vcf ${output}


#/home/xzhou15/Software/polymutt2_v0.2/bin/vcf2map --vcf trio_NA12878_chr1_final.vcf --ped ../CEU/trio_2.ped --map ../CEU/GeneticMap/genetic_map_GRCh37_chr1.txt --include_list ../CEU/1000G.SNV.clean.MAF0.05.tbl.gz --out_map chr1.map

#/home/xzhou15/Software/polymutt2_v0.2/bin/polymutt2 -p ../CEU/trio_2.ped -m chr1.map --in_vcf trio_NA12878_chr1_final.vcf --out_vcf trio_NA12878_polymutt_chr1.vcf

rm trio_NA12878_chrxx.vcf
rm trio_NA12878_chrxx_final.vcf
rm chrxx.map



