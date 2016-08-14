#!/bin/bash

for i in {1..22}
do
    chr="chr"
    chr_num=$chr$i

    output_prefix="trio_NA12878_chr"
    output_suffix=".vcf"
    output_name=$output_prefix$i$output_suffix

    cat NA12878_GRCh37.vcf | awk '{if($1=="'$chr_num'") print $0}' > $output_name
    #cat header.vcf trio_NA12878_chrxx.vcf > trio_NA12878_chrxx_final.vcf

done




