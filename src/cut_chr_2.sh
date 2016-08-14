#!/bin/bash

for i in {12..22}
do
    chr="chr"
    chr_num=$chr$i

    output_prefix="NA12891.chr"
    output_suffix=".bam"
    output_name=$output_prefix$i$output_suffix

    /scail/u/xzhou15/Softwares/samtools-1.3.1/samtools view -b /scail/data/group/genomics/10X_family/rawdata/NA12891_GRCh37.bam $chr_num > /scail/u/xzhou15/CancerProj_10X/10xbamfiles/$output_name


done



