#!/bin/bash

for i in {2..22}
do
    chr="chr"
    chr_num=$chr$i

    input_prefix="NA12878.chr"
    input_suffix=".bam"
    input_name=$input_prefix$i$input_suffix

    output_prefix="NA12878_chr"
    output_suffix="_hp1.bam"
    output_name=$output_prefix$i$output_suffix


    /scail/u/xzhou15/Softwares/samtools-1.3.1/samtools view /scail/u/xzhou15/CancerProj_10X/10xbamfiles/$input_name  | grep "HP:i:1" | sed 's/20976/20000/g' | /scail/u/xzhou15/Softwares/samtools-1.3.1/samtools view -bt /scail/u/zhanglu2/reference/refdata-hg19-2.0.0/fasta/genome.fa.fai > /scail/u/xzhou15/CancerProj_10X/10xbamfiles/$output_name


    /scail/u/xzhou15/Softwares/samtools-1.3.1/samtools reheader /scail/u/xzhou15/CancerProj_10X/10xbamfiles/NA12878_hp1_header.sam /scail/u/xzhou15/CancerProj_10X/10xbamfiles/NA12878_chr"$i"_hp1.bam > /scail/u/xzhou15/CancerProj_10X/10xbamfiles/ForVarCall/NA12878_chr"$i"_hp1.bam

    /scail/u/xzhou15/Softwares/samtools-1.3.1/samtools sort /scail/u/xzhou15/CancerProj_10X/10xbamfiles/ForVarCall/NA12878_chr"$i"_hp1.bam -o /scail/u/xzhou15/CancerProj_10X/10xbamfiles/ForVarCall/NA12878_chr"$i"_hp1_sorted.bam

    /scail/u/xzhou15/Softwares/samtools-1.3.1/samtools index /scail/u/xzhou15/CancerProj_10X/10xbamfiles/ForVarCall/NA12878_chr"$i"_hp1_sorted.bam

    rm  /scail/u/xzhou15/CancerProj_10X/10xbamfiles/$output_name
    rm  /scail/u/xzhou15/CancerProj_10X/10xbamfiles/ForVarCall/$output_name

done



