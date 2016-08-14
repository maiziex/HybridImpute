#!/bin/bash

############################# cut chromosome for three files ################################

for i in {1..22}
do
    chr_num=$i

    output_prefix="NA12878_gold_pos_chr"
    output_suffix=".vcf"
    output_name=$output_prefix$i$output_suffix

    cat /scail/u/xzhou15/CancerProj_10X/NA12878_GIAB_highconf_IllFB-IllGATKHC-CG-Ion-Solid_ALLCHROM_v3.2.2_highconf.vcf | awk '{if($1=="'$chr_num'") print $2}' > $output_name


done


for i in {1..22}
do
    chr="chr"
    chr_num=$chr$i

    output_prefix="phase_convert_chr"
    output_suffix=".vcf"
    output_name=$output_prefix$i$output_suffix


    cat /scail/u/xzhou15/CancerProj_10X/whatshap_results/phased_convert.vcf | awk '{if($1=="'$chr_num'") print $0}' > $output_name


done


for i in {1..22}
do
    chr="chr"
    chr_num=$chr$i

    output_prefix="10x_phased_chr"
    output_suffix=".vcf"
    output_name=$output_prefix$i$output_suffix


    cat /scail/u/xzhou15/CancerProj_10X/phasedvcf/merge_NA12878_forwhatshap.vcf | awk '{if($1=="'$chr_num'") print $0}' > $output_name


done


############################# only select gold loci ################################

for i in {1..22}
do
    input_prefix="phase_convert_chr"
    input_suffix=".vcf"
    input_name=$input_prefix$i$input_suffix


    input2_prefix="NA12878_gold_pos_chr"
    input2_suffix=".vcf"
    input2_name=$input2_prefix$i$input2_suffix

    output_prefix="phase_convert_gold_pos_chr"
    output_suffix=".vcf"
    output_name=$output_prefix$i$output_suffix



    cat /scail/u/xzhou15/CancerProj_10X/whatshap_results/usegold/$input_name |sort -k2,2| join -t$'\t' -1 2 -2 1 - <(cat /scail/u/xzhou15/CancerProj_10X/whatshap_results/usegold/$input2_name | sort -k1,1) | awk -F $'\t' ' { t = $1; $1 = $2; $2 = t; print; } ' OFS=$'\t' | sort -nk2 > $output_name




done

for i in {1..22}
do
    input_prefix="10x_phased_chr"
    input_suffix=".vcf"
    input_name=$input_prefix$i$input_suffix


    input2_prefix="NA12878_gold_pos_chr"
    input2_suffix=".vcf"
    input2_name=$input2_prefix$i$input2_suffix

    output_prefix="10x_phased_gold_pos_chr"
    output_suffix=".vcf"
    output_name=$output_prefix$i$output_suffix



    cat /scail/u/xzhou15/CancerProj_10X/whatshap_results/usegold/$input_name |sort -k2,2| join -t$'\t' -1 2 -2 1 - <(cat /scail/u/xzhou15/CancerProj_10X/whatshap_results/usegold/$input2_name | sort -k1,1) | awk -F $'\t' ' { t = $1; $1 = $2; $2 = t; print; } ' OFS=$'\t'  | sort -nk2 > $output_name



done


cat phase_convert_gold_pos_chr1.vcf phase_convert_gold_pos_chr2.vcf phase_convert_gold_pos_chr3.vcf phase_convert_gold_pos_chr4.vcf phase_convert_gold_pos_chr5.vcf phase_convert_gold_pos_chr6.vcf phase_convert_gold_pos_chr7.vcf phase_convert_gold_pos_chr8.vcf phase_convert_gold_pos_chr9.vcf phase_convert_gold_pos_chr10.vcf phase_convert_gold_pos_chr11.vcf phase_convert_gold_pos_chr12.vcf phase_convert_gold_pos_chr13.vcf phase_convert_gold_pos_chr14.vcf phase_convert_gold_pos_chr15.vcf phase_convert_gold_pos_chr16.vcf phase_convert_gold_pos_chr17.vcf phase_convert_gold_pos_chr18.vcf phase_convert_gold_pos_chr19.vcf phase_convert_gold_pos_chr20.vcf phase_convert_gold_pos_chr21.vcf phase_convert_gold_pos_chr22.vcf > phase_convert_gold_pos_all.vcf




cat 10x_phased_gold_pos_chr1.vcf 10x_phased_gold_pos_chr2.vcf 10x_phased_gold_pos_chr3.vcf 10x_phased_gold_pos_chr4.vcf 10x_phased_gold_pos_chr5.vcf 10x_phased_gold_pos_chr6.vcf 10x_phased_gold_pos_chr7.vcf 10x_phased_gold_pos_chr8.vcf 10x_phased_gold_pos_chr9.vcf 10x_phased_gold_pos_chr10.vcf 10x_phased_gold_pos_chr11.vcf 10x_phased_gold_pos_chr12.vcf 10x_phased_gold_pos_chr13.vcf 10x_phased_gold_pos_chr14.vcf 10x_phased_gold_pos_chr15.vcf 10x_phased_gold_pos_chr16.vcf 10x_phased_gold_pos_chr17.vcf 10x_phased_gold_pos_chr18.vcf 10x_phased_gold_pos_chr19.vcf 10x_phased_gold_pos_chr20.vcf 10x_phased_gold_pos_chr21.vcf 10x_phased_gold_pos_chr22.vcf > 10x_phased_gold_pos_all.vcf



cat header1.vcf 10x_phased_gold_pos_all.vcf > 10x_phased_gold_pos.vcf

cat header2.vcf phase_convert_gold_pos_all.vcf > phase_convert_gold_pos.vcf











