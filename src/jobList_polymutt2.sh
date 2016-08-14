#!/bin/bash 
for i in {1..22}
do
    chr="chr"
    chr_num=$chr$i
    
    genetic_map_prefix="genetic_map_GRCh37_chr"
    genetic_map_suffix=".txt"
    genetic_map=$genetic_map_prefix$i$genetic_map_suffix

    output_prefix="trio_NA12878_polymutt_chr"
    output_suffix=".vcf"
    output_name=$output_prefix$i$output_suffix

    ~/10X/Scripts/run_polymutt2.sh $chr_num $genetic_map $output_name
    
    #~/10X/Scripts/run_polymutt2.sh "chr1" genetic_map_GRCh37_chr1.txt trio_NA12878_polymutt_chr1.vcf
done
