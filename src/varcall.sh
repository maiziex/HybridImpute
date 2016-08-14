#!/bin/bash

for i in {1..22}
do
    (java -jar /scail/u/zhanglu2/GATK/GenomeAnalysisTK.jar -R /scail/u/zhanglu2/reference/refdata-hg19-2.0.0/fasta/genome.fa -T HaplotypeCaller -I NA12878_chr"$i"_hp1_sorted.bam -I NA12878_chr"$i"_hp2_sorted.bam -I NA12878_chr"$i"_nohp_sorted.bam -I NA12891_chr"$i"_hp1_sorted.bam -I NA12891_chr"$i"_hp2_sorted.bam -I NA12891_chr"$i"_nohp_sorted.bam -I NA12892_chr"$i"_hp1_sorted.bam -I NA12892_chr"$i"_hp2_sorted.bam -I NA12892_chr"$i"_nohp_sorted.bam -o chr"$i".vcf)&

done
