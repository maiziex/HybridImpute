set -x
out_dir=$1
num=$2
declare -a arr=("aa" "ab" "ac" "ad" "ae" "af" "ag" "ah" "ai" "aj" "ak" "al" "am" "an" "ao" "ap" "aq" "ar" "as" "at" "au" "av" "aw" "ax" "ay" "az" "ba" "bb" "bc" "bd" "be" "bf" "bg" "bh" "bi" "bj" "bk" "bl" "bm" "bn" "bo" "bp" "bq" "br" "bs" "bt" "bu" "bv" "bw" "bx" "by" "bz" "ca" "cb" "cc" "cd" "ce" "cf" "cg" "ch" "ci" "cj" "ck" "cl" "cm" "cn" "co" "cp" "cq" "cr" "cs" "ct" "cu" "cv" "cw" "cx" "cy" "cz" "da" "db" "dc" "dd" "de" "df" "dg" "dh" "di" "dj" "dk" "dl" "dm" "dn" "do" "dp" "dq" "dr" "ds" "dt" "du" "dv")

start=0
for j in `eval echo {$start..$num}`
do
    echo ${arr[$j]}
    i=${arr[$j]}

    if [ "$i" == "aa" ]
    then
        cp $out_dir"quast_result_"$i/contigs_reports/all_alignments_supernova_contig-fasta"$i".tsv  temp_"$i".tsv
    else
        cat $out_dir"quast_result_"$i/contigs_reports/all_alignments_supernova_contig-fasta"$i".tsv | tail -n+2 >  temp_"$i".tsv
    fi

    cat temp_"$i".tsv>>"$out_dir"all_alignments_supernova_contig-fasta.tsv 
    rm temp_"$i".tsv
done
